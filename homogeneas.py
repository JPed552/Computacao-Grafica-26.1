import math


# Matriz identidade 3x3 — transformacao neutra (nao altera o ponto).
def identidade():
    return [[1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]]


# Multiplicacao de duas matrizes 3x3 — usada para compor transformacoes.
def mat_mult(A, B):
    C = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                C[i][j] += A[i][k] * B[k][j]
    return C


# Aplica a matriz homogenea M ao ponto (x, y).
# Representa o ponto como [x, y, 1], multiplica por M e divide por w.
def aplicar_ponto(M, x, y):
    xn = M[0][0] * x + M[0][1] * y + M[0][2]
    yn = M[1][0] * x + M[1][1] * y + M[1][2]
    w  = M[2][0] * x + M[2][1] * y + M[2][2]
    if w == 0:
        raise ValueError("Coordenada homogenea w == 0 (transformacao invalida).")
    return xn / w, yn / w


# Aplica M a todos os vertices da lista. Retorna lista de pontos transformados.
def aplicar_transformacao(vertices, M):
    return [aplicar_ponto(M, x, y) for x, y in vertices]


# Gera os n vertices de um poligono regular centrado na origem.
# n par  → lados horizontais/verticais (ex: quadrado reto, hexagono plano).
# n impar → vertice no topo (ex: triangulo apontando para cima).
def poligono_regular(n, raio):
    offset = math.pi / n if n % 2 == 0 else math.pi / 2
    vertices = []
    for k in range(n):
        angulo = offset + 2 * math.pi * k / n
        x = raio * math.cos(angulo)
        y = raio * math.sin(angulo)
        vertices.append((x, y))
    return vertices
