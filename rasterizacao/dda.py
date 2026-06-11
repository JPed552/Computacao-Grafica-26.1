# Algoritmo DDA — rasteriza uma reta entre (x1,y1) e (x2,y2) usando ponto flutuante.
# Divide o segmento em L passos e incrementa x e y proporcionalmente a cada passo.
def dda(x1, y1, x2, y2, set_pixel, log):
    dx = x2 - x1
    dy = y2 - y1
    comprimento = max(abs(dx), abs(dy))  # numero de passos = maior variacao

    log("DDA")
    log(f"P1=({x1},{y1})  P2=({x2},{y2})")

    if comprimento == 0:
        set_pixel(x1, y1)
        return

    x_inc = dx / comprimento   # incremento por passo em x
    y_inc = dy / comprimento   # incremento por passo em y
    log(f"x_inc={x_inc:.2f}  y_inc={y_inc:.2f}\n")

    x, y = float(x1), float(y1)
    set_pixel(x, y)
    log(f"  ({round(x)}, {round(y)})")

    for _ in range(comprimento):
        x += x_inc
        y += y_inc
        set_pixel(x, y)
        log(f"  ({round(x)}, {round(y)})")
