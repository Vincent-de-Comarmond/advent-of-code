import numpy as np
from typing import List, Tuple

TEST = False
PRINT = False

if TEST:
    raw = [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
        "",
        "#...##..#",
        "#....#..#",
        "..##..###",
        "#####.##.",
        "#####.##.",
        "..##..###",
        "#....#..#",
    ]

    raw = [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
        "",
        "#...##..#",
        "#....#..#",
        "..##..###",
        "#####.##.",
        "#####.##.",
        "..##..###",
        "#....#..#",
        "",
        ".#.##.#.#",
        ".##..##..",
        ".#.##.#..",
        "#......##",
        "#......##",
        ".#.##.#..",
        ".##..##.#",
        "",
        "#..#....#",
        "###..##..",
        ".##.#####",
        ".##.#####",
        "###..##..",
        "#..#....#",
        "#..##...#",
        "",
        "#.##..##.",
        "..#.##.#.",
        "##..#...#",
        "##...#..#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
    ]


else:
    with open("./input.txt", "r") as txtin:
        raw = [ln.strip() for ln in txtin]

puzzles = []
cache = []
for idx, row in enumerate(raw):
    if row == "":
        puzzles.append(np.array(cache))
        cache = []
        continue
    cache.append([_ for _ in row])

if len(cache) > 0:
    puzzles.append(np.array(cache))
    cache = []


def print_np(input_array: np.ndarray) -> None:
    if len(input_array.shape) == 2:
        print("\n".join(["".join(row) for row in input_array]))
    if len(input_array.shape) == 1:
        print("".join(input_array))


def check_reflections(
    input_matrix: np.ndarray, printme: bool = False
) -> List[Tuple[int]]:

    if printme:
        print_np(input_matrix)

    reflections = []
    for col_idx in range(1, input_matrix.shape[1]):
        width = min(col_idx, input_matrix.shape[1] - col_idx)
        alpha = input_matrix[:, col_idx - width : col_idx]
        beta = np.flip(input_matrix[:, col_idx : col_idx + width], axis=1)
        if printme:
            print(col_idx)
            print_np(alpha)
            print("----------------------")
            print_np(beta)
            print((alpha == beta).all())
            print("----------------------")

        if (alpha == beta).all():
            reflections.append((0, col_idx))

    for row_idx in range(1, input_matrix.shape[0]):
        height = min(row_idx, input_matrix.shape[0] - row_idx)
        alpha = input_matrix[row_idx - height : row_idx, :]
        beta = np.flip(input_matrix[row_idx : row_idx + height, :], axis=0)
        if printme:
            print(row_idx)
            print_np(alpha)
            print("----------------------")
            print_np(beta)
            print((alpha == beta).all())
            print("----------------------")

        if (alpha == beta).all():
            reflections.append((row_idx, 0))
    return reflections


def find_and_desmudge(
    input_matrix: np.ndarray, blocked: Tuple[int], curr_idx: int = 0
) -> Tuple[int]:

    nr, nc = input_matrix.shape

    curr_pt = (curr_idx // nc, curr_idx % nc)
    # print(curr_idx)
    # print(curr_pt)

    original = input_matrix[*curr_pt]
    input_matrix[*curr_pt] = "." if original == "#" else "#"
    # print_np(input_matrix)
    # print("--------------------")
    new_reflections = check_reflections(input_matrix)
    if blocked in new_reflections:
        new_reflections.remove(blocked)
    if len(new_reflections) == 0 and curr_idx < nr * nc - 1:
        input_matrix[*curr_pt] = original
        return find_and_desmudge(input_matrix, blocked, curr_idx + 1)

    return new_reflections


smudged_mirrors = {}
for idx, puzzle in enumerate(puzzles):
    smudged_mirrors[idx] = check_reflections(puzzle)[0]


unsmudged_mirrors = {}
for idx, puzzle in enumerate(puzzles):
    unsmudged_mirrors[idx] = find_and_desmudge(puzzle, smudged_mirrors[idx])[0]

total = sum([100 * _[0] + _[1] for _ in unsmudged_mirrors.values()])
print(total)


# 41996 -> answer is too low
