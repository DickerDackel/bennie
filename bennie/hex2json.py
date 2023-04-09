import sys
import argparse
import json

cmdline = argparse.ArgumentParser(description='Convert lospec.com hex palettes to rgb tuples in json')
cmdline.add_argument('hex', type=str, help='hex palette filename')
cmdline.add_argument('json', type=str, nargs='?', help='json filename')
opts = cmdline.parse_args(sys.argv[1:])

def main():
    palette = []
    with open(opts.hex) as f:
        for l in [_.strip() for _ in f]:
            r, g, b = int(l[0:2], 16), int(l[2:4], 16), int(l[4:], 16)
            palette.append((r, g, b))
    if opts.json:
        with open(opts.json, 'w') as f:
            json.dump(palette, f)
    else:
        print(json.dumps(palette))
