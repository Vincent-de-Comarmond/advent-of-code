from functools import lru_cache
import numpy as np
import mathplotlib.pyplot as plt

# Rocks roll NWSE


TEST = True
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


@lru_cache(maxsize=None)
def switch(_array: np.ndarray, idx: int, _dir: str) -> int:
    if _dir in ("n", "w"):
        if idx < 0:
            return idx + 1

        if _array[idx] == "." and _array[idx + 1] == "O":
            _array[idx] = "O"
            _array[idx + 1] = "."
            return idx - 1
        return idx + 1

    if idx > len(_array) - 1:
        return idx - 1
    # Else
    if _array[idx] == "." and _array[idx - 1] == "O":
        _array[idx - 1] = "."
        _array[idx] = "O"
        return idx + 1
    return idx - 1


@lru_cache(maxsize=None)
def cycle(_in: np.ndarray, _dir: str) -> None:

    if _dir in ("n", "s"):
        for col_idx in range(_in.shape[1]):
            col = _in[:, col_idx]
            if _dir == "n":
                idx = 0
                while idx < _in.shape[1] - 1:
                    idx = switch(col, idx, "n")
            else:
                idx = _in.shape[1] - 1
                while idx > 0:
                    idx = switch(col, idx, "s")
    else:
        for row_idx in range(_in.shape[0]):
            row = _in[row_idx, :]
            if _dir == "w":
                idx = 0
                while idx < _in.shape[0] - 1:
                    idx = switch(row, idx, "w")
            else:
                idx = _in.shape[0] - 1
                while idx > 0:
                    idx = switch(row, idx, "e")

    if PRINT:
        print(f"Results of direction: {_dir}")
        print(_in)

    return (
        cycle(_in, "w")
        if _dir == "n"
        else cycle(_in, "s")
        if _dir == "w"
        else cycle(_in, "e")
        if _dir == "s"
        else None
    )


def calculate_load(_in: np.ndarray) -> int:
    total = 0
    for col_idx in range(_in.shape[1]):
        col = _in[:, col_idx]

        for idx, char in enumerate(col):
            if char == "O":
                total += _in.shape[0] - idx
    return total


# Part a: 105982 is correct

before = data.copy()

loads = []
for count in range(1000000000):
    if count % 100000 == 0:
        print(f"Cycle number: {count}")
    cycle(data, "n")
    loads.append(calculate_load(data))
load = calculate_load(data)
print(load)
