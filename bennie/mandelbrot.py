def iterate(c, maxdepth, i0=0, z0=complex(0.0, 0.0)):
    z = z0
    for i in range(i0, maxdepth):
        if abs(z) > 2:
            return i, z
        z = z * z + c

    return i+1, z

def process_cell(x0, y0, w, h, maxdepth, steps, cache=None):
    cell = []
    cy = y0
    for y in range(steps):
        row = []
        cx = x0
        for x in range(steps):
            if cache:
                row.append(iterate(complex(cx, cy), maxdepth, *cache[y][x]))
            else:
                row.append(iterate(complex(cx, cy), maxdepth))
            cx += w
        cell.append(row)
        cy += h

    return cell
