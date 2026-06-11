# Escala S(sx, sy) — redimensiona o objeto em relacao a origem.
# sx e sy na diagonal principal controlam o fator de escala em cada eixo.
def escala(sx, sy):
    return [[sx,  0, 0],
            [ 0, sy, 0],
            [ 0,  0, 1]]
