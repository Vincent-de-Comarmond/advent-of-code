import numpy as np


test = True

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
    raw_input = [[_ for _ in row] for row in raw_input]

else:
    with open("./input.txt", "r") as txtin:
        for ln in txtin:
            raw_input.append([_ for _ in ln.strip()])


raw_input = np.array(raw_input)

row_sums = np.sum(raw_input == "#", axis=1)
col_sums = np.sum(raw_input == "#", axis=0)

num_cols = len(col_sums) + np.sum(col_sums == 0)
num_rows = len(row_sums) + np.sum(row_sums == 0)


expanded_output = []
for i, row in enumerate(raw_input):

    if row_sums[i] == 0:
        expanded_output.append(["." for _ in range(num_cols)])

    expanded_row = []
    for j, col in enumerate(row):
        expanded_row.append(col)

        if col_sums[j] == 0:
            expanded_row.append(".")
    expanded_output.append(expanded_row)

expanded_output = np.array(expanded_output)
galaxies = np.where(expanded_output == "#")

galaxy_locs = list(zip(*galaxies))

distances = {}
for idx1, loc1 in enumerate(galaxy_locs):
    for idx2 in range(idx1 + 1, len(galaxy_locs)):
        loc2 = galaxy_locs[idx2]
        distances[frozenset({idx1, idx2})] = abs(loc2[0] - loc1[0]) + abs(
            loc2[1] - loc1[1]
        )

print(distances)
print(sum(distances.values()))
# 9233514 was the correct answer
