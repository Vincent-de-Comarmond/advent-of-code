from pprint import pprint
from typing import List, Optional

lines = []
with open("./input.txt", "r") as txtin:
    for ln in txtin:
        lines.append(list(map(int, ln.strip().split(" "))))


def solve_line(line: List[Optional[int]]) -> int:

    lvl = line
    down_stash = [line]
    while min(lvl) != 0 or max(lvl) != 0:
        down_stash.append([lvl[idx] - lvl[idx - 1] for idx in range(1, len(lvl))])
        lvl = down_stash[-1]
    # pprint(down_stash)

    up_stash = []
    idx = 0
    while len(up_stash) != len(down_stash):
        down_idx = len(down_stash) - 1 - idx
        down = down_stash[down_idx]
        if idx in (0, 1):
            lvl = down + [down[-1]]
            up_stash.append(lvl)
        else:
            appendme = down[-1] + up_stash[idx - 1][-1]
            lvl = down + [appendme]
            up_stash.append(lvl)
        idx += 1
    # pprint(up_stash)
    return up_stash[-1][-1]


#################################
# test = [                      #
#     [0, 3, 6, 9, 12, 15],     #
#     [1, 3, 6, 10, 15, 21],    #
#     [10, 13, 16, 21, 30, 45], #
# ]                             #
#################################

extrapolated_sum = 0
for ln in lines:
    extrapolated_sum += solve_line(ln)

print(extrapolated_sum)
# 1588095150 is too low
# 2038472161 is the right answer
