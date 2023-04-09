from enum import Enum, auto
from types import SimpleNamespace


SCREEN_SIZE = (768, 768)
FPS = 60

X0, Y0 = -2, -1.5
X1, Y1 = 1, 1.5
MAXDEPTH = 50
CELLSIZE = 16

DEFAULT_PALETTE = 'greyscale'

THREADS = 10


class States(Enum):
    RENDER = auto()
    RERENDER = auto()
    SHARPEN = auto()
    SELECT_FRAME = auto()
    MENU = auto()
    DEMO = auto()


persist = SimpleNamespace(
    screen=None,
    canvas=None,
    queues=None,
    fps=FPS,
    rect=None,
    maxdepth=MAXDEPTH,
    old_maxdepth=MAXDEPTH,
    palettes=None,
    palette=None,
    colors=0,
    frame=(X0, Y0, X1, Y1),
    cellsize=CELLSIZE,
)
