from functools import partial
import numpy as np
from typing import List, Tuple


TEST = False
PRINT = False

raw = []
if TEST:
    raw = [
        "O....#....",
        "O.OO#....#",
        ".....##...",
        "OO.#O....O",
        ".O.....O#.",
        "O.#..O.#.#",
        "..O..#O..O",
        ".......O..",
        "#....###..",
        "#OO..#....",
    ]
else:
    with open("./input.txt", "r") as txtin:
        raw = [ln.strip() for ln in txtin]

data = np.array([[_ for _ in row] for row in raw])


def switch(column: np.ndarray, idx: int) -> int:
    if idx > 0 and idx < len(column):
        if column[idx] == "O":
            if column[idx - 1] == ".":
                column[idx - 1] = "O"
                column[idx] = "."
                return idx - 1
        return idx + 1
    return idx + 1


def tilt(_in: np.ndarray) -> None:

    if PRINT:
        print("Complete before:")
        print(_in)

    for col_idx in range(_in.shape[1]):
        col = _in[:, col_idx]
        if PRINT:
            print("Before")
            print(col)
        idx, attempts = 0, 10000
        while idx < len(col) and 0 < attempts:
            attempts -= 1
            idx = switch(col, idx)
        if PRINT:
            print("After")
            print(col)

    if PRINT:
        print("Complete after:")
        print(_in)


def calculate_load(_in: np.ndarray) -> int:
    total = 0
    for col_idx in range(_in.shape[1]):
        col = _in[:, col_idx]

        for idx, char in enumerate(col):
            if char == "O":
                total += _in.shape[0] - idx
    return total


tilt(data)
load = calculate_load(data)
print(load)
