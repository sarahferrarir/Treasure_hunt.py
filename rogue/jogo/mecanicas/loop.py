import time

import random

from jogo.gui.tela import Tela
from ..mecanicas import som

from . import movimento
from . import inputbox
from . import buttonbox
from . import arquivo
from . import loja

from jogo.personagens.monstros.boss import Boss
from jogo.personagens.aventureiro.aventureiro import Aventureiro
from jogo.personagens.aventureiro.guerreiro import Guerreiro
from jogo.personagens.aventureiro.tank import Tank
from jogo.personagens.aventureiro.secreto import Secreta
from jogo.personagens.tesouro import Tesouro
from jogo.personagens.obstaculo import Obstaculo
from jogo.personagens.pocao import Pocao 

import pygame

def jogo():
    tesouro = Tesouro()

    nome = inputbox.ler_texto("Informe o seu nome:")
    if nome == "SEGREDO":
        classe = "Secreta"
    else:
        classe = buttonbox.selecionar_classe("Clique na classe desejada:")

    match classe:
        case "Aventureiro":
            jogador = Aventureiro(nome)
        case "Guerreiro":
            jogador = Guerreiro(nome)
        case "Tank":
            jogador = Tank(nome)
        case "Secreta":
            jogador = Secreta(nome)

    print(f"Saudações, {jogador.nome}! Boa sorte!")

    obstaculos = []
    for _ in range(5):
        obstaculos.append(Obstaculo(tesouro, obstaculos))

    pocao = Pocao(tesouro,obstaculos)

    tela = Tela()

    mensagem_combate = ""
    jogo_acabou = False
    while not jogo_acabou:
        # Controlar os eventos
        teclas = pygame.key.get_pressed()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            
            if evento.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                match loja.analizar_clique(pos):
                    case "Ataduras":
                        if jogador.ouro - 5 >= 0:
                            jogador.ouro -= 5
                            jogador.vida += 10
                            mensagem_combate = "Você comprou ataduras! um pouco de vitalidade aumentada."
                        else:
                            mensagem_combate = "Você não possui ouro suficiente."
                    case "Pocao de xp":
                        if jogador.ouro - 10 >= 0:
                            jogador.ouro -= 10
                            jogador.xp += 5
                            if jogador.xp >= jogador.xp_por_nivel:
                                jogador.xp -= jogador.xp_por_nivel
                                jogador.subir_nivel()
                            mensagem_combate = "Você comprou uma poção de xp! xp aumentado."
                        else:
                            mensagem_combate = "Você não possui ouro suficiente."
                    case "Pocao de vida":
                        if jogador.ouro - 15 >= 0:
                            jogador.ouro -= 15
                            jogador.vida += 50
                            mensagem_combate = "Você comprou uma poção de vida! Vitalidade aumentada."
                        else:
                            mensagem_combate = "Você não possui ouro suficiente."
                    case "Pocao de força":
                        if jogador.ouro - 15 >= 0:
                            jogador.ouro -= 15
                            jogador.forca += 10
                            mensagem_combate = "Você comprou uma poção de força! Força aumentada."
                        else:
                            mensagem_combate = "Você não possui ouro suficiente."
                    case "Pocao de defesa":
                        if jogador.ouro - 15 >= 0:
                            jogador.ouro -= 15
                            jogador.defesa += 5
                            mensagem_combate = "Você comprou uma poção de defesa! Defesa aumentada."
                        else:
                            mensagem_combate = "Você não possui ouro suficiente."
                

            if evento.type == pygame.KEYUP:
                if teclas[pygame.K_q]:
                    print("Já correndo?")
                    jogo_acabou = True

                if teclas[pygame.K_p]:
                    arquivo.salvar(jogador, tesouro, obstaculos,pocao)
                elif teclas[pygame.K_o]:
                    if arquivo.save_existe():
                        jogador, tesouro, obstaculos,pocao = arquivo.carregar()
                elif teclas[pygame.K_z]:
                    jogador.mudar_cor()
                elif teclas[pygame.K_x]:
                    jogador.mudar_char()
                elif teclas[pygame.K_KP_PLUS]:
                    jogador.aumentar_dificuldade()
                elif teclas[pygame.K_KP_MINUS]:
                    jogador.diminuir_dificuldade()
                else:
                    # Executar as ações do jogo
                    resultado, nome_monstro = movimento.movimentar(jogador, teclas, obstaculos)
                    if resultado == 0:
                        mensagem_combate = f"Você foi derrotado por {nome_monstro}..."
                        jogo_acabou = True
                    elif resultado == 1:
                        mensagem_combate = f"{nome_monstro} foi derrotado!"
                    else:
                        mensagem_combate = "Você não encontrou nada"
                    if jogador.posicao == pocao.posicao:
                         efeito = random.choices(["vida", "forca", "defesa"])[0]
                         match efeito:
                            case "vida":
                             jogador.vida = 2*jogador.vida
                             mensagem_combate = "Você encontrou uma poção! Vitalidade aumentada."
                            case "forca":
                             jogador.forca += 15
                             mensagem_combate = "Você encontrou uma poção! Força aumentada."
                            case "defesa":
                             jogador.defesa += 10
                             mensagem_combate = "Você encontrou uma poção! Resistência aumentada."
                         som.tomar_pocao()
                         pocao.posicao = [100,100]
                            

                    if jogador.posicao == tesouro.posicao:
                        boss = Boss(jogador.dificuldade)
                        if movimento.iniciar_combate(jogador, boss):
                            mensagem_combate = f"Parabéns, {jogador.nome}, você encontrou o tesouro!"
                        else:
                            mensagem_combate = f"Você foi derrotado pelo chefão... =("

                        jogo_acabou = True

        # Desenho na tela
        tela.renderizar(jogador, tesouro, mensagem_combate, obstaculos, pocao)

        # Chamar o relógio interno do jogo
        pygame.time.Clock().tick(60)

    time.sleep(2)
