from collections import defaultdict
from json import dump
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

# Rocks roll NWSE


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
for count in range(5000):
    if count % 100000 == 0:
        print(f"Cycle number: {count}")
    cycle(data, "n")
    loads.append(calculate_load(data))

plt.plot(loads)
plt.show()

with open("./new_input.json", "w") as jsonout:
    dump(loads, jsonout)

###################################
# Figure out frequency/recurrence #
###################################


newdata = np.array(loads)
future_equal = newdata == newdata[500]  # Arbitrary
recurrence = np.where(future_equal)[0]
frequencies = {
    recurrence[idx] - recurrence[idx - 1] for idx in range(1, len(recurrence))
}

fundamental = next(iter(frequencies))

simple_map = defaultdict(set)
for idx, val in enumerate(newdata):
    if idx >= 500:
        simple_map[idx % fundamental].add(val)

pprint(simple_map)

# Total load after 1000000000 cycles
total_load = simple_map[1000000000 % fundamental]
pprint(total_load)

# 85192 - answer is too high
# - 1st attempt ... accidentally started indexing at 500 rather than 0
# 85155 - answer is too low
# - 0 index of module operation where index 0 is 1 cycle, which is modulo 0
# But counts as first attempt so should be modulo 1

normal_map = {k: next(iter(v)) for k, v in simple_map.items()}
sorted_map = sorted(normal_map.items(), key=lambda _: _[1])


binary_search_options = [
    (24, 85155),  # Done
    (13, 85157),
    (30, 85160),
    (23, 85175),  # Right answer because of zero indexing interpretations
    (6, 85178),
    (31, 85189),
    (14, 85192),  # Done
]
