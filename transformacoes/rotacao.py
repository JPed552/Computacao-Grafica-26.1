import math


def rotacao(graus):
    rad = math.radians(graus)
    c   = math.cos(rad)
    s   = math.sin(rad)
    return [[ c, -s, 0],
            [ s,  c, 0],
            [ 0,  0, 1]]
