from collections import defaultdict
from copy import deepcopy
import numpy as np
from typing import Dict, Tuple

TEST = False
STEPS_TO_TO_TAKE = 6 if TEST else 64

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
steps_reported = set()

while len(active) > 0:
    for k, v in deepcopy(active).items():
        if v not in steps_reported:
            print(f"SteppedReached: {v}")
            steps_reported.add(v)

        burnt[k].add(v)
        _ = active.pop(k)

        for i, j in (-1, 0), (0, 1), (1, 0), (0, -1):
            point = (k[0] + i, k[1] + j)

            if point[0] < 0 or point[0] >= NR or point[1] < 0 or point[1] >= NC:
                continue

            if DATA[*point] == "#":
                continue

            if v + 1 > STEPS_TO_TO_TAKE:
                continue

            active[point] = v + 1

results = dict(filter(lambda _: STEPS_TO_TO_TAKE in _[1], burnt.items()))
print(len(results))
# 3600 is the right answer
