import numpy as np
from typing import Tuple

txt_matrix = []
dst_matrix = []
with open("./input.txt", "r") as txtin:
    for ln in txtin:
        array = [_ for _ in ln.strip()]
        txt_matrix.append(array)
        dst_matrix.append([-1 for _ in array])

txt_matrix = np.array(txt_matrix)
dst_matrix = np.array(dst_matrix)

num_rows, num_cols = txt_matrix.shape
num_rows, num_cols = num_rows, num_cols
si, sj = map(lambda _: _[0], np.where(txt_matrix == "S"))

connections = {
    "|": "is a vertical pipe connecting north and south.",
    "-": "is a horizontal pipe connecting east and west.",
    "L": "is a 90-degree bend connecting north and east.",
    "J": "is a 90-degree bend connecting north and west.",
    "7": "is a 90-degree bend connecting south and west.",
    "F": "is a 90-degree bend connecting south and east.",
    ".": "is ground; there is no pipe in this tile.",
    "S": "is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.",
}

interpretations = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
}

distance = 0
prev_pt, curr_pt = (si, sj), (si, sj)
traversed = []

while True:
    char = txt_matrix[*curr_pt]
    dst_matrix[*curr_pt] = distance
    # print(char, curr_pt)
    traversed.append((*curr_pt, distance))

    if char == "S":
        if distance != 0:
            break
        i, j = curr_pt
        n, e, s, w = (i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)
        for _dir in (n, e, s, w):
            adjacent = txt_matrix[*_dir]
            if _dir == n and adjacent in ("|", "7", "F"):
                curr_pt = n
                break
            if _dir == e and adjacent in ("-", "J", "7"):
                curr_pt = e
                break
            if _dir == s and adjacent in ("|", "L", "J"):
                curr_pt = s
                break
            if _dir == w and adjacent in ("-", "L", "F"):
                curr_pt = w
                break
        distance += 1
        continue

    if char in ("|", "-", "L", "J", "7", "F"):
        diff = tuple(prev_pt[_] - curr_pt[_] for _ in (0, 1))
        posses = interpretations[char]

        nxt = posses[1] if posses[0] == diff else posses[0]

        prev_pt = curr_pt
        curr_pt = tuple(curr_pt[_] + nxt[_] for _ in (0, 1))
        distance += 1

###################################################################
# with open("./output_map.txt", "w") as txtout:                  #
#     lines = []                                                 #
#     for row in dst_matrix:                                     #
#         stringified = [str(_) if _ != -1 else " " for _ in row] #
#         lines.append("".join(stringified))                     #
#     txtout.write("\n".join(lines))                              #
###################################################################


max_distance = max(traversed, key=lambda _: _[2])[2] // 2
# 6820 is the right answer
