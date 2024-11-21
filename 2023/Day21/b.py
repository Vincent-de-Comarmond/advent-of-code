from collections import defaultdict
from copy import deepcopy
import numpy as np
from typing import Dict, Tuple

TEST = True
STEPS_TO_TO_TAKE = 100 if TEST else 64

if TEST:
    _raw = [
        "...........",
        ".....###.#.",
        ".###.##..#.",
        "..#.#...#..",
        "....#.#....",
        ".##..S####.",
        ".##..#...#.",
        ".......##..",
        ".##.#.####.",
        ".##..##.##.",
        "...........",
    ]
else:
    with open("./input.txt", "r") as txtin:
        _raw = [ln.strip() for ln in txtin]

DATA = np.array([[_ for _ in row] for row in _raw])
NR, NC = DATA.shape
starting_point = tuple(map(int, np.where(DATA == "S")))

active = {starting_point: 0}
burnt = defaultdict(set)

while len(active) > 0:
    for k, v in deepcopy(active).items():
        burnt[k].add(v)
        _ = active.pop(k)

        for i, j in (-1, 0), (0, 1), (1, 0), (0, -1):
            point = (k[0] + i, k[1] + j)
            grid_point = (point[0] % NR, point[1] % NC)

            if DATA[*grid_point] == "#":
                continue

            if v + 1 > STEPS_TO_TO_TAKE:
                continue

            active[point] = v + 1

results = dict(filter(lambda _: STEPS_TO_TO_TAKE in _[1], burnt.items()))
print(len(results))
# 3600 is the right answer
