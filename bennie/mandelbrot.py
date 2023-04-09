def iterate(c, maxdepth):
    z = complex(0.0, 0.0)
    for i in range(maxdepth):
        z = z * z + c
        if abs(z) > 2:
            return i
    return maxdepth


def process_cell(x0, y0, dx, dy, steps_x, steps_y, maxdepth):
    cell = []
    cy = y0
    for y in range(steps_y):
        row = []
        cx = x0
        for x in range(steps_x):
            row.append(iterate(complex(cx, cy), maxdepth))
            cx += dx
        cell.append(row)
        cy += dy

    return cell
