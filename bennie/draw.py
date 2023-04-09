import pygame
from math import log

from bennie.utils import a2b

BLACK = pygame.Color('black')


def map_color_mod(it, palette, colors, maxdepth, min_i=0, max_i=None):
    interval = max_i - min_i

    if it == maxdepth:
        return BLACK
    else:
        c = int((it - min_i) % colors)
        return pygame.Color(palette[c])


def map_color_linear(it, palette, colors, maxdepth, min_i=0, max_i=None):
    interval = maxdepth

    if it == maxdepth:
        return BLACK
    else:
        c = int(a2b(interval, colors, it))
        return pygame.Color(palette[c])


def map_color_scaled(it, palette, colors, maxdepth, min_i=0, max_i=None):
    interval = max_i - min_i

    if it == maxdepth:
        return BLACK
    else:
        c = int(a2b(interval, colors, it - min_i))
        return pygame.Color(palette[c])


def map_color_sqrt(it, palette, colors, maxdepth, min_i=0, max_i=None):
    interval = max_i - min_i
    i_sqrt = interval ** 0.5
    colors -= 1

    if it == maxdepth:
        return BLACK
    else:
        c = colors - int(a2b(i_sqrt, colors, (max_i - it) ** 0.5))
        return pygame.Color(palette[c])


def map_color_log(it, palette, colors, maxdepth, min_i=0, max_i=None):
    interval = max_i - min_i
    i_log = log(interval)

    if it == maxdepth:
        return BLACK
    else:
        c = (colors - 1) - int(a2b(i_log, (colors - 1), log(max_i - it)))
        return pygame.Color(palette[c])


def draw_cell(rect, cell, palette, maxdepth, min_i=0, max_i=None):
    colors = len(palette)
    surface = pygame.Surface(rect.size)

    if max_i is None:
        max_i = maxdepth
    interval = max_i - min_i

    for y in range(rect.height):
        for x in range(rect.width):
            it = cell[y][x][0]

            col = map_color_scaled(it, palette, colors, maxdepth, min_i, max_i)
            #col = BLACK if it == maxdepth else pygame.Color(palette[int((it - min_i) * colors / interval)])
            pygame.draw.line(surface, col, (x, y), (x + 1, y))

    return surface
