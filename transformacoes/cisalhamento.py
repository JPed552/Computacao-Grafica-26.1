# Cisalhamento (shear) — distorce o objeto inclinando seus eixos.
#   shx → desloca X proporcionalmente a Y (inclina na horizontal)
#   shy → desloca Y proporcionalmente a X (inclina na vertical)
def cisalhamento(shx, shy):
    return [[  1, shx, 0],
            [shy,   1, 0],
            [  0,   0, 1]]
