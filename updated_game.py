import random

# Função para centralizar texto
def centralizar_texto(texto, largura=80):
    return texto.center(largura)

# Função para colorir o texto no terminal
def colorir_texto(texto, cor):
    cores = {
        "vermelho": "\033[91m",
        "reset": "\033[0m"
    }
    return f"{cores[cor]}{texto}{cores['reset']}"

# Função para exibir índice de dificuldade no canto superior direito
def exibir_dificuldade(dificuldade, largura=80):
    texto = f"Índice de dificuldade: {dificuldade:.4f}"
    espacos = largura - len(texto)
    print(" " * espacos + texto)

# Operações do aventureiro
def aventureiro_andar(aventureiro, direcao):
    if direcao == "W" and aventureiro['posicao'][1] != 0:
        aventureiro['posicao'][1] -= 1
        return True
    elif direcao == "A" and aventureiro['posicao'][0] != 0:
        aventureiro['posicao'][0] -= 1
        return True
    elif direcao == "S" and aventureiro['posicao'][1] != 9:
        aventureiro['posicao'][1] += 1
        return True
    elif direcao == "D" and aventureiro['posicao'][0] != 9:
        aventureiro['posicao'][0] += 1
        return True
    return False

def aventureiro_atacar(aventureiro):
    return aventureiro['forca'] + random.randint(1, 6)

def aventureiro_defender(aventureiro, dano):
    dano_absorvido = dano - aventureiro['defesa']
    if dano_absorvido > 0:
        aventureiro['vida'] -= dano_absorvido

def ver_atributos_aventureiro(aventureiro, movimentos):
    atributos = (f"Aventureiro {aventureiro['nome']} - Vida: {aventureiro['vida']} - Força: {aventureiro['forca']} - "
                 f"Defesa: {aventureiro['defesa']} - {movimentos} movimentos")
    print(centralizar_texto(atributos))

def aventureiro_esta_vivo(aventureiro):
    return aventureiro['vida'] > 0

# Operações do monstro
def novo_monstro():
    print("Um novo monstro apareceu!")
    return {'forca': random.randint(5, 25), 'vida': random.randint(10, 100)}

def monstro_atacar(monstro):
    return monstro['forca']

def monstro_defender(monstro, dano):
    monstro['vida'] -= dano

def monstro_esta_vivo(monstro):
    return monstro['vida'] > 0

# Operações do mapa
def desenhar(aventureiro, tesouro, pocao):
    for y in range(10):
        for x in range(10):
            if [x, y] == aventureiro["posicao"]:
                print("@", end=" ")
            elif [x, y] == tesouro["posicao"]:
                print(colorir_texto("X", "vermelho"), end=" ")
            elif [x, y] == pocao["posicao"]:
                print("%", end=" ")
            else:
                print(".", end=" ")
        print()

# Combate
def iniciar_combate(aventureiro, monstro):
    while True:
        dano_causado_aventureiro = aventureiro_atacar(aventureiro)
        monstro_defender(monstro, dano_causado_aventureiro)
        print(f"{aventureiro['nome']} causa {dano_causado_aventureiro} de dano! Vida do monstro: {monstro['vida']}")
        if not monstro_esta_vivo(monstro):
            print("Monstro foi derrotado!")
            return True
        
        dano_causado_monstro = monstro_atacar(monstro)
        aventureiro_defender(aventureiro, dano_causado_monstro)
        print(f"Monstro causa {dano_causado_monstro} de dano! Vida de {aventureiro['nome']}: {aventureiro['vida']}")
        if not aventureiro_esta_vivo(aventureiro):
            print(f"{aventureiro['nome']}, você foi derrotado!")
            return False

# Operação principal do jogo
def movimentar(aventureiro, direcao, movimentos):
    if not aventureiro_andar(aventureiro, direcao):
        print("Movimento inválido, Atenção aos limites do mapa!")
        return True, movimentos

    movimentos += 1
    efeito = random.choices(["nada", "monstro"], [0.6, 0.4])[0]
    if efeito == "monstro":
        monstro = novo_monstro()
        return iniciar_combate(aventureiro, monstro), movimentos

    return True, movimentos

def gerar_tesouro():
    while True:
        x, y = random.randint(0, 9), random.randint(0, 9)
        if [x, y] != [0, 0]:
            return {'posicao': [x, y]}

def gerar_pocao():
    while True:
        x, y = random.randint(0, 9), random.randint(0, 9)
        if [x, y] != [0, 0]:
            return {'posicao': [x, y]}

def aplicar_efeito_pocao(aventureiro):
    efeito = random.choice(["vida", "forca", "defesa"])
    if efeito == "vida":
        aventureiro['vida'] *= 2
        print(f"{aventureiro['nome']} encontrou uma poção! Vida dobrada!")
    elif efeito == "forca":
        aventureiro['forca'] += 15
        print(f"{aventureiro['nome']} encontrou uma poção! Força aumentada em 15!")
    elif efeito == "defesa":
        aventureiro['defesa'] += 10
        print(f"{aventureiro['nome']} encontrou uma poção! Defesa aumentada em 10!")

def main():
    movimentos = 0
    dificuldade = random.uniform(0.1, 10.0)
    
    nome_aventureiro = input("Deseja buscar um tesouro? Primeiro, informe seu nome: ")
    if nome_aventureiro.upper() == "SEGREDO":
        aventureiro = {
            "nome": nome_aventureiro,
            "forca": 30,
            "defesa": 30,
            "vida": 200,
            "posicao": [0, 0]
        }
    else:
        aventureiro = {
            "nome": nome_aventureiro,
            "forca": random.randint(10, 18),
            "defesa": random.randint(10, 18),
            "vida": random.randint(100, 120),
            "posicao": [0, 0]
        }

    tesouro = gerar_tesouro()
    pocao = gerar_pocao()

    print(f"Saudações, {aventureiro['nome']}! Boa sorte!")
    exibir_dificuldade(dificuldade)
    desenhar(aventureiro, tesouro, pocao)
    ver_atributos_aventureiro(aventureiro, movimentos)

    while True:
        op = input("Insira o seu comando: ").upper()
        if op == "Q":
            print("Já correndo?")
            break
        elif op == "T":
            ver_atributos_aventureiro(aventureiro, movimentos)
        elif op in ["W", "A", "S", "D"]:
            resultado, movimentos = movimentar(aventureiro, op, movimentos)
            if not resultado:
                print("Game Over...")
                break
            if aventureiro['posicao'] == tesouro['posicao']:
                print(f"Parabéns, {aventureiro['nome']}! Você encontrou o tesouro!")
                break
            elif aventureiro['posicao'] == pocao['posicao']:
                aplicar_efeito_pocao(aventureiro)
                pocao['posicao'] = [-1, -1]  # Remove a poção do mapa

            exibir_dificuldade(dificuldade)
            desenhar(aventureiro, tesouro, pocao)
            ver_atributos_aventureiro(aventureiro, movimentos)
        else:
            print(f"{aventureiro['nome']}, não conheço essa opção! Tente novamente!")

if __name__ == "__main__":
    main()
