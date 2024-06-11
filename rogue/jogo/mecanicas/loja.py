import pygame
LARGURA_BOTAO = 196
MARGEM = 22


def analizar_clique(pos):
    x, y = pos

    x_esq = MARGEM
    x_dir = MARGEM + LARGURA_BOTAO

    y_sup1 = 144
    y_inf1 = 104

    y_sup2 = 209
    y_inf2 = 169

    y_sup3 = 274
    y_inf3 = 234

    y_sup4 = 339
    y_inf4 = 229

    y_sup5 = 404
    y_inf5 = 364


    if x_esq <= x <= x_dir and y_inf1 <= y <= y_sup1:
        return "Ataduras"

    elif x_esq <= x <= x_dir and y_inf2 <= y <= y_sup2:
        return "Pocao de xp"
    
    elif x_esq <= x <= x_dir and y_inf3 <= y <= y_sup3:
        return "Pocao de vida"
    
    elif x_esq <= x <= x_dir and y_inf4 <= y <= y_sup4:
        return "Pocao de força"
    
    elif x_esq <= x <= x_dir and y_inf5 <= y <= y_sup5:
        return "Pocao de defesa"

    else:
        return ""