import pdb
import numpy as np


TEST = True

if TEST:
    raw = [
        "2413432311323",
        "3215453535623",
        "3255245654254",
        "3446585845452",
        "4546657867536",
        "1438598798454",
        "4457876987766",
        "3637877979653",
        "4654967986887",
        "4564679986453",
        "1224686865563",
        "2546548887735",
        "4322674655533",
    ]

    # raw = ["1121", "2112", "1221", "1111"]


else:
    with open("./input.txt", "r") as txtin:
        raw = [ln.strip() for ln in txtin]

DATA = np.array([[int(_) for _ in row] for row in raw])


def t_add(t1: tuple, t2: tuple) -> tuple:
    return tuple(t1[i] + t2[i] for i in range(len(t1)))


def t_minus(t1: tuple, t2: tuple) -> tuple:
    return tuple(t1[i] - t2[i] for i in range(len(t1)))


burnt = {}
NR, NC = DATA.shape
active = {((0, 0), 0, "e"), ((0, 0), 0, "s")}
directions = {"n": (-1, 0), "e": (0, 1), "s": (1, 0), "w": (0, -1)}

while len(active) > 0:

    for datum in active.copy():
        active.remove(datum)

        point, energy, journey = datum
        _dir = journey[-1]

        new_point = t_add(point, directions[_dir])
        ni, nj = new_point
        if ni < 0 or nj < 0 or ni > NR - 1 or nj > NC - 1:
            continue
        new_energy = energy + DATA[new_point]

        if new_point not in burnt:
            burnt[new_point] = {"energy": new_energy, "journey": journey}
            print(new_point)
            if new_point == (NR - 1, NC - 1):
                print(burnt[NR - 1, NC - 1])
        elif new_energy < burnt[new_point]["energy"]:
            burnt[new_point] = {"energy": new_energy, "journey": journey}
            if new_point == (NR - 1, NC - 1):
                print(burnt[NR - 1, NC - 1])
        elif new_energy > burnt[new_point]["energy"] + 20:
            # Stop infinite loops
            # Don't burn points trivially ... it might hurt us
            continue

        # Don't continue if we're at the edge
        if new_point == (NR - 1, NC - 1):
            continue

        for k, v in directions.items():
            # No u-turns
            if {_dir, k} in ({"n", "s"}, {"e", "w"}):
                continue
            laststeps = journey[-3:] + k
            # Max 3 steps in the same direction
            if len(laststeps) == 4 and len(set(laststeps)) == 1:
                continue

            active.add((new_point, new_energy, journey + k))


reversed_map = DATA.astype(str)
# translator = str.maketrans({"n": "s", "s": "n", "w": "e", "e": "w"})
pt = (NR - 1, NC - 1)
reversed_map[pt] = "."
for _d in reversed(burnt[pt]["journey"]):
    pt = t_minus(pt, directions[_d])
    reversed_map[pt] = "."

print(reversed_map)


print(burnt)
