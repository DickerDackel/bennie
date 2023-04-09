import queue
import random
import pygame

from pygamehelpers import GameState

from bennie.globals import X0, Y0, X1, Y1, MAXDEPTH, CELLSIZE, DEFAULT_PALETTE, States
from bennie.draw import draw_cell
from .render import create_orders

WHITE = pygame.Color('white')


class Sharpen(GameState):
    def __init__(self, persist):
        super().__init__(persist)

        self.qi, self.qo = self.persist.queues

    def reset(self, persist=None):
        super().reset(persist)
        self.persist.canvas.fill(WHITE)
        pygame.time.set_timer(pygame.USEREVENT, 1000 // 60)

    def dispatch_events(self):
        for e in pygame.event.get():
            self.dispatch_event(e)

    def dispatch_event(self, e):
        match e.type:
            case pygame.USEREVENT:
                self._draw()

    def render_frame(self):
        canvas = self.persist.canvas
        canvas.fill(WHITE)
        self._draw()
        pygame.display.flip()


        def reorder_cache(cache, x0, y0, x1, y1, maxdepth, cellsize, rect, shuffle=True):
            dx = (x1 - x0) / rect.width
            dy = (y1 - y0) / rect.height

            return [(x, y, x0 + x * dx, y0 + y * dy, dx, dy, maxdepth, cellsize, cell)
                    for x, y, cell in cache]

        orders = reorder_cache(self.persist.cache, *self.persist.frame,
                               self.persist.maxdepth, self.persist.cellsize,
                               self.persist.rect, shuffle=True)

        def has_black(cell, maxdepth):
            for row in cell:
                for i, z in row:
                    if i == maxdepth and abs(z) <= 2:
                        return True
            return False

        for o, c in zip(orders, self.persist.cache):
            x, y, cell = c
            if has_black(cell, self.persist.old_maxdepth):
                self.qi.put(o)
                pygame.draw.rect(canvas, pygame.Color('red'),
                                 (x, y, self.persist.cellsize + 1, self.persist.cellsize + 1),
                                 width=1)
            else:
                self.qo.put(c)
                pygame.draw.rect(canvas, pygame.Color('green'),
                                 (x, y, self.persist.cellsize + 1, self.persist.cellsize + 1),
                                 width=1)


        self.persist.cache = []
        todo = len(orders)
        while todo:
            self.dispatch_events()

            try:
                x, y, cell = self.qo.get(timeout=5)
            except queue.Empty:
                continue
            self.qo.task_done()
            todo -= 1
            self.persist.cache.append((x, y, cell))

            r = pygame.Rect(x, y, self.persist.cellsize, self.persist.cellsize)
            surf = draw_cell(r, cell, self.persist.palette, self.persist.maxdepth)
            canvas.blit(surf, r)

    def update(self, dt):
        self.render_frame()
        self.next_state = States.SELECT_FRAME

    # Draw and flip outside the main loop
    def _draw(self):
        self.draw(self.persist.screen)
        pygame.display.flip()

    def draw(self, screen):
        screen.blit(self.persist.canvas, (0, 0))
