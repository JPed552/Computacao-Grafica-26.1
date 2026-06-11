import math

# Rotacao R(theta) — gira o objeto em torno da origem no sentido anti-horario.
# Usa seno e cosseno do angulo para montar a matriz de rotacao 2D em coord. homogeneas.
def rotacao(graus):
    rad = math.radians(graus)
    c   = math.cos(rad)
    s   = math.sin(rad)
    return [[ c, -s, 0],
            [ s,  c, 0],
            [ 0,  0, 1]]
