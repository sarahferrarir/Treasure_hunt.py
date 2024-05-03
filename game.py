import random

# Operações do aventureiro
def aventureiro_andar(aventureiro, direcao):
    """
    Altera o valor da posição do aventureiro conforme a direção informada pelo
    usuário. Direções válidas:
    - W: cima
    - A: esquerda
    - S: baixo
    - D: direita

    Se o aventureiro estiver nos limites do mapa, não faz nenhum movimento.

    Considerar que o mapa é um sistema cartesiano, com o eixo x aumentando da esquerda para a direita, e o eixo y aumentando de cima para baixo.
    Portanto, as coordenadas (0, 0) estão no canto superior esquerdo do mapa, enquanto que as coordenadas (9, 9) estão no canto inferior direito.
    Retorna True caso o aventureiro tenha andado, e False caso contrário.
    """
    match direcao:
        case "W":
            if aventureiro['posicao'][1] != 0:
                aventureiro['posicao'][1] -= 1
                return True
        case"A":
            if aventureiro['posicao'][0] != 0:
                aventureiro['posicao'][0] -= 1
                return True
        case"S":
            if aventureiro['posicao'][1] != 9:
                aventureiro['posicao'][1] += 1
                return True
        case "D":
            if aventureiro['posicao'][0] != 9:
                aventureiro['posicao'][0] += 1
                return True
    return False
    


def aventureiro_atacar(aventureiro): 
    """
    Retorna um inteiro igual à Força do aventureiro, mais um valor aleatório
    entre 1 e 6.
    """
    return aventureiro['forca'] + random.randint(1,6)

def aventureiro_defender(aventureiro, dano): 
    """
    Calcula o dano a ser absorvido pelo aventureiro, igual ao dano causado
    menos o atributo de defesa do aventureiro.

    Se o dano a ser absorvido é menor ou igual a zero, não faz nada. Se for
    maior que zero, reduz esse dano da vida do aventureiro.
    """
    dano_absorvido = dano - aventureiro['defesa']
    if dano_absorvido > 0:
        aventureiro['vida'] -= dano_absorvido

def ver_atributos_aventureiro(aventureiro): 
    """
    Exibe na tela os atributos do aventureiro (nome, vida, força, defesa).
    """
    for k,v in aventureiro.items():
        print(f"{k}: {v}")
    

def aventureiro_esta_vivo(aventureiro): 
    """
    Retorna True se a vida do aventureiro é maior que zero.
    """
    return aventureiro['vida'] > 0

# Operações do monstro
def novo_monstro():
    """
    Inicia um novo monstro, retornando um dicionário com as seguintes chaves
    e valores:

    - forca: Um valor aleatório entre 5 e 25
    - vida: um valor aleatório entre 10 e 100

    Antes de retornar o dicionário, exibe na tela a mensagem "Um novo monstro
    apareceu!".
    """
    print("Um novo monstro apareceu!")
    return {'forca':random.randint(5,25),'vida':random.randint(10,100)}

def monstro_atacar(monstro):
    """
    Retorna o dano do monstro, igual ao seu atributo de força.
    """
    return monstro['forca']

def monstro_defender(monstro, dano):
    """
    Reduz o dano causado da vida do monstro.
    """
    monstro['vida'] -= dano

def monstro_esta_vivo(monstro):
    """
    Retorna True se a vida do monstro é maior que zero.
    """
    return monstro['vida'] > 0

# Operações do mapa
def desenhar(aventureiro, tesouro):
    """
    Desenha um mapa 10 x 10, posicionando o tesouro e o aventureiro.
    Representa o aventureiro por um @, o tesouro por um X, e por um ponto (.)
    os demais locais.
    """
    for y in range(10):
        for x in range(10):
            if [x, y] == aventureiro["posicao"]:
                print("@", end=" ")
            elif [x, y] == tesouro["posicao"]:
                print("X", end=" ")
            else:
                print(".", end=" ")
        print()

# Combate
def iniciar_combate(aventureiro, monstro):
    """
    Executa um loop infinito, que possui as seguintes etapas:
    - Calcula o dano causado pelo aventureiro
    - Monstro faz a sua defesa
    - Exibe na tela o dano causado pelo aventureiro e a vida atual do monstro
    - Se o monstro não está mais vivo, retorna True
    - Calcula o dano causado pelo monstro
    - Aventureiro faz sua defesa
    - Exibe na tela o dano causado pelo monstro e a vida atual do aventureiro
    - Se o aventureiro não está mais vivo, retorna False
    """
    while True:
        #Calcula o dano causado do aventureiro
        dano_causado_aventureiro = aventureiro_atacar(aventureiro)
        
        #defesa do monstro
        monstro_defender(monstro,dano_causado_aventureiro)

        #exibe na tela o dano causado pelo aventureiro, a vida tual do monstro e verifica se aventureiro foi derrotado
        print(f"{aventureiro['nome']} causa {dano_causado_aventureiro} de dano!  Vida do monstro: {monstro['vida']}")
        if not monstro_esta_vivo(monstro):
            print("Monstro foi derrotado!")
            return True
        # exibe na tela o dano causado pelo monstro, a vida tual do aventureiro e verifica se o monstro foi derrotado
        dano_causado_monstro = monstro_atacar(monstro)
        aventureiro_defender(aventureiro,dano_causado_monstro)
        print(f"Monstro causa {dano_causado_monstro} de dano! Vida de {aventureiro['nome']}: {aventureiro['vida']}")
        if not aventureiro_esta_vivo(aventureiro):
            print(f"{aventureiro['nome']}, você foi derrotado!")
            return False
            

# Operação principal do jogo
def movimentar(aventureiro, direcao):
    """
    Realiza a ação de movimento e analisa as consequências.

    Chama a função aventureiro_andar e analisa o seu resultado. Se for False,
    ou seja, se o aventureiro não tiver andado nada, retorna True.

    Em seguida, analisa o efeito do movimento. Há 60% de chance de nada
    acontecer, e 40% de chance de um monstro aparecer (pesquise sobre a função
    random.choices).

    Se um monstro aparecer, inicia um novo monstro e retorna e resultado da
    função iniciar_combate.

    Caso não seja um monstro, retorna True.
    """
    if not aventureiro_andar(aventureiro, direcao):
        print("Movimento inválido, Atenção aos limites do mapa!")
        return True

    efeito = random.choices(["nada", "monstro"], [0.6, 0.4])[0]
    if efeito == "monstro":
        monstro = novo_monstro()
        return iniciar_combate(aventureiro, monstro)

    return True

def gerar_tesouro():
    """
    Gera o tesouro em uma posição aleatória no mapa, diferente de [0, 0].

    Ou seja, deve gerar uma coordenada x entre 0 e 9, e uma coordenada y entre
    0 e 9. Porém, se a coordenada gerada for (0, 0), deve gerar uma nova
    coordenada, até atender ao requisito.
    """
    x = random.randint(0,9)
    y = random.randint(0,9)
    if x == 0 and y == 0:
        gerar_tesouro()
    return {'posicao':[x,y]}
    


def main():
    """
    Fluxo principal do jogo, possui as seguintes etapas:
    - Inicia um aventureiro num dicionário com as propriedades:
        - forca: valor inteiro aleatório entre 10 e 18
        - defesa: valor inteiro aleatório entre 10 e 18
        - vida: valor inteiro aleatório entre 100 e 120
        - posicao: uma lista [0, 0]

    - Gera uma posição aleatória para o tesouro, usando a função gerar_tesouro
    - Lê um nome para o aventureiro, e armazena no dicionário
    - Desenha o mapa pela primeira vez
    - Em um loop infinito:
        - Lê o comando inserido pelo usuário
        - Se for o comando "Q", encerra o programa
        - Se for o comando "T", exibe os atributos do aventureiro
        - Se o comando for "W", "A", "S" ou "D":
            - Realiza o movimento e verifica o resultado da função movimentar
            - Se o resultado for True, desenha novamente o mapa
            - Se for False, imprime "Game over" na tela e encerra o programa
        - Se o usuário inserir algum comando diferente, diz que não reconheceu
        - Se a posição do aventureiro for igual à posição do tesouro, dispara
        uma mensagem que o aventureiro ganhou o jogo
    """
    aventureiro = {
        "forca": random.randint(10, 18),
        "defesa": random.randint(10, 18),
        "vida": random.randint(100, 120),
        "posicao": [0, 0]
    }

    tesouro = gerar_tesouro()

    aventureiro['nome'] = input("Deseja buscar um tesouro? Primeiro, informe seu nome: ")
    print(f"Saudações, {aventureiro['nome']}! Boa sorte!")

    desenhar(aventureiro, tesouro)

    while True:
        op = input("Insira o seu comando: ").upper()
        if op == "Q":
            print("Já correndo?")
            break
        elif op == "T":
            ver_atributos_aventureiro(aventureiro)
        elif op in ["W", "A", "S", "D"]:
            if movimentar(aventureiro, op):
                desenhar(aventureiro, tesouro)
            else:
                print("Game Over...")
                break
        else:
            print(f"{aventureiro['nome']}, não conheço essa opção! Tente novamente!")

        if aventureiro['posicao'] == tesouro['posicao']:
            print(f"Parabéns, {aventureiro['nome']}! Você encontrou o tesouro!")
            break

if __name__ == "__main__":
    main()
