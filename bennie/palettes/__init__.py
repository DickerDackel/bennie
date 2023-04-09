import json
import importlib.resources
from os.path import basename, splitext

palettes = {}

print(__name__)
package = 'bennie.palettes'
for fname in importlib.resources.contents(package):
    if not fname.endswith('.json'):
        continue

    name = splitext(basename(fname))[0]
    data = importlib.resources.files(package).joinpath(fname).read_text()
    palettes[name] = json.loads(data)
