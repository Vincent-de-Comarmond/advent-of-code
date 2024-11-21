import numpy as np
from collections import defaultdict
from IPython import embed

txt_matrix = []
dst_matrix = []
with open("./inputb.txt", "r") as txtin:
    for ln in txtin:
        array = ["."] + [_ for _ in ln.strip()] + ["."]
        txt_matrix.append(array)
        dst_matrix.append([-1 for _ in array])

txt_matrix.insert(0, ["."] * len(txt_matrix[0]))
txt_matrix.append(["."] * len(txt_matrix[0]))
dst_matrix.insert(0, [-1] * len(txt_matrix[0]))
dst_matrix.append([-1] * len(txt_matrix[0]))

txt_matrix = np.array(txt_matrix)
dst_matrix = np.array(dst_matrix)

if False:
    txt = (
        "...........",
        ".S-------7.",
        ".|F-----7|.",
        ".||.....||.",
        ".||.....||.",
        ".|L-7.F-J|.",
        ".|..|.|..|.",
        ".L--J.L--J.",
        "...........",
    )
    txt_matrix = np.array([[col for col in row] for row in txt])
    dst_matrix = np.zeros(txt_matrix.shape)
    dst_matrix.fill(-1)


num_rows, num_cols = txt_matrix.shape
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
    traversed.append(curr_pt)

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

excl_matrix = np.zeros(dst_matrix.shape)


burnt = set()
active_edge = {((0, 0), ((1, 0), (0, 1), (1, 1))), ((si, sj), ((-1, 0), (1, 0)))}

while len(active_edge) != 0:

    new_edge = set()
    for pt, allowed in active_edge:
        if pt in burnt:
            continue
        burnt.add(pt)

        if dst_matrix[*pt] == -1:
            excl_matrix[*pt] = 1

        for (_i, _j) in allowed:
            i, j = pt[0] + _i, pt[1] + _j

            if i < 0 or i >= num_rows or j < 0 or j >= num_cols:
                continue

            excl_matrix[i, j] = 1
            if dst_matrix[i, j] == -1:
                new_edge.add(
                    (
                        (i, j),
                        (
                            (-1, -1),
                            (-1, 0),
                            (-1, 1),
                            (0, -1),
                            (0, 1),
                            (1, -1),
                            (1, 0),
                            (1, 1),
                        ),
                    )
                )
                continue

            char = txt_matrix[i, j]
            if char == "S":
                directions = ((-1, 0), (1, 0))
            elif char == "-":
                directions = ((0, -1), (0, 1))
            elif char == "|":
                directions = ((-1, 0), (1, 0))
            elif char == "L":
                directions = ((-1, 0), (0, 1))
            elif char == "J":
                directions = ((-1, 0), (0, -1))
            elif char == "7":
                directions = ((1, 0), (0, -1))
            elif char == "F":
                directions = ((1, 0), (0, 1))

            new_edge.add(((i, j), tuple(directions)))

    active_edge = new_edge

incl_matrix = np.ones(dst_matrix.shape) - np.maximum(excl_matrix, (dst_matrix != -1))


# for i, row in enumerate(dst_matrix):
#     newrow = [
#         "1" if incl_matrix[i, j] == 1 else "·" if col != -1 else " "
#         for j, col in enumerate(row)
#     ]
#     print("".join(newrow))

for i, row in enumerate(dst_matrix):
    newrow = [
        "\033[31m1\033[0m"
        if incl_matrix[i, j] == 1
        else txt_matrix[i, j]
        if col != -1
        else " "
        for j, col in enumerate(row)
    ]
    print("".join(newrow))

print(int(incl_matrix.sum()))
# 636 - wrong ... too high
# 558 - wrong ... too high
# 529 - wrong ... too high
# 507 is wrong
# 573 is too high
