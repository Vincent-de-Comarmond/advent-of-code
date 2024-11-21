from copy import deepcopy
from operator import itemgetter
from typing import Dict, List, Set, Tuple


TEST = True

if TEST:
    _raw = [
        "R 6 (#70c710)",
        "D 5 (#0dc571)",
        "L 2 (#5713f0)",
        "D 2 (#d2c081)",
        "R 2 (#59c680)",
        "D 2 (#411b91)",
        "L 5 (#8ceee2)",
        "U 2 (#caa173)",
        "L 1 (#1b58a2)",
        "U 2 (#caa171)",
        "R 2 (#7807d2)",
        "U 3 (#a77fa3)",
        "L 2 (#015232)",
        "U 2 (#7a21e3)",
    ]

    _raw = [
        "U 2 (#7a21e3)",
        "L 2 (#015232)",
        "U 3 (#a77fa3)",
        "R 2 (#7807d2)",
        "U 2 (#caa171)",
        "L 1 (#1b58a2)",
        "U 2 (#caa173)",
        "L 5 (#8ceee2)",
        "D 2 (#411b91)",
        "R 2 (#59c680)",
        "D 2 (#d2c081)",
        "L 2 (#5713f0)",
        "D 5 (#0dc571)",
        "R 6 (#70c710)",
    ]


else:
    with open("./input.txt", "r") as txtin:
        _raw = [ln.strip() for ln in txtin]

DIRECTIONS = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}

DATA = [
    (DIRECTIONS[_[0]], int(_[1]), _[2].replace("(", "").replace(")", ""))
    for _ in map(lambda _str: _str.split(" "), _raw)
]


def t_add(*tuples: Tuple[int]) -> Tuple[int]:
    return tuple(
        (sum((t[idx] for t in tuples)) for idx in range(max(map(len, tuples))))
    )


def t_mult(tupl: tuple, scalar: int) -> tuple:
    return tuple(scalar * i for i in tupl)


def t_minus(*tuples: Tuple[int]) -> Tuple[int]:
    rest = t_add(*tuples[1:])
    return tuple(t - rest[idx] for idx, t in enumerate(tuples[0]))


def convert_coordinates(raw_data: List[tuple]) -> List[tuple]:
    mapping = {"0": "R", "1": "D", "2": "L", "3": "U"}

    output = []
    for _, _, code in raw_data:
        dir_code = mapping[code[-1]]
        distance = int(code[1:-1], 16)
        output.append((DIRECTIONS[dir_code], distance, ""))
        print((dir_code, distance, ""))
    return output


def determine_quads(converted_coordinates: List[tuple]):
    quad_cache = set()
    area_cache = set()

    point0 = (0, 0)
    point1 = (0, 0)
    point2 = (0, 0)
    point3 = (0, 0)

    for idx in range(len(convert_coordinates), 2):
        prev_coords = converted_coordinates[idx - 1]
        coords = converted_coordinates[idx]
        next_coords = converted_coordinates[idx + 1]

        # Now ... protrusions can either be concave (collecting) or convex (excluding)

    for idx, direction, distance, _ in enumerate(converted_coordinates):
        next_coord = converted_coordinates[idx + 1]

    pass


def determine_path(
    data_input: List[tuple],
) -> List[Tuple[int]]:
    point = (0, 0)
    path = [point]
    for direction, distance, _ in data_input:
        for _ in range(distance):
            point = t_add(point, direction)
            path.append(point)

    return path


def create_grid(traversed_path: List[Tuple[int]]) -> List[List[str]]:
    row_min = min(map(itemgetter(0), traversed_path))
    row_max = max(map(itemgetter(0), traversed_path))
    col_min = min(map(itemgetter(1), traversed_path))
    col_max = max(map(itemgetter(1), traversed_path))

    return [
        ["#" if (i, j) in traversed_path else "." for j in range(col_min, col_max + 1)]
        for i in range(row_min, row_max + 1)
    ]


def determine_capacity(traversed_path: List[Tuple[int]]) -> Set[Tuple[int]]:
    row_min = min(map(itemgetter(0), traversed_path))
    row_max = max(map(itemgetter(0), traversed_path))
    col_min = min(map(itemgetter(1), traversed_path))
    col_max = max(map(itemgetter(1), traversed_path))

    right_hand = {(-1, 0): (0, 1), (0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0)}
    # left_hand = {(-1, 0): (0, -1), (0, 1): (-1, 0), (1, 0): (0, 1), (0, -1): (1, 0)}
    cut = {_ for _ in traversed_path}

    current_frac = -1

    path_length = len(traversed_path)

    for idx, point in enumerate(traversed_path[1:]):
        frac_comp = int(1000 * idx / path_length)
        if frac_comp != current_frac:
            current_frac = frac_comp
            print(f"Completed {current_frac/10} %")

        prev_pnt = traversed_path[idx]
        diff = (point[0] - prev_pnt[0], point[1] - prev_pnt[1])
        direction = right_hand[diff]

        # left_point = prev_pnt
        left_point = point

        if direction == (-1, 0):
            _range = range(left_point[0], row_min, -1)
        if direction == (0, 1):
            _range = range(left_point[1], col_max, 1)
        if direction == (1, 0):
            _range = range(left_point[0], row_max, 1)
        if direction == (0, -1):
            _range = range(left_point[1], col_min, -1)

        for _ in _range:
            if left_point is not None:
                left_point = t_add(left_point, direction)
                if left_point in traversed_path:
                    break
                cut.add(left_point)

    return cut


def print_grid(grid: List[[List[str]]]) -> None:
    print("\n".join(("".join(row) for row in grid)))


def fill_grid(
    grid: List[List[str]], cap: Set[Tuple[int]], path: List[Tuple[int]]
) -> None:
    grid_min = tuple(min(map(itemgetter(i), cap)) for i in (0, 1))
    path_len_tenth = len(path) // 10

    symbols = {(-1, 0): "^", (0, 1): ">", (1, 0): "v", (0, -1): "<"}

    for i, j in cap:
        adj_i, adj_j = i - grid_min[0], j - grid_min[1]
        try:
            idx = path.index((i, j))
            diff = t_minus(path[idx + 1], path[idx])
            symbol = symbols[diff]
            if idx <= path_len_tenth:
                grid[adj_i][adj_j] = f"\033[0;36m{symbol}\033[0m"
            else:
                grid[adj_i][adj_j] = f"\033[0;31m{symbol}\033[0m"
        except:
            grid[adj_i][adj_j] = "#"


determined_path = determine_path(convert_coordinates(DATA))
capacity = determine_capacity(determined_path)
created_grid = create_grid(determined_path)

# grid_copy = deepcopy(created_grid)
# fill_grid(created_grid, capacity, determined_path)
# print_grid(created_grid)
# for index, row in enumerate(grid):
#     grid_copy[index] = grid_copy[index] + row

# print_grid(grid_copy)

print(f"Capacity: {len(capacity)}")

# 52033 is too low
# 52054 is too low -  visual inspection tells me this is missing 1 point
# 52055
