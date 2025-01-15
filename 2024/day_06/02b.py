# stdlib
from collections import defaultdict
from functools import lru_cache
from typing import Any, Dict, Optional, Set, Tuple

# 3rd party
import numpy as np


@lru_cache
def get_grid_and_start(path: str) -> np.ndarray:
    grid = list()
    with open(path, "r") as flin:
        for ln in flin:
            grid.append([char for char in ln if char != "\n"])
            if "^" in ln:
                start = len(grid) - 1, ln.index("^")
    return np.array(grid), start


def get_bounce(grid, y, x, direction) -> Optional[Tuple[int, ...]]:

    travels = {
        0: lambda: grid[:y, x],
        1: lambda: grid[y, x:],
        2: lambda: grid[y:, x],
        3: lambda: grid[y, :x],
    }
    travel = travels[direction]()
    bounce = np.where((travel == "#") | (travel == "O"))[0]
    # First or last depending on whether we're travlling in an increasing or decreasing direction
    # bounce = bounce[0] if direction in (1, 2) else bounce[-1]
    if len(bounce) == 0:
        return None
    bounce = int(bounce[0]) if direction in (1, 2) else int(bounce[-1])

    new_starts = {
        0: lambda: (bounce + 1, x),
        1: lambda: (y, x + bounce - 1),
        2: lambda: (y + bounce - 1, x),
        3: lambda: (y, bounce + 1),
    }
    return *new_starts[direction](), (direction + 1) % 4


def get_bounce_history(
    grid, start_y, start_x, start_dir=0, accum: Optional[defaultdict] = None
) -> Dict[dict, Any]:

    if accum is None:
        accum = defaultdict(int)

    bounce = get_bounce(grid, start_y, start_x, start_dir)
    if bounce in accum:
        return "Loop"

    if bounce is None:
        return dict(accum)

    accum[bounce] += 1
    return get_bounce_history(grid, *bounce, accum)


def get_loop_locations(grid, start_y, start_x, start_dir=0) -> Set[Tuple[int, ...]]:

    loop_locations = set()
    for j in range(grid.shape[0]):
        print(f"Doing row {j+1} of {grid.shape[0]}")
        for i in range(grid.shape[1]):
            if grid[j, i] != ".":
                continue
            grid[j, i] = "O"
            bounce_history = get_bounce_history(grid, start_y, start_x, start_dir)
            if bounce_history == "Loop":
                loop_locations.add((j, i))
            grid[j, i] = "."
    return loop_locations


if __name__ == "__main__":
    grid, start = get_grid_and_start("./input.txt")
    loop_locations = get_loop_locations(grid, *start, 0)
    print(len(loop_locations))

# 1527 -  answer is too low
# 1686 is the right answer
