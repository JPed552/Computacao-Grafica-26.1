def dda(x1, y1, x2, y2, set_pixel, log):
    dx = x2 - x1                          
    dy = y2 - y1                    
    comprimento = max(abs(dx), abs(dy))   

    log("DDA")
    log(f"P1=({x1},{y1})  P2=({x2},{y2})")

    if comprimento == 0:
        set_pixel(x1, y1)
        return

    x_inc = dx / comprimento   # (x2 - x1) / L
    y_inc = dy / comprimento   # (y2 - y1) / L
    log(f"x_inc={x_inc:.2f}  y_inc={y_inc:.2f}\n")

    x, y = float(x1), float(y1)
    set_pixel(x, y)
    log(f"  ({round(x)}, {round(y)})")

    for _ in range(comprimento):
        x += x_inc
        y += y_inc
        set_pixel(x, y)
        log(f"  ({round(x)}, {round(y)})")