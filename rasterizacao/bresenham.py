# Bresenham generalizado — rasteriza retas em todos os 8 octantes.
# Usa variavel de erro (err = dx - dy) para decidir o proximo pixel sem ponto flutuante.
# Utilizado para desenhar as arestas dos poligonos nas transformacoes geometricas.
def bresenham_geral(x0, y0, x1, y1, set_pixel, log=None):
    dx  = abs(x1 - x0)
    dy  = abs(y1 - y0)
    sx  = 1 if x0 < x1 else -1  # direcao em x
    sy  = 1 if y0 < y1 else -1  # direcao em y
    err = dx - dy

    while True:
        set_pixel(x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:   # avanca em x
            err -= dy
            x0  += sx
        if e2 < dx:    # avanca em y
            err += dx
            y0  += sy


# Bresenham restrito ao 1o octante (0 <= dy <= dx, direcao positiva).
# Versao educacional com log detalhado passo a passo.
def bresenham(x1, y1, x2, y2, set_pixel, log):
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1

    if dy < 0 or dy > dx or dx <= 0:
        log("ERRO: fora do 1 oitante.")
        return

    d     = 2 * dy - dx       # variavel de decisao inicial
    incE  = 2 * dy             # incremento ao mover para Leste
    incNE = 2 * (dy - dx)      # incremento ao mover para Nordeste

    log("Bresenham (1 oitante)")
    log(f"P1=({x1},{y1})  P2=({x2},{y2})")
    log(f"dx={dx}  dy={dy}")
    log(f"d_init={d}  incE={incE}  incNE={incNE}\n")

    x, y = x1, y1
    set_pixel(x, y)
    log(f"  inicio ({x},{y})")

    while x < x2:
        x += 1
        if d <= 0:
            d += incE
            mov = "E "
        else:
            d += incNE
            y += 1
            mov = "NE"
        set_pixel(x, y)
        log(f"  {mov} -> ({x},{y})  d={d}")
