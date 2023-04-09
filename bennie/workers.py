import threading
import queue

from bennie.mandelbrot import process_cell
from bennie.globals import THREADS

qi = queue.Queue()
qo = queue.Queue()

finished = threading.Event()

def worker():
    self = threading.get_ident()

    while not finished.is_set():
        try:
            celldef = qi.get(timeout=1)
        except queue.Empty:
            continue
        x, y, cx, cy, dx, dy, size, maxdepth = celldef
        cell = process_cell(cx, cy, dx, dy, size, size, maxdepth)
        qo.put((x, y, cell))
        qi.task_done()

threads = [threading.Thread(target=worker, daemon=True).start()
           for i in range(THREADS)]
