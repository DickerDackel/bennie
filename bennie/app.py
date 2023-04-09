import pygame

from pygamehelpers import App

from .globals import SCREEN_SIZE, FPS, DEFAULT_PALETTE, States, persist
from .states import Render, Rerender, Sharpen, PaletteSmoothing, SelectFrame, Menu, Demo
from .palettes import palettes, palette_idx
from .workers import qi, qo

pygame.init()
pygame.display.set_caption('Bennie')

# Many fields in persist are initialized when importing the globals module.
# These here are the ones that contain dynamically created runtime data.
persist.screen = pygame.display.set_mode(SCREEN_SIZE)
persist.canvas = persist.screen.copy()
persist.clock = pygame.time.Clock()
persist.rect = persist.screen.get_rect()
persist.palettes = palettes
persist.palette_idx = palette_idx
persist.palette = palettes[next(palette_idx)]
persist.colors = len(persist.palette)
persist.queues = (qi, qo)

states = {
    States.RENDER: Render(persist),
    States.RERENDER: Rerender(persist),
    States.SHARPEN: Sharpen(persist),
    States.PALETTE_SMOOTHING: PaletteSmoothing(persist),
    States.SELECT_FRAME: SelectFrame(persist),
    States.MENU: Menu(persist),
    States.DEMO: Demo(persist),
}


def main():
    app = App(persist.screen, persist.clock, persist.fps, states, States.RENDER)
    app.run()
