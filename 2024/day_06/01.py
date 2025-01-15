from sys import argv
from sys import setrecursionlimit

setrecursionlimit(15000)

grid = dict()

with open(argv[1], "r") as flin:
    for y, ln in enumerate(flin):
        for x, char in filter(lambda _: _[1] != "\n", enumerate(ln)):
            grid[y, x] = char
            if char == "^":
                start = y, x


def step(y, x, direction):
    grid[y, x] = "X"
    for k in range(4):
        direction = (direction + k) % 4
        dx = 1 if direction == 1 else -1 if direction == 3 else 0
        dy = -1 if direction == 0 else 1 if direction == 2 else 0
        if (y + dy, x + dx) not in grid:
            return
        if grid[y + dy, x + dx] != "#":
            return step(y + dy, x + dx, direction)



        
step(*start, 0)
print(len([_ for _ in grid.values() if _ == "X"]))
