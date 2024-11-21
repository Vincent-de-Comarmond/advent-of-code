from more_itertools import distinct_permutations
import re
from typing import Tuple

Test = False
raw = []

if Test:
    raw = [
        "???.### 1,1,3",
        ".??..??...?##. 1,1,3",
        "?#?#?#?#?#?#?#? 1,3,1,6",
        "????.#...#... 4,1,1",
        "????.######..#####. 1,6,5",
        "?###???????? 3,2,1",
    ]
else:
    with open("./input.txt", "r") as txtin:
        raw = [ln.strip() for ln in txtin]

info = [
    (row.split(" ")[0], tuple(map(int, row.split(" ")[1].split(",")))) for row in raw
]

PATTERN = re.compile(r"#+")


def expand_record(input_str: str, input_numbers: Tuple[int]) -> Tuple[str, Tuple[int]]:
    return "?".join(input_str for _ in range(5)), tuple(list(input_numbers) * 5)


def check_number_valid_combos(input_str: str, input_numbers: Tuple[int]) -> int:

    length = len(input_str)
    known_broken = input_str.count("#")
    known_working = input_str.count(".")

    broken = sum(input_numbers)
    working = length - broken

    unknown_broken = broken - known_broken
    unknown_working = working - known_working

    possibilities = 0
    for combo in distinct_permutations("#" * unknown_broken + "." * unknown_working):
        replaced = input_str
        for char in combo:
            replaced = replaced.replace("?", char, 1)  # replace takes no kwargs

        match_patterns = tuple(len(_) for _ in PATTERN.findall(replaced))
        if match_patterns == input_numbers:
            possibilities += 1

    return possibilities


total_possibilities = 0
for idx, record in enumerate(info):
    expanded_rec = expand_record(*record)
    total_possibilities += check_number_valid_combos(*expanded_rec)
    completion = 100 * (idx + 1) / len(info)
    print(f"{completion:2.2f} %")

print(total_possibilities)
