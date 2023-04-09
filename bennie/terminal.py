import sys

from bennie.mandelbrot import iterate, process_cell
from bennie.globals import X0, Y0, X1, Y1, MAXDEPTH

def main():
    black, *palette = list(' .:-+=|/*X#%')
    colors = len(palette)
    MAXDEPTH = 25

    screen_width = 80
    screen_height = 40

    x0, y0 = X0, Y0
    x1, y1 = X1, Y1
    dx = (x1 - x0) / screen_width
    dy = (y1 - y0) / screen_height

    cell = process_cell(x0, y0, dx, dy, screen_width, screen_height, MAXDEPTH)
    for y in range(screen_height):
        for x in range(screen_width):
            iters = cell[y][x]
            c = black if iters == MAXDEPTH else palette[int(iters * colors / MAXDEPTH)]
            print(c, end='')
        print()

if __name__ == '__main__':
    main()
