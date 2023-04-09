import pygame

from enum import Enum, auto
from random import choice

from cooldown import Cooldown
from pygamehelpers import GameState

from bennie.globals import X0, Y0, X1, Y1, MAXDEPTH, CELLSIZE, DEFAULT_PALETTE, States


a2b = lambda a, b, x: x * b / a


class Mode(Enum):
    CROSSHAIR = auto()
    DRAGGING = auto()
    SELECTED = auto()
    CONFIRM = auto()
    CONFIRMED = auto()


class SelectFrame(GameState):
    def __init__(self, persist):
        super().__init__(persist)

        self.crosshair = None
        self.crosshair_cooldown = Cooldown(3)
        self.selection = None
        self.drag_to = None
        self.mode = None
        self.aspect = persist.rect.width / persist.rect.height
        self.inverse = None

        self.font = pygame.Font(None, 14)

    def reset(self, persist=None):
        super().reset(persist)
        self.crosshair = self.persist.rect.center
        self.crosshair_cooldown.reset()
        self.selection = self.persist.rect.copy()
        self.mode = Mode.CROSSHAIR

    def reset_hard(self):
        self.persist.frame = (X0, Y0, X1, Y1)
        self.persist.maxdepth = MAXDEPTH
        self.persist.cellsize = CELLSIZE

        self.persist.palette = self.persist.palettes[DEFAULT_PALETTE]
        self.persist.colors = len(self.persist.palette)

    def dispatch_event(self, e):
        super().dispatch_event(e)
        match(e.type):
            case pygame.MOUSEMOTION:
                if self.mode == Mode.CROSSHAIR:
                    self.crosshair_cooldown.reset()
                    self.selection.center = e.pos
                elif self.mode == Mode.DRAGGING:
                    self.drag_to = e.pos

            case pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if self.mode == Mode.CONFIRM:
                        if self.selection.collidepoint(e.pos):
                            self.mode = Mode.CONFIRMED
                        else:
                            self.mode = Mode.CROSSHAIR
                    elif self.mode == Mode.CROSSHAIR:
                        self.mode = Mode.DRAGGING
                        self.selection.width = self.selection.height = 1
                        self.selection.center = self.drag_to = e.pos
                elif e.button == 3:
                    self.mode = Mode.CROSSHAIR
                    self.selection.center = e.pos

            case pygame.MOUSEBUTTONUP:
                if self.mode == Mode.DRAGGING and e.button == 1:
                    self.mode = Mode.SELECTED

            case pygame.KEYDOWN:
                match e.key:
                    case pygame.K_p:
                        self.persist.palette = choice(list(self.persist.palettes.values()))
                        self.persist.colors = len(self.persist.palette)
                        self.next_state = States.RERENDER
                    case pygame.K_s:
                        self.persist.old_maxdepth = self.persist.maxdepth
                        self.persist.maxdepth *= 2
                        self.next_state = States.SHARPEN
                    case pygame.K_r:
                        self.reset_hard()
                        self.next_state = States.RENDER

    def screen2frame(self, rect):
        fx0, fy0 = self.persist.frame[0:2]

        fw = self.persist.frame[2] - self.persist.frame[0]
        fh = self.persist.frame[3] - self.persist.frame[1]

        sw = self.persist.rect.width
        sh = self.persist.rect.height

        x0 = a2b(sw, fw, rect.left) + fx0
        y0 = a2b(sh, fh, rect.top) + fy0
        x1 = a2b(sw, fw, rect.right) + fx0
        y1 = a2b(sh, fh, rect.bottom) + fy0

        return (x0, y0, x1, y1)

    def update(self, dt):
        # Nothing to do here, code for future use...
        match(self.mode):
            case Mode.CROSSHAIR:
                # Nothing to do here
                pass

            case Mode.DRAGGING:
                x0, y0 = self.selection.center
                x1, y1 = self.drag_to

                delta = max(x1 - x0, y1 - y0)

                # Changing width/height is relative to top left corner, so save center
                # and restore it after setting the new dimensions
                center = self.selection.center
                self.selection.width = 2 * delta
                self.selection.height = 2 * delta * self.aspect
                self.selection.center = center

            case Mode.SELECTED:
                self.selection.clamp_ip(self.persist.rect)
                self.inverse = pygame.transform.invert(self.persist.canvas.subsurface(self.selection))
                self.mode = Mode.CONFIRM

            case Mode.CONFIRM:
                # Nothing to do here
                pass

            case Mode.CONFIRMED:

                self.next_state = States.RENDER

                self.persist.frame = self.screen2frame(self.selection)
                self.next_state = States.RENDER

    def draw(self, screen):
        screen.blit(self.persist.canvas, (0, 0))

        match(self.mode):
            case Mode.CROSSHAIR:
                if not self.crosshair_cooldown.cold:
                    mx, my = self.selection.center
                    pygame.draw.line(screen, pygame.Color('green'),
                                     (mx, self.persist.rect.top),
                                     (mx, self.persist.rect.bottom))
                    pygame.draw.line(screen, pygame.Color('green'),
                                     (self.persist.rect.left, my),
                                     (self.persist.rect.right, my))
                    screen.blit(self.text(f'{self.selection.center}'), (5, 5))
                    x = a2b(self.persist.rect.width,
                            self.persist.frame[2] - self.persist.frame[0],
                            mx) + self.persist.frame[0]
                    y = a2b(self.persist.rect.height,
                            self.persist.frame[3] - self.persist.frame[1],
                            my) + self.persist.frame[1]
                    screen.blit(self.text(f'{x, y}'), (5, 5 + self.font.get_height()))
                    screen.blit(self.text(f'{self.persist.frame}'), (5, 5 + 2 * self.font.get_height()))

            case Mode.DRAGGING:
                pygame.draw.rect(screen, pygame.Color('green'), self.selection, width=1)

            case Mode.SELECTED:
                pygame.draw.rect(screen, pygame.Color('blue'), self.selection)

            case Mode.CONFIRM:
                screen.blit(self.inverse, self.selection)

    def text(self, s):
        surf = self.font.render(s, True, pygame.Color('red'))
        return surf
