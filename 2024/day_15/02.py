# stdlib
from sys import argv

# 3rd party
import numpy as np


def load_input(txt_file: str) -> tuple[np.ndarray, list[str]]:
    are_instructions = False
    warehouse: list[list[int]] = []
    instructions: list[str] = []

    dir_mapper = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
    icon_mapper = {"#": "##", ".": "..", "O": "[]", "@": "@."}

    with open(txt_file, "r") as txtin:
        for line in txtin:
            cleanline = [_ for _ in line if _ != "\n"]
            if len(cleanline) == 0:
                are_instructions = True
                continue

            if are_instructions:
                instructions.extend(map(dir_mapper.get, cleanline))
            else:
                warehouse.append(
                    [_ for char in cleanline for _ in icon_mapper.get(char)]
                )

    return np.array(warehouse), instructions


def get_location(warehouse: np.ndarray) -> tuple[np.int64]:
    return tuple(map(lambda _: _[0], np.where(warehouse == "@")))


def move_leftright(
    warehouse: np.ndarray, location: tuple[np.int64], direction: tuple[int]
) -> tuple[np.ndarray, tuple[np.int64]]:
    i, j = location
    projections = {
        (0, -1): lambda: warehouse[i, :j],
        (0, 1): lambda: warehouse[i, j + 1 :],
    }
    row = projections[direction]()
    is_decreasing = min(direction) == -1
    is_open = np.where(row == ".")[0]
    is_blocked = np.where(row == "#")[0]

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

    if direction == (0, -1):
        for k in range(next_open, new_loc[1]):
            warehouse[i, k] = warehouse[i, k + 1]
    elif direction == (0, 1):
        for k in range(new_loc[1] + next_open - 1, new_loc[1], -1):
            warehouse[i, k] = warehouse[i, k - 1]

    warehouse[location[0], location[1]] = "."
    warehouse[new_loc[0], new_loc[1]] = "@"

    return warehouse, new_loc


def move_updown(
    warehouse: np.ndarray, location: tuple[np.int64], direction: tuple[int]
) -> tuple[np.ndarray, tuple[np.int64]]:
    k, j = location

    projections = {
        (-1, 0): lambda: warehouse[:k, j],
        (1, 0): lambda: warehouse[k + 1 :, j],
    }

    col = projections[direction]()

    new_loc = tuple(np.add(location, direction))
    active_edge = list()

    if warehouse[*new_loc] == "[":
        active_edge = [new_loc, (new_loc[0], new_loc[1] + 1)]
    elif warehouse[*new_loc] == "]":
        active_edge = [new_loc, (new_loc[0], new_loc[1] - 1)]

    tree = list()
    is_blocked = False
    while len(active_edge) > 0:
        if is_blocked:
            break
        tmp = list()

        for node in sorted(active_edge):
            tree.append(node)
            next_node = tuple(np.add(node, direction))

            match warehouse[*next_node]:
                case ".":
                    continue
                case "#":
                    is_blocked = True
                    break
                case "[":
                    tmp.extend([next_node, (next_node[0], next_node[1] + 1)])
                case "]":
                    tmp.extend([next_node, (next_node[0], next_node[1] - 1)])

        active_edge = tmp

    if is_blocked:
        return warehouse, location

    tree = sorted(set(tree))
    iterator = tree if direction == (-1, 0) else list(reversed(tree))

    for node in iterator:
        next_node = tuple(np.add(node, direction))
        warehouse[*next_node] = warehouse[*node]
        warehouse[*node] = "."

    if warehouse[*new_loc] == "#":
        return warehouse, location

    warehouse[*location] = "."
    warehouse[*new_loc] = "@"

    return warehouse, new_loc


def move(
    warehouse: np.ndarray, location: tuple[np.int64], direction: tuple[int]
) -> tuple[np.ndarray, tuple[np.int64]]:

    return (
        move_leftright(warehouse, location, direction)
        if direction == (0, -1) or direction == (0, 1)
        else move_updown(warehouse, location, direction)
    )


def get_gps_sum(warehouse: np.ndarray) -> int:
    return sum(map(lambda _: 100 * _[0] + _[1], zip(*np.where(warehouse == "["))))


def main(file_path: str):
    warehouse, instructions = load_input(file_path)
    location = get_location(warehouse)

    # print("\n".join(["".join([_ for _ in row]) for row in warehouse]))
    for instruction in instructions:
        warehouse, location = move(warehouse, location, instruction)
        # print(instruction)
        # print("\n".join(["".join([_ for _ in row]) for row in warehouse]))
    print(get_gps_sum(warehouse))
    return get_gps_sum


if __name__ == "__main__":
    main(argv[1])
    # 1563092 is the right answer for part 1
    # 1582688 is the right answer for part 2
