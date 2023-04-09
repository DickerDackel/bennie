import queue
import random
import pygame

from pygamehelpers import GameState

from bennie.globals import X0, Y0, X1, Y1, MAXDEPTH, CELLSIZE, DEFAULT_PALETTE, States
from bennie.mandelbrot import process_cell

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


def create_orders(x0, y0, x1, y1, maxdepth, cellsize, rect, shuffle=True):
    dx = (x1 - x0) / rect.width
    dy = (y1 - y0) / rect.height

    orders = [(x, y, x0 + x * dx, y0 + y * dy, dx, dy, cellsize, maxdepth)
              for y in range(0, rect.width, cellsize)
              for x in range(0, rect.height, cellsize)]

    if shuffle:
        random.shuffle(orders)

    return orders


def draw_cell(rect, cell, palette, maxdepth):
    colors = len(palette)
    surface = pygame.Surface(rect.size)

    for y in range(rect.height):
        for x in range(rect.width):
            it = cell[y][x]
            col = BLACK if it == maxdepth else pygame.Color(palette[int(it * colors / maxdepth)])
            pygame.draw.line(surface, col, (x, y), (x + 1, y))
    sr = surface.get_rect()
    return surface


class Render(GameState):
    def __init__(self, persist):
        super().__init__(persist)

        self.qi, self.qo = self.persist.queues

        self.reset_hard()

    def reset(self, persist=None):
        super().reset(persist)
        self.persist.canvas.fill(WHITE)

    # The render module is called after each selection
    def reset_hard(self):
        self.persist.frame = (X0, Y0, X1, Y1)
        self.persist.maxdepth = MAXDEPTH
        self.persist.cellsize = CELLSIZE

        self.persist.palette = self.persist.palettes[DEFAULT_PALETTE]
        self.persist.colors = len(self.persist.palette)

    def render_frame(self):
        canvas = self.persist.canvas
        canvas.fill(WHITE)
        self._draw()
        pygame.display.flip()

        orders = create_orders(*self.persist.frame, self.persist.maxdepth,
                               self.persist.cellsize, self.persist.rect,
                               shuffle=True)
        for o in orders:
            self.qi.put(o)

            # FIXME debugging
            x, y = o[0:2]
            pygame.draw.rect(canvas, pygame.Color('red'),
                             (x, y, self.persist.cellsize + 1, self.persist.cellsize + 1),
                             width=1)
        self._draw()
        pygame.display.flip()

        todo = len(orders)
        while todo:
            pygame.event.pump()

            # if qi.empty() and qo.empty():
            #     break

            try:
                x, y, cell = self.qo.get(timeout=5)
            except queue.Empty:
                continue
            self.qo.task_done()
            todo -= 1

            r = pygame.Rect(x, y, self.persist.cellsize, self.persist.cellsize)
            surf = draw_cell(r, cell, self.persist.palette, self.persist.maxdepth)
            canvas.blit(surf, r)
            self._draw()
            pygame.display.flip()

    def update(self, dt):
        self.render_frame()
        self.next_state = States.SELECT_FRAME

    # Draw and flip outside the main loop
    def _draw(self):
        self.draw(self.persist.screen)
        pygame.display.flip()

    def draw(self, screen):
        screen.blit(self.persist.canvas, (0, 0))
