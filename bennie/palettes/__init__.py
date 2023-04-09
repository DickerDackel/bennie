import json
import importlib.resources
from os.path import basename, splitext
from itertools import cycle

palettes = {}

package = 'bennie.palettes'
for fname in importlib.resources.contents(package):
    if not fname.endswith('.json'):
        continue

    name = splitext(basename(fname))[0]
    data = importlib.resources.files(package).joinpath(fname).read_text()
    palettes[name] = json.loads(data)

palette_idx = cycle(palettes.keys())
