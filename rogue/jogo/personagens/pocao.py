import random

class Pocao:
    def __init__(self, tesouro, obstaculos):
        """
        Gera uma poção em uma posição aleatória no mapa, diferente de [0, 0] e também diferente dos obstaculos e tesouro.

        Ou seja, deve gerar uma coordenada x entre 0 e 9, e uma coordenada y entre
        0 e 9. Porém, se a coordenada gerada for (0, 0) ou igual aos outros , deve gerar uma nova
        coordenada, até atender ao requisito.
        """
        pos_preenchidas = [[0, 0], tesouro.posicao] + [obstaculo.posicao for obstaculo in obstaculos]
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if [x, y] not in pos_preenchidas:
                break

        self.posicao = [x, y]
    
    def exportar(self):
        return {"pocao": self.posicao}

    def importar(self, dados):
        self.posicao = dados["pocao"]
    
