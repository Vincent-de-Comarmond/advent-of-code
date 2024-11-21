import numpy as np
from collections import defaultdict

test = False

raw_input = []
if test:
    raw_input = [
        "...#......",
        ".......#..",
        "#.........",
        "..........",
        "......#...",
        ".#........",
        ".........#",
        "..........",
        ".......#..",
        "#...#.....",
    ]
    # Answer should be 374
    raw_input = [[_ for _ in row] for row in raw_input]

else:
    with open("./input.txt", "r") as txtin:
        for ln in txtin:
            raw_input.append([_ for _ in ln.strip()])


raw_input = np.array(raw_input)

row_sums = np.sum(raw_input == "#", axis=1)
col_sums = np.sum(raw_input == "#", axis=0)


multiplier = 1000000
galaxies = np.where(raw_input == "#")
galaxy_locs = list(zip(*galaxies))

distances = defaultdict(int)
for idx1, loc1 in enumerate(galaxy_locs):
    for idx2 in range(idx1 + 1, len(galaxy_locs)):
        loc2 = galaxy_locs[idx2]

        for i in range(min(loc1[0], loc2[0]), max(loc1[0], loc2[0])):
            mult = 1 if row_sums[i] != 0 else multiplier
            distances[frozenset({idx1, idx2})] += mult
        for j in range(min(loc1[1], loc2[1]), max(loc1[1], loc2[1])):
            mult = 1 if col_sums[j] != 0 else multiplier
            distances[frozenset({idx1, idx2})] += mult

# print(distances)
print(sum(distances.values()))
# 9233514 was the correct answer
# 363293506944 is the correct answer
