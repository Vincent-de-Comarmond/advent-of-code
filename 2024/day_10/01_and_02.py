from typing import Set
import numpy as np

with open("./input.txt", "r") as txtin:
    data = np.array([[int(char) for char in line if char != "\n"] for line in txtin])

# Note the format here is row, column
trails = {((_[0], _[1], 0),) for _ in zip(*np.where(data == 0))}


def get_legit_neighbours(i, j, elevation, grid=data):
    neighbours = [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]
    neighbours = [_ for _ in neighbours if _[0] >= 0 and _[1] >= 0]
    neighbours = [
        _ for _ in neighbours if _[0] < grid.shape[0] and _[1] < grid.shape[1]
    ]
    return [(a, b, grid[a, b]) for a, b in neighbours if grid[a, b] == elevation + 1]


def recurse_trails(trail_list: Set[tuple]):
    newtrail_list = set()
    for trail in trail_list:
        point = trail[-1]
        legit_neighbours = get_legit_neighbours(*trail[-1])
        newtrail_list |= {
            tuple(list(trail) + [neighbour]) for neighbour in legit_neighbours
        }
    if len(newtrail_list) == 0:
        return trail_list
    return recurse_trails(newtrail_list)


total_trails = recurse_trails(trails)
trail_starts_and_ends = {
    (_[0], _[-1]) for _ in total_trails if _[0][2] == 0 and _[-1][2] == 9
}

print(f"Total trail score: {len(trail_starts_and_ends)}")
# 629 is the right answer for part 1
print(f"Total trail rating: {len(total_trails)}")
# 1242 is the right answer for part 2
