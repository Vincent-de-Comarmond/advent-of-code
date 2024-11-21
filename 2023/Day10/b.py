import numpy as np
from collections import defaultdict

txt_matrix = []
dst_matrix = []
with open("./inputb.txt", "r") as txtin:
    for ln in txtin:
        array = [_ for _ in ln.strip()]
        txt_matrix.append(array)
        dst_matrix.append([-1 for _ in array])

txt_matrix = np.array(txt_matrix)
dst_matrix = np.array(dst_matrix)

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

encl_matrix = np.zeros(dst_matrix.shape)


for i, row in enumerate(dst_matrix):
    for j, val in enumerate(row):
        if val != -1:
            # Ignore things that are pipes
            # i.e. things that have distance != -1
            continue

        n, e, s, w = False, False, False, False

        seen_chars = list()

        # North
        for ii in range(i, -1, -1):
            char = txt_matrix[ii, j]
            if dst_matrix[ii, j] != -1 and char != "|":
                if char == "-":
                    n = True
                    break
                if char in ("7", "F"):
                    seen_chars.append(char)
                    if len(seen_chars) < 2:
                        continue

                    gotcha = False
                    if seen_chars[0] == "F":
                        if seen_chars.count("F") - seen_chars.count("7") > 0:
                            gotcha = True
                    if seen_chars[0] == "7":
                        if seen_chars.count("7") - seen_chars.count("7") > 0:
                            gotcha = True
                    if gotcha:
                        n = True
                        break
        else:
            seen_chars = list()
            continue

        # East
        for jj in range(j, num_cols):
            char = txt_matrix[i, jj]
            if dst_matrix[i, jj] != -1 and char != "-":
                if char == "|":
                    e = True
                    break
                if char in ("J", "7"):
                    seen_chars.append(char)
                    if len(seen_chars) < 2:
                        continue

                    gotcha = False
                    if seen_chars[0] == "J":
                        if seen_chars.count("J") - seen_chars.count("J") > 0:
                            gotcha = True
                    if seen_chars[0] == "7":
                        if seen_chars.count("7") - seen_chars.count("J") > 0:
                            gotcha = True
                    if gotcha:
                        e = True
                        break
        else:
            seen_chars = list()
            continue

        # South
        for ii in range(i, num_rows):
            char = txt_matrix[ii, j]
            if dst_matrix[ii, j] != -1 and char != "|":
                if char == "-":
                    s = True
                    break
                if char in ("L", "J"):
                    seen_chars.append(char)
                    if len(seen_chars) < 2:
                        continue

                    gotcha = False
                    if seen_chars[0] == "L":
                        if seen_chars.count("L") - seen_chars.count("J") > 0:
                            gotcha = True
                    if seen_chars[0] == "J":
                        if seen_chars.count("J") - seen_chars.count("L") > 0:
                            gotcha = True
                    if gotcha:
                        s = True
                        break
        else:
            seen_chars = list()
            continue

        # West
        for jj in range(j, -1, -1):
            char = txt_matrix[i, jj]
            if dst_matrix[i, jj] != -1 and char != "-":
                if char == "|":
                    w = True
                    break
                if char in ("F", "L"):
                    seen_chars.append(char)
                    if len(seen_chars) < 2:
                        continue

                    gotcha = False
                    if seen_chars[0] == "F":
                        if seen_chars.count("F") - seen_chars.count("L") > 0:
                            gotcha = True
                    if seen_chars[0] == "L":
                        if seen_chars.count("L") - seen_chars.count("F") > 0:
                            gotcha = True

                    if gotcha:
                        w = True
                        break
        else:
            seen_chars = list()
            continue

        if all((n, e, s, w)):
            encl_matrix[i, j] = 1


####################################################
# for row in encl_matrix:                          #
#     print()                                      #
#     for col in row:                              #
#         print(int(col), end="")                  #
#                                                  #
# for row in dst_matrix:                           #
#     print()                                      #
#     for col in row:                              #
#         print("·" if col != -1 else " ", end="") #
####################################################


for i, row in enumerate(dst_matrix):
    newrow = [
        "1" if encl_matrix[i, j] == 1 else "·" if col != -1 else " "
        for j, col in enumerate(row)
    ]
    print("".join(newrow))


print(int(encl_matrix.sum()))
# 636 - wrong ... too high
# 558 - wrong ... too high
# 529 - wrong ... too high
# 507 is wrong
