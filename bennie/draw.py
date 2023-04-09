import pygame

BLACK = pygame.Color('black')


def draw_cell(rect, cell, palette, maxdepth):
    colors = len(palette)
    surface = pygame.Surface(rect.size)

    for y in range(rect.height):
        for x in range(rect.width):
            it = cell[y][x][0]
            col = BLACK if it == maxdepth else pygame.Color(palette[int(it * colors / maxdepth)])
            pygame.draw.line(surface, col, (x, y), (x + 1, y))

    return surface
