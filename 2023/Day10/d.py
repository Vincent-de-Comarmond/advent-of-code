import numpy as np
from functools import partial
from collections import defaultdict
from IPython import embed

txt_matrix = []
dst_matrix = []
with open("./inputb.txt", "r") as txtin:
    for ln in txtin:
        array = ["."] + [_ for _ in ln.strip()] + ["."]
        txt_matrix.append(array)
        dst_matrix.append([-1 for _ in array])

txt_matrix = np.array(txt_matrix)
dst_matrix = np.array(dst_matrix)


test = False
if test:
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


def t_add(t1: tuple, t2: tuple) -> tuple:
    return tuple(t1[i] + t2[i] for i in range(len(t1)))


paintme = np.zeros(dst_matrix.shape)

for idx in range(1, len(traversed)):
    curr = traversed[idx]
    curr_char = txt_matrix[*curr]
    prev = traversed[idx - 1]
    prev_char = txt_matrix[*prev]
    diff = tuple(curr[i] - prev[i] for i in (0, 1))

    paint_left = set()
    paint_right = set()

    if prev_char == "|":
        if diff == (1, 0):
            paint_left.add(t_add(prev, (0, 1)))
            paint_right.add(t_add(prev, (0, -1)))
        if diff == (-1, 0):
            paint_left.add(t_add(prev, (0, -1)))
            paint_right.add(t_add(prev, (0, 1)))
    if prev_char == "-":
        if diff == (0, 1):
            paint_left.add(t_add(prev, (-1, 0)))
            paint_right.add(t_add(prev, (1, 0)))
        if diff == (0, -1):
            paint_left.add(t_add(prev, (1, 0)))
            paint_right.add(t_add(prev, (-1, 0)))
    if prev_char == "L":
        if diff == (-1, 0):
            paint_left.add(t_add(prev, (0, -1)))
            paint_left.add(t_add(prev, (1, -1)))
            paint_left.add(t_add(prev, (1, 0)))
            paint_right.add(t_add(prev, (-1, 1)))
        if diff == (0, 1):
            paint_right.add(t_add(prev, (-1, 1)))
            paint_right.add(t_add(prev, (0, -1)))
            paint_right.add(t_add(prev, (1, -1)))
            paint_left.add(t_add(prev, (1, 0)))
    if prev_char == "J":
        if diff == (-1, 0):
            paint_left.add(t_add(prev, (-1, -1)))
            paint_right.add(t_add(prev, (1, 0)))
            paint_right.add(t_add(prev, (1, 1)))
            paint_right.add(t_add(prev, (0, 1)))
        if diff == (0, -1):
            paint_left.add(t_add(prev, (0, 1)))
            paint_left.add(t_add(prev, (1, 1)))
            paint_left.add(t_add(prev, (1, 0)))
            paint_right.add(t_add(prev, (-1, -1)))
    if prev_char == "7":
        if diff == (0, -1):
            paint_left.add(t_add(prev, (1, -1)))
            paint_right.add(t_add(prev, (0, 1)))
            paint_right.add(t_add(prev, (-1, 1)))
            paint_right.add(t_add(prev, (-1, 0)))
        if diff == (1, 0):
            paint_left.add(t_add(prev, (-1, 0)))
            paint_left.add(t_add(prev, (-1, 1)))
            paint_left.add(t_add(prev, (1, 1)))
            paint_right.add(t_add(prev, (1, -1)))
    if prev_char == "F":
        if diff == (1, 0):
            paint_left.add(t_add(prev, (1, 1)))
            paint_right.add(t_add(prev, (-1, 0)))
            paint_right.add(t_add(prev, (-1, -1)))
            paint_right.add(t_add(prev, (-1, 0)))
        if diff == (0, 1):
            paint_right.add(t_add(prev, (1, 1)))
            paint_left.add(t_add(prev, (0, -1)))
            paint_left.add(t_add(prev, (-1, -1)))
            paint_left.add(t_add(prev, (-1, 0)))

    for _tup in paint_left:
        paintme[*_tup] = -1
    for _tup in paint_right:
        paintme[*_tup] = 1

paintme[dst_matrix != -1] = 0

left_start = {_ for _ in zip(*np.where(paintme == -1))}
right_start = {_ for _ in zip(*np.where(paintme == 1))}


for idx, active_edge in enumerate((left_start, right_start)):

    burnt = set()
    fill = -1 if idx == 0 else 1
    while len(active_edge) != 0:
        new_edge = set()

        for pt in active_edge:
            if pt in burnt:
                continue
            burnt.add(pt)

            if dst_matrix[*pt] == -1:
                paintme[*pt] = fill
            else:
                continue

            for k in range(9):
                _pt = (pt[0] + k // 3 - 1, pt[1] + k % 3 - 1)
                if _pt[0] < 0 or _pt[0] >= num_rows or _pt[1] < 0 or _pt[1] >= num_cols:
                    continue

                new_edge.add(_pt)
        active_edge = new_edge

if True:
    for i, row in enumerate(dst_matrix):
        newrow = [
            txt_matrix[i, j]
            if dst_matrix[i, j] != -1
            else "\033[34m0\033[0m"
            if paintme[i, j] == -1
            else "\033[31m0\033[0m"
            if paintme[i, j] == 1
            else " "
            for j, col in enumerate(row)
        ]
        print("".join(newrow))

print((paintme == -1).sum())
# 332 is also wrong (FML)
# 346 is also wrong
