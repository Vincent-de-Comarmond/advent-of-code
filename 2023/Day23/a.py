from copy import deepcopy
import numpy as np
from typing import List, Tuple

TEST = True

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
    _raw = ["#.###", ".....", ".###.", ".###.", ".....", "####."]
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

hikes = {START: [START]}

hikes = {(START,)}

def tplus(*tuples: tuple) -> tuple:
    return tuple(sum(_[i] for _ in tuples) for i in range(len(tuples[0])))


while not all(hike[-1] == END for k, hike in hikes.items()):
    for k, v in hikes.copy().items():
        cp = v[-1]
        if cp == END:
            continue

        # Check if your move is forced
        if DATA[*cp] == ">":
            nxt = tplus(cp, (0, 1))
            if nxt in v:
                del hikes[k]
            else:
                v.append(tplus(cp, (0, 1)))
            continue
        elif DATA[*cp] == "v":
            nxt = tplus(cp, (1, 0))
            if nxt in v:
                del hikes[k]
            else:
                v.append(tplus(cp, (1, 0)))
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
                    print(nxt)
                    print(possible_steps)
                    possible_steps.add(nxt)

            if len(possible_steps) == 0:
                del hikes[k]
            elif len(possible_steps) == 1:
                v.append(next(iter(possible_steps)))
            else:
                for step in possible_steps:
                    print("Here")
                    hikes[step] = deepcopy(v) + [step]
                del hikes[k]

print("Max hike length:")
print(max(len(v) for v in hikes.values()) - 1)


def print_hike(grid: np.ndarray, hike: List[tuple]) -> None:
    copy = deepcopy(grid)
    for point in hike:
        copy[*point] = "O"

    print("\n".join("".join(_ for _ in row) for row in copy))
