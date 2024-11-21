from functools import lru_cache
import numpy as np

# import matplotlib.pyplot as plt
from typing import Tuple

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
def switch(cheat: bytes, idx: int, _dir: str) -> Tuple[Tuple[str], int]:
    _array = np.frombuffer(cheat, dtype="<U1").copy()
    if _dir in ("n", "w"):
        if idx < 0:
            return _array, idx + 1

        if _array[idx] == "." and _array[idx + 1] == "O":
            try:
                _array[idx] = "O"
            except:
                from IPython import embed

                embed()
            _array[idx + 1] = "."
            return _array, idx - 1
        return _array, idx + 1

    if idx > len(_array) - 1:
        return _array, idx - 1
    # Else
    if _array[idx] == "." and _array[idx - 1] == "O":
        _array[idx - 1] = "."
        _array[idx] = "O"
        return _array, idx + 1
    return _array, idx - 1


@lru_cache(maxsize=None)
def cycle(cheat: bytes, _dir: str) -> None:
    _in = np.frombuffer(cheat, dtype="<U1").copy()
    _in.resize(10, 10)

    if _dir in ("n", "s"):
        for col_idx in range(_in.shape[1]):
            col = _in[:, col_idx]
            if _dir == "n":
                idx = 0
                while idx < _in.shape[1] - 1:
                    col, idx = switch(col.tobytes(), idx, "n")
            else:
                idx = _in.shape[1] - 1
                while idx > 0:
                    col, idx = switch(col.tobytes(), idx, "s")
            _in[:, col_idx] = col
    else:
        for row_idx in range(_in.shape[0]):
            row = _in[row_idx, :]
            if _dir == "w":
                idx = 0
                while idx < _in.shape[0] - 1:
                    row, idx = switch(row.tobytes(), idx, "w")
            else:
                idx = _in.shape[0] - 1
                while idx > 0:
                    row, idx = switch(row.tobytes(), idx, "e")
            _in[row_idx, :] = row
    if PRINT:
        print(f"Results of direction: {_dir}")
        print(_in)

    return (
        cycle(_in.tobytes(), "w")
        if _dir == "n"
        else cycle(_in.tobytes(), "s")
        if _dir == "w"
        else cycle(_in.tobytes(), "e")
        if _dir == "s"
        else _in
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
    if count % 1000000 == 0:
        print(f"Cycle number: {count}")
    cycle(data.tobytes(), "n")
    loads.append(calculate_load(data))
load = calculate_load(data)
print(load)
