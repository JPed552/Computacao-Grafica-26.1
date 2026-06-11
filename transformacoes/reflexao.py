from homogeneas import identidade

# Reflexao — espelha o objeto em relacao ao eixo ou ponto indicado.
#   'x'      → inverte Y (espelha em relacao ao eixo X)
#   'y'      → inverte X (espelha em relacao ao eixo Y)
#   'origem' → inverte X e Y (espelha em relacao a origem)
#   'y=x'    → troca X e Y (espelha em relacao a reta y = x)
def reflexao(eixo):
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
