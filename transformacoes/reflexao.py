from homogeneas import identidade


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
