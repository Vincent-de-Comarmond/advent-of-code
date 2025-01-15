from sys import argv

# 3rd party
import numpy as np


def load_input(txt_file: str) -> tuple[np.ndarray, list[str]]:
    are_instructions = False
    warehouse: list[list[int]] = []
    instructions: list[str] = []

    dir_mapper = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
    # icon_mapper = {"#": -1, ".": 0, "O": 1, "@": 2}

    with open(txt_file, "r") as txtin:
        for line in txtin:
            cleanline = [_ for _ in line if _ != "\n"]
            if len(cleanline) == 0:
                are_instructions = True
                continue

            if are_instructions:
                instructions.extend(map(dir_mapper.get, cleanline))
            else:
                warehouse.append(cleanline)

    return np.array(warehouse), instructions


def get_location(warehouse: np.ndarray) -> tuple[np.int64]:
    return tuple(map(lambda _: _[0], np.where(warehouse == "@")))


def move(
    warehouse: np.ndarray, location: tuple[np.int64], direction: tuple[int]
) -> tuple[np.ndarray, tuple[np.int64]]:

    i, j = location
    projections = {
        (-1, 0): lambda: warehouse[:i, j],
        (0, -1): lambda: warehouse[i, :j],
        (1, 0): lambda: warehouse[i + 1 :, j],
        (0, 1): lambda: warehouse[i, j + 1 :],
    }
    row_or_col = projections[direction]()

    is_decreasing = min(direction) == -1
    is_open = np.where(row_or_col == ".")[0]
    is_blocked = np.where(row_or_col == "#")[0]

    if len(is_open) == 0:
        return warehouse, location

    if is_decreasing:
        next_open, next_blocked = is_open.max(), is_blocked.max()
        if next_open < next_blocked:
            return warehouse, location
    else:
        next_open, next_blocked = is_open.min() + 1, is_blocked.min() + 1
        if next_blocked < next_open:
            return warehouse, location

    new_loc = np.add(location, direction)
    warehouse[location[0], location[1]] = "."
    warehouse[new_loc[0], new_loc[1]] = "@"

    match direction:
        case (-1, 0):
            warehouse[next_open : new_loc[0], j] = "O"
        case (0, -1):
            warehouse[i, next_open : new_loc[1]] = "O"
        case (1, 0):
            warehouse[new_loc[0] + 1 : new_loc[0] + next_open, j] = "O"
        case (0, 1):
            warehouse[i, new_loc[1] + 1 : new_loc[1] + next_open] = "O"

    return warehouse, new_loc


def get_gps_sum(warehouse: np.ndarray) -> int:
    return sum(map(lambda _: 100 * _[0] + _[1], zip(*np.where(warehouse == "O"))))


def main(file_path: str):
    warehouse, instructions = load_input(file_path)
    location = get_location(warehouse)

    for instruction in instructions:
        warehouse, location = move(warehouse, location, instruction)
    print(get_gps_sum(warehouse))
    return get_gps_sum

if __name__ == "__main__":
    main(argv[1])
    # 1563092 is the right answer for part 1
