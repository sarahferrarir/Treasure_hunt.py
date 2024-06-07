from .aventureiro import Aventureiro

class Secreta(Aventureiro):
    def __init__(self, nome):
        super().__init__(nome)
        self.char = "S"
        self.vida = 200
        self.forca = 30
        self.defesa = 30
        self.chars_possiveis.append("S")

