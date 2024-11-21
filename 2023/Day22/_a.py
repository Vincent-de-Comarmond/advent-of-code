from itertools import product
import numpy as np
from typing import List, Set

TEST = True

if TEST:
    _raw = [
        "1,0,1~1,2,1",
        "0,0,2~2,0,2",
        "0,2,3~2,2,3",
        "0,0,4~0,2,4",
        "2,0,5~2,2,5",
        "0,1,6~2,1,6",
        "1,1,8~1,1,9",
    ]
else:
    with open("./input.txt", "r") as txtin:
        _raw = [ln for ln in txtin]


def create_data(rawinput: List[str]):
    output = {}

    for idx, line in enumerate(rawinput):
        side1, side2 = line.split("~")
        point1 = tuple(map(int, side1.split(",")))
        point2 = tuple(map(int, side2.split(",")))
        tmp = {"lower": set(), "upper": set()}

        for i, j in product(
            range(point1[0], point2[0] + 1), range(point1[1], point2[1] + 1)
        ):
            tmp["lower"].add((i, j, min(point1[2], point2[2])))
            tmp["upper"].add((i, j, max(point1[2], point2[2])))
        output[idx] = tmp

    return output

def settle_bricks()



if False:

    def create_data(raw_input: List[str]) -> np.ndarray:
        bricks = list()

        max_x, max_y, max_z = -np.inf, -np.inf, -np.inf

        for row in raw_input:
            start, end = row.split("~")
            a, b, c = map(int, start.split(","))
            d, e, f = map(int, end.split(","))

            max_x, max_y, max_z = max(a, d, max_x), max(b, e, max_y), max(c, f, max_z)
            bricks.append(((a, d), (b, e), (c, f)))

        dataset = np.full((max_x + 1, max_y + 1, max_z + 1), np.nan)
        for idx, brick in enumerate(bricks):
            for i in range(min(brick[0]), max(brick[0]) + 1):
                for j in range(min(brick[1]), max(brick[1]) + 1):
                    for k in range(min(brick[2]), max(brick[2]) + 1):
                        dataset[i, j, k] = idx + 1
        return dataset

    def settle_bricks(grid: np.ndarray, idx: int = 1) -> np.ndarray:
        last = idx == grid.shape[2] - 1

        if all(np.isnan(grid[:, :, idx]).ravel()):
            layer_removed = np.delete(grid, idx, axis=2)

            if last:
                return layer_removed
            return settle_bricks(layer_removed, idx)

        if last:
            return grid
        return settle_bricks(grid, idx + 1)

    def what_can_i_remove(settled_grid: np.ndarray) -> Set[int]:
        pass
