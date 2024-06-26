import random

from .monstro import Monstro

class Thanos(Monstro):
    def __init__(self, dificuldade):
        self.nome = "Thanos"
        self.vida = int(dificuldade * random.randint(10, 100))
        self.forca = int(dificuldade * random.randint(15, 25))
        self.xp = int(2 * dificuldade)
        self.ouro = int(random.randint(1, 5) * dificuldade)
        print("Um Thanos apareceu!")

    def atacar(self):
        return self.forca + random.randint(1, 4)
