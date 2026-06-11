# Translacao T(tx, ty) — desloca o objeto (tx, ty) unidades nos eixos X e Y.
# tx e ty ficam na ultima coluna, que e onde a translacao aparece em coord. homogeneas.
def translacao(tx, ty):
    return [[1, 0, tx],
            [0, 1, ty],
            [0, 0,  1]]
