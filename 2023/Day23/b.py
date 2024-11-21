from copy import deepcopy
from multiprocessing import Pool
import numpy as np
from typing import Dict, List, Literal, Tuple

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


def mp_function(
    input_tuple: Tuple[Tuple[int]],
) -> Dict[Literal["add", "discard"], Tuple[Tuple[int]]]:
    cp = input_tuple[-1]
    if cp == END:
        return dict()

    possible_steps = set()
    for i, j in ((-1, 0), (0, 1), (1, 0), (0, -1)):
        nxt = tplus(cp, (i, j))
        if (
            nxt[0] < 0
            or nxt[0] > NR - 1
            or nxt[1] < 0
            or nxt[1] > NC - 1
            or nxt in input_tuple
        ):
            continue
        if DATA[*nxt] in (".", ">", "v"):
            possible_steps.add(nxt)

    output = {"add": [], "discard": input_tuple}

    for step in possible_steps:
        output["add"].append(input_tuple + (step,))

    return output


with Pool(processes=10) as pool:
    while not all(hike[-1] == END for hike in hikes):
        results = pool.map(mp_function, list(hikes))

        for result in results:
            if "discard" in result:
                hikes.remove(result["discard"])
            if "add" in result:
                for path in result["add"]:
                    hikes.add(path)

print("Max hike length:")
print(max(len(v) for v in hikes) - 1)
# 1998 -  correct answer for part 1


def print_hike(grid: np.ndarray, hike: Tuple[Tuple[int]]) -> None:
    copy = deepcopy(grid)
    for point in hike:
        copy[*point] = "O"

    print("\n".join("".join(_ for _ in row) for row in copy))
