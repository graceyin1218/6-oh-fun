#!/usr/bin/env python
from lib601.util import line_indices
import sys
import os


def usage():
    print("Usage: %s world.py out.txt gx gy height width" %
          sys.argv[0], file=sys.stderr)
    sys.exit(1)


def point_to_indices(p1):
    global height, width
    x, y = p1
    state_width = (x1-x0) / width
    c = int((x-x0)/state_width)
    c = min(max(0, c), width-1)
    state_height = float(y1-y0) / height
    r = height - 1 - int((y-y0)/state_height)
    r = min(max(0, r), height-1)
    return (r, c)


def dimensions(x, y):
    global x0, y0, x1, y1
    x0 = 0
    y0 = 0
    x1 = x
    y1 = y


def wall(p1, p2):
    global grid
    c1, c2 = point_to_indices(p1), point_to_indices(p2)
    indices = line_indices(c1, c2)
    for (r, c) in indices:
        grid[r][c] = '#'


def initialRobotLoc(x, y):
    r, c = point_to_indices((x, y))
    grid[r][c] = 'S'


def get_maze_text(soar_world_loc, goal, _height, _width):
    global grid, height, width
    height = _height
    width = _width
    grid = [['.' for c in range(width)] for r in range(height)]
    for r in range(height):
        grid[r][0] = '#'
        grid[r][-1] = '#'
    for c in range(width):
        grid[0][c] = '#'
        grid[-1][c] = '#'

    with open(soar_world_loc) as w:
        code = compile(w.read(), soar_world_loc, 'exec')
        exec(code)

    r, c = point_to_indices(goal)
    grid[r][c] = 'G'
    for r, row in enumerate(grid):
        grid[r] = ''.join(row)

    return grid

if __name__ == "__main__":
    if len(sys.argv) != 7 or \
       not os.path.exists(sys.argv[1]):
        usage()

    try:
        f = open(sys.argv[2], 'w')
    except FileNotFoundError:
        print("Unable to open output maze file", file=sys.stderr)
        usage()

    try:
        gx = float(sys.argv[3])
        gy = float(sys.argv[4])
    except ValueError:
        print("Invalid goal coordinates", file=sys.stderr)
        usage()
    goal = (gx, gy)

    try:
        height = int(sys.argv[5])
        width = int(sys.argv[6])
    except ValueError:
        print("Invalid height and width (must be integers)", file=sys.stderr)
        usage()

    grid = get_maze_text(sys.argv[1], goal, height, width)
    print('\n'.join(grid), file=f)
    f.close()
