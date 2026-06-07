"""
Transformacoes geometricas 2D em coordenadas homogeneas.

Um ponto (x, y) eh representado como vetor coluna [x, y, 1]^T.
A transformacao aplica-se por: p' = M * p  (M eh 3x3).
"""

import math


# ---------------------------------------------------------------------------
# Utilitarios de algebra linear (matrizes 3x3)
# ---------------------------------------------------------------------------

def identidade():
    return [[1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]]


def mat_mult(A, B):
    """Multiplicacao de duas matrizes 3x3."""
    C = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                C[i][j] += A[i][k] * B[k][j]
    return C


def aplicar_ponto(M, x, y):
    """
    Aplica a matriz homogenea M (3x3) ao ponto (x, y).
    Retorna (x', y') apos divisao pela coordenada homogenea w.
    """
    xn = M[0][0] * x + M[0][1] * y + M[0][2]
    yn = M[1][0] * x + M[1][1] * y + M[1][2]
    w  = M[2][0] * x + M[2][1] * y + M[2][2]
    if w == 0:
        raise ValueError("Coordenada homogenea w == 0 (transformacao invalida).")
    return xn / w, yn / w


def aplicar_transformacao(vertices, M):
    """Aplica M a uma lista de pontos (x, y). Retorna lista transformada."""
    return [aplicar_ponto(M, x, y) for x, y in vertices]


# ---------------------------------------------------------------------------
# Gerador de poligono regular
# ---------------------------------------------------------------------------

def poligono_regular(n, raio):
    """
    Gera os n vertices de um poligono regular centrado na origem.
    Primeiro vertice no topo (angulo inicial = +pi/2).
    """
    vertices = []
    for k in range(n):
        angulo = math.pi / 2 + 2 * math.pi * k / n
        x = raio * math.cos(angulo)
        y = raio * math.sin(angulo)
        vertices.append((x, y))
    return vertices


# ---------------------------------------------------------------------------
# Construtores de matrizes de transformacao (coordenadas homogeneas)
# ---------------------------------------------------------------------------

def translacao(tx, ty):
    """T(tx, ty) — desloca o objeto por (tx, ty)."""
    return [[1, 0, tx],
            [0, 1, ty],
            [0, 0,  1]]


def escala(sx, sy):
    """S(sx, sy) — escala em relacao a origem."""
    return [[sx,  0, 0],
            [ 0, sy, 0],
            [ 0,  0, 1]]


def rotacao(graus):
    """R(theta) — rotacao anti-horaria em torno da origem."""
    rad = math.radians(graus)
    c   = math.cos(rad)
    s   = math.sin(rad)
    return [[ c, -s, 0],
            [ s,  c, 0],
            [ 0,  0, 1]]


def reflexao(eixo):
    """
    Reflexao em relacao ao eixo especificado.
      'x'      — eixo X
      'y'      — eixo Y
      'origem' — em relacao a origem
      'y=x'    — em relacao a reta y = x
    """
    if eixo == "x":
        return [[ 1,  0, 0],
                [ 0, -1, 0],
                [ 0,  0, 1]]
    if eixo == "y":
        return [[-1,  0, 0],
                [ 0,  1, 0],
                [ 0,  0, 1]]
    if eixo == "origem":
        return [[-1,  0, 0],
                [ 0, -1, 0],
                [ 0,  0, 1]]
    if eixo == "y=x":
        return [[ 0,  1, 0],
                [ 1,  0, 0],
                [ 0,  0, 1]]
    return identidade()


def cisalhamento(shx, shy):
    """
    Cisalhamento (shear).
      shx — fator horizontal (desloca x em funcao de y)
      shy — fator vertical   (desloca y em funcao de x)
    """
    return [[  1, shx, 0],
            [shy,   1, 0],
            [  0,   0, 1]]
