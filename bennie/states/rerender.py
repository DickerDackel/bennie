import queue
import random
import pygame

from pygamehelpers import GameState

from bennie.globals import X0, Y0, X1, Y1, MAXDEPTH, CELLSIZE, DEFAULT_PALETTE, States
from bennie.mandelbrot import process_cell
from bennie.draw import draw_cell

WHITE = pygame.Color('white')


class Rerender(GameState):
    def __init__(self, persist):
        super().__init__(persist)

    def reset(self, persist=None):
        pygame.time.set_timer(pygame.USEREVENT, 1000 // 25)

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

        for x, y, cell in self.persist.cache:
            r = pygame.Rect(x, y, self.persist.cellsize, self.persist.cellsize)
            surf = draw_cell(r, cell, self.persist.palette, self.persist.maxdepth)
            canvas.blit(surf, r)
            for e in pygame.event.get():
                self.dispatch_event(e)

            # self._draw()
            # pygame.display.flip()

    def update(self, dt):
        self.render_frame()
        self.next_state = States.SELECT_FRAME

    # Draw and flip outside the main loop
    def _draw(self):
        self.draw(self.persist.screen)
        pygame.display.flip()

    def draw(self, screen):
        screen.blit(self.persist.canvas, (0, 0))
