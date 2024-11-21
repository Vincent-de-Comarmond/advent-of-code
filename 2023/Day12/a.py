from copy import copy
import re


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

# pattern = re.compile(r"(#|\?)+")
pattern = re.compile(r"#+")
total_possibilities = 0

for datum in info:
    solved = []
    row, numbers = datum
    damaged = sum(numbers)
    undamaged = len(row) - damaged

    unknown_damaged = damaged - row.count("#")
    unknown_undamaged = undamaged - row.count(".")

    possiblity_set = []
    for idx, char in enumerate(row):

        if char == "?":

            if len(possiblity_set) == 0:

                option1, option2 = [_ for _ in row], [_ for _ in row]
                option1[idx], option2[idx] = ".", "#"
                possiblity_set.extend(["".join(option1), "".join(option2)])
            else:

                extensions = []
                for parent in copy(possiblity_set):
                    child1, child2 = [_ for _ in parent], [_ for _ in parent]
                    child1[idx], child2[idx] = ".", "#"
                    possiblity_set.extend(["".join(child1), "".join(child2)])
                    possiblity_set.remove(parent)

    possiblities = 0
    for test_str in possiblity_set:
        broken = tuple(map(len, pattern.findall(test_str)))
        if numbers == broken:
            possiblities += 1
    total_possibilities += possiblities
    # print(possiblities)

print("#####")
print(total_possibilities)
print("#####")
# 7204 is the right answer
