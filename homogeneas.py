import math


def identidade():
    return [[1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]]


def mat_mult(A, B):
    C = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                C[i][j] += A[i][k] * B[k][j]
    return C


def aplicar_ponto(M, x, y):
    xn = M[0][0] * x + M[0][1] * y + M[0][2]
    yn = M[1][0] * x + M[1][1] * y + M[1][2]
    w  = M[2][0] * x + M[2][1] * y + M[2][2]
    if w == 0:
        raise ValueError("Coordenada homogenea w == 0 (transformacao invalida).")
    return xn / w, yn / w


def aplicar_transformacao(vertices, M):
    return [aplicar_ponto(M, x, y) for x, y in vertices]


def poligono_regular(n, raio):

    offset = math.pi / n if n % 2 == 0 else math.pi / 2
    vertices = []
    for k in range(n):
        angulo = offset + 2 * math.pi * k / n
        x = raio * math.cos(angulo)
        y = raio * math.sin(angulo)
        vertices.append((x, y))
    return vertices
