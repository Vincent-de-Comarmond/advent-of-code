import numpy as np
from typing import List

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
else:
    with open("./input.txt", "r") as txtin:
        raw = [ln.strip() for ln in txtin]

puzzles = []
cache = []
for idx, row in enumerate(raw):
    if row == "" or idx == len(raw) - 1:
        puzzles.append(np.array(cache))
        cache = []
        continue
    cache.append([_ for _ in row])


def print_np(input_array: np.ndarray) -> None:
    if len(input_array.shape) == 2:
        print("\n".join(["".join(row) for row in input_array]))
    if len(input_array.shape) == 1:
        print("".join(input_array))


def check_vertical_mirrors(input_matrix: np.ndarray) -> List[int]:
    mirror_indicies = []

    if PRINT:
        print_np(input_matrix)

    for col_idx in range(1, input_matrix.shape[1]):
        width = min(col_idx, input_matrix.shape[1] - col_idx)
        alpha = input_matrix[:, col_idx - width : col_idx]
        beta = np.flip(input_matrix[:, col_idx : col_idx + width], axis=1)
        if PRINT:
            print(col_idx)
            print_np(alpha)
            print("----------------------")
            print_np(beta)
            print((alpha == beta).all())
            print("----------------------")

        if (alpha == beta).all():
            mirror_indicies.append(col_idx)
    return mirror_indicies


def check_horizontal_mirrors(input_matrix: np.ndarray) -> List[int]:
    mirror_idxs = []

    if PRINT:
        print_np(input_matrix)

    for row_idx in range(1, input_matrix.shape[0]):
        height = min(row_idx, input_matrix.shape[0] - row_idx)
        alpha = input_matrix[row_idx - height : row_idx, :]
        beta = np.flip(input_matrix[row_idx : row_idx + height, :], axis=0)
        if PRINT:
            print(row_idx)
            print_np(alpha)
            print("----------------------")
            print_np(beta)
            print((alpha == beta).all())
            print("----------------------")

        if (alpha == beta).all():
            mirror_idxs.append(row_idx)
    return mirror_idxs


if True:
    total = 0
    for idx, puzzle in enumerate(puzzles):
        vertical_score = sum(check_vertical_mirrors(puzzle))
        horizontal_score = 100 * sum(check_horizontal_mirrors(puzzle))

        if vertical_score + horizontal_score == 0:
            print(idx)

        total += horizontal_score + vertical_score

    print(total)

# 15608 That's not the right answer; your answer is too low
# 25123 is too low
# 17109  -> obviously going to be too low
