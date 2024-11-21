from copy import deepcopy
import numpy as np
from typing import List, Tuple

TEST = False

if TEST:
    _raw = [
        "#.#####################",
        "#.......#########...###",
        "#######.#########.#.###",
        "###.....#.>.>.###.#.###",
        "###v#####.#v#.###.#.###",
        "###.>...#.#.#.....#...#",
        "###v###.#.#.#########.#",
        "###...#.#.#.......#...#",
        "#####.#.#.#######.#.###",
        "#.....#.#.#.......#...#",
        "#.#####.#.#.#########v#",
        "#.#...#...#...###...>.#",
        "#.#.#v#######v###.###v#",
        "#...#.>.#...>.>.#.###.#",
        "#####v#.#.###v#.#.###.#",
        "#.....#...#...#.#.#...#",
        "#.#########.###.#.#.###",
        "#...###...#...#...#.###",
        "###.###.#.###v#####v###",
        "#...#...#.#.>.>.#.>.###",
        "#.###.###.#.###.#.#v###",
        "#.....###...###...#...#",
        "#####################.#",
    ]
    __raw = ["#.###", ".....", ".###.", ".###.", ".....", "####."]
    # "#.###"
    # "....."
    # ".###."
    # ".###."
    # "....."
    # "####."

else:
    with open("./input.txt", "r") as txtin:
        _raw = [ln for ln in txtin]

DATA = np.array([[_ for _ in row] for row in _raw])
NR, NC = DATA.shape
START = tuple(map(int, np.where(DATA[:1, :] == ".")))
END = next(filter(lambda _: _[0] == NR - 1, zip(*np.where(DATA == "."))))
############################################################################################################
# Because of all the mist from the waterfall, the slopes are probably quite icy;                           #
# if you step onto a slope tile, your next step must be downhill (in the direction the arrow is pointing). #
# To make sure you have the most scenic hike possible, never step onto the same tile twice.                #
# What is the longest hike you can take?                                                                   #
############################################################################################################


hikes = {(START,)}


def tplus(*tuples: tuple) -> tuple:
    return tuple(sum(_[i] for _ in tuples) for i in range(len(tuples[0])))


while not all(hike[-1] == END for hike in hikes):
    for v in hikes.copy():
        cp = v[-1]
        if cp == END:
            continue

        # Check if your move is forced
        if DATA[*cp] == ">":
            nxt = tplus(cp, (0, 1))
            if nxt not in v:
                try:
                    hikes.add(v + (nxt,))
                except Exception as ex:
                    import pdb

                    pdb.set_trace()
            hikes.remove(v)
            continue
        elif DATA[*cp] == "v":
            nxt = tplus(cp, (1, 0))
            if nxt not in v:
                hikes.add(v + (nxt,))
            hikes.remove(v)
            continue
        else:
            possible_steps = set()

            for i, j in ((-1, 0), (0, 1), (1, 0), (0, -1)):
                nxt = tplus(cp, (i, j))
                if (
                    nxt[0] < 0
                    or nxt[0] > NR - 1
                    or nxt[1] < 0
                    or nxt[1] > NC - 1
                    or nxt in v
                ):
                    continue
                if DATA[*nxt] in (".", ">", "v"):
                    possible_steps.add(nxt)

            for step in possible_steps:
                hikes.add(v + (step,))
            hikes.remove(v)

print("Max hike length:")
print(max(len(v) for v in hikes) - 1)
# 1998

def print_hike(grid: np.ndarray, hike: Tuple[Tuple[int]]) -> None:
    copy = deepcopy(grid)
    for point in hike:
        copy[*point] = "O"

    print("\n".join("".join(_ for _ in row) for row in copy))
