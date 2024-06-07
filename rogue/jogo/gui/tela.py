from .cores import CORES

from ..mecanicas import relogio

import pygame

GRID = 40
TAMANHO_MAPA = 10

LARGURA_ADICIONAL = 500
ALTURA_ADICIONAL = 100
MARGEM = 10

LARGURA = TAMANHO_MAPA * GRID + LARGURA_ADICIONAL
ALTURA = TAMANHO_MAPA * GRID + ALTURA_ADICIONAL

FONTE = "Courier New"

def centralizar_texto_mapa(posicao_inicial, texto):
    x0 = posicao_inicial[0] * GRID + (GRID - texto.get_width()) // 2
    y0 = posicao_inicial[1] * GRID + (GRID - texto.get_height()) // 2
    return [x0 + LARGURA_ADICIONAL // 2, y0 + ALTURA_ADICIONAL // 2]

class Tela:
    def __init__(self):
        self.display = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Rogue")

    def renderizar(self, aventureiro, tesouro, mensagem_combate, obstaculos,pocao):
        self.display.fill(CORES.preto)
        self.aventureiro(aventureiro)
        self.tesouro(tesouro)
        self.obstaculos(obstaculos)
        self.pocao(pocao)
        self.mapa(aventureiro, tesouro, obstaculos,pocao)
        self.combate(mensagem_combate)
        self.cronometro()
        self.mostrar_dificuladade(aventureiro)
        self.mostrar_ouro(aventureiro)

        pygame.display.update()

    def cronometro(self):
        tempo = relogio.tempo_decorrido()
        fonte = pygame.font.SysFont(FONTE, GRID // 2)
        texto = fonte.render(tempo, True, CORES.branco)
        self.display.blit(texto, [LARGURA - MARGEM - texto.get_width(), MARGEM])
    
    def mostrar_dificuladade(self, aventureiro):
        dificuldade = aventureiro.dificuldade 
        fonte = pygame.font.SysFont(FONTE, GRID // 2)
        texto = fonte.render(f"Dificuldade:{dificuldade:0.4f}", True, CORES.branco)
        self.display.blit(texto, [LARGURA - MARGEM - texto.get_width(), MARGEM * 2 + texto.get_height()])

    def obstaculos(self, obstaculos):
        for obstaculo in obstaculos:
            self.desenha_mensagem("O", obstaculo.posicao)
    
    def pocao(self, pocao):
            self.desenha_mensagem("%", pocao.posicao)
   
    def combate(self, mensagem_combate):
        fonte = pygame.font.SysFont(FONTE, GRID // 2)
        texto = fonte.render(mensagem_combate, True, CORES.branco)
        self.display.blit(texto, [MARGEM, MARGEM])

    def mostrar_ouro(self, aventureiro):
        fonte = pygame.font.SysFont(FONTE, GRID // 2)
        texto = fonte.render(f"Ouro: {aventureiro.ouro}", True, CORES.branco)
        self.display.blit(texto, [MARGEM, MARGEM+22])

    def desenha_mensagem(self, mensagem, posicao, cor=CORES.branco):
        fonte = pygame.font.SysFont(FONTE, GRID)
        texto = fonte.render(mensagem, True, cor)
        self.display.blit(texto, centralizar_texto_mapa(posicao, texto))

    def aventureiro(self, aventureiro):
        self.desenha_mensagem(aventureiro.char, aventureiro.posicao, aventureiro.cor)

        atributos = f"{aventureiro.nome} nv {aventureiro.nivel} ({aventureiro.xp}/{aventureiro.xp_por_nivel}) - " \
            f"Vida {aventureiro.vida} - Força {aventureiro.forca} - Defesa {aventureiro.defesa} - Movimentos {aventureiro.movimentos}"

        fonte = pygame.font.SysFont(FONTE, GRID // 2)
        texto = fonte.render(atributos, True, CORES.branco)

        y = GRID * TAMANHO_MAPA + ALTURA_ADICIONAL - MARGEM - texto.get_height()
        texto_rect =texto.get_rect(center=(LARGURA/2,y))
        self.display.blit(texto,texto_rect)

    def tesouro(self, tesouro):
        self.desenha_mensagem("X", tesouro.posicao,tesouro.cor)

    def mapa(self, aventureiro, tesouro, obstaculos,pocao):
        for linha in range(TAMANHO_MAPA):
            for coluna in range(TAMANHO_MAPA):
                pos_preenchidas = [aventureiro.posicao, tesouro.posicao,pocao.posicao]
                for obstaculo in obstaculos:
                    pos_preenchidas.append(obstaculo.posicao)
                if [linha, coluna] not in pos_preenchidas:
                    self.desenha_mensagem(".", [linha, coluna])
