import random

# Operações do aventureiro
def aventureiro_andar(aventureiro, direcao):
    x, y = aventureiro["posicao"]

    if direcao == 'W' and y > 0:  # Cima
        y -= 1
        aventureiro["posicao"] = [x, y]
        return True
    elif direcao == 'A' and x > 0:  # Esquerda
        x -= 1
        aventureiro["posicao"] = [x, y]
        return True
    elif direcao == 'S' and y < 9:  # Baixo
        y += 1
        aventureiro["posicao"] = [x, y]
        return True
    elif direcao == 'D' and x < 9:  # Direita
        x += 1
        aventureiro["posicao"] = [x, y]
        return True
    else:
        return False

def aventureiro_atacar(aventureiro):
    forca = aventureiro['forca']
    return forca + random.randint(1, 6)

def aventureiro_defender(aventureiro, dano):
    defesa = aventureiro['defesa']
    vida = aventureiro['vida']
    dano_absorvido = dano - defesa
    if dano_absorvido > 0:
        vida -= dano_absorvido
        aventureiro['vida'] = vida

def ver_atributos_aventureiro(aventureiro):
    print("Nome:", aventureiro['nome'])
    print("Vida:", aventureiro['vida'])
    print("Força:", aventureiro['forca'])
    print("Defesa:", aventureiro['defesa'])

def aventureiro_esta_vivo(aventureiro):
    return aventureiro['vida'] > 0

# Operações do monstro
def novo_monstro():
    print("Um novo monstro apareceu!")
    return {"forca": random.randint(5, 25), "vida": random.randint(10, 100)}

def monstro_atacar(monstro):
    return monstro["forca"]

def monstro_defender(monstro, dano):
    monstro["vida"] -= dano

def monstro_esta_vivo(monstro):
    return monstro["vida"] > 0

# Operações do mapa
def desenhar(aventureiro, tesouro):
    for y in range(10):
        for x in range(10):
            if [x, y] == aventureiro["posicao"]:
                print("@", end=" ")
            elif [x, y] == tesouro:
                print("X", end=" ")
            else:
                print(".", end=" ")
        print()

# Combate
def iniciar_combate(aventureiro, monstro):
    while True:
        # Aventureiro ataca o monstro
        dano_ataque_aventureiro = aventureiro_atacar(aventureiro)
        monstro_defender(monstro, dano_ataque_aventureiro)
        print(aventureiro['nome'], "causa", dano_ataque_aventureiro, "de dano. Vida atual do monstro: ", monstro["vida"])
        if not monstro_esta_vivo(monstro):
            print("O monstro foi derrotado!")
            return True

        # Monstro ataca o aventureiro
        dano_ataque_monstro = monstro_atacar(monstro)
        aventureiro_defender(aventureiro, dano_ataque_monstro)
        print("Monstro causa", dano_ataque_monstro, "de dano. Vida atual de", aventureiro['nome'], ":", aventureiro["vida"])
        if not aventureiro_esta_vivo(aventureiro):
            print("O aventureiro foi derrotado!")
            return False

# Operação principal do jogo
def movimentar(aventureiro, direcao):
    if not aventureiro_andar(aventureiro, direcao):
        return True

    efeito = random.choices(["nada", "monstro"], [0.6, 0.4])[0]
    if efeito == "monstro":
        monstro = novo_monstro()
        return iniciar_combate(aventureiro, monstro)

    return True

def gerar_tesouro(aventureiro):
    while True:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        if [x, y] != aventureiro["posicao"]:
            return [x, y]

def main():
    aventureiro = {
        "forca": random.randint(10, 18),
        "defesa": random.randint(10, 18),
        "vida": random.randint(100, 120),
        "posicao": [0, 0]
    }

    tesouro = gerar_tesouro(aventureiro)

    aventureiro["nome"] = input("Deseja buscar um tesouro? Primeiro, informe seu nome: ")
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

        if aventureiro["posicao"] == tesouro:
            print(f"Parabéns, {aventureiro['nome']}! Você encontrou o tesouro!")
            break

if __name__ == "__main__":
    main()
