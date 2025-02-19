# Stdlib
from sys import argv

# 3rd party
import numpy as np


def get_neighbours(grid: np.ndarray, point: tuple[int, int]) -> set[tuple[int, int]]:
    row, col = point
    neighbours = set()
    for r, c in [(row + 1, col), (row, col + 1), (row - 1, col), (row, col - 1)]:
        if r >= 0 and r < grid.shape[0] and c >= 0 and c < grid.shape[1]:
            if grid[r, c] == ".":
                neighbours.add((r, c))
    return neighbours


def solve(
    grid: np.ndarray,
    active: set[tuple[int, int]],
    burnt: set[tuple[int, int]],
    steps: int = 0,
) -> tuple[tuple[int, int], ...]:

    new_active = set()
    target = tuple(map(lambda _: _ - 1, grid.shape))

    for point in active:
        burnt.add(point)
        neighbours = get_neighbours(grid, point) - burnt

        if target in neighbours:
            return steps + 1

        for neighbour in neighbours:
            new_active.add(neighbour)

    return solve(grid, new_active, burnt, steps + 1)


if __name__ == "__main__":
    SIZE = int(argv[1]) + 1
    FILE_PATH = argv[2]
    BYTES_FALLEN = int(argv[3])
    GRID = np.full((SIZE, SIZE), ".")

    with open(argv[2], "r") as flin:
        for idx, ln in enumerate(flin):
            if idx == BYTES_FALLEN:
                break

            col, row = map(int, ln.split(","))
            GRID[row, col] = "#"
    print(GRID)

    steps = solve(GRID, {(0, 0)}, set())
    print(steps)

    # Correct answer for part 1 is 326
