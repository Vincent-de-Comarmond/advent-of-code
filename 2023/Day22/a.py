from copy import deepcopy
from collections import defaultdict
from itertools import product
import numpy as np
from typing import Dict, List, Set, Tuple

TEST = False

if TEST:
    _raw = [
        "1,0,1~1,2,1",
        "0,0,2~2,0,2",
        "0,2,3~2,2,3",
        "0,0,4~0,2,4",
        "2,0,5~2,2,5",
        "0,1,6~2,1,6",
        "1,1,8~1,1,9",
    ]
else:
    with open("./input.txt", "r") as txtin:
        _raw = [ln for ln in txtin]


def create_data(rawinput: List[str]) -> List[Dict[str, Set[Tuple[int]]]]:
    output = []

    for idx, line in enumerate(rawinput):
        side1, side2 = line.split("~")
        point1 = tuple(map(int, side1.split(",")))
        point2 = tuple(map(int, side2.split(",")))
        tmp = {"lower": set(), "upper": set(), "settled": False, "id": idx}

        for i, j in product(
            range(point1[0], point2[0] + 1), range(point1[1], point2[1] + 1)
        ):
            low_point = min(point1[2], point2[2])
            if low_point == 1:
                tmp["settled"] = True

            tmp["lower"].add((i, j, low_point))
            tmp["upper"].add((i, j, max(point1[2], point2[2])))
        output.append(tmp)

    return output


def settle_bricks(
    input_data: List[Dict[str, Set[Tuple[int]]]]
) -> List[Dict[str, Set[Tuple[int]]]]:
    #

    max_height_so_far = 0
    while not all((_["settled"] for _ in input_data)):
        fraction = sum(_["settled"] for _ in input_data) / len(input_data)
        print(f"Fraction settled: {fraction}")

        for brick in sorted(
            input_data, key=lambda _: min(pt[2] for pt in _["lower"])
        ).copy():
            if brick["settled"]:
                max_height_so_far = max(
                    max_height_so_far, max(_[2] for _ in brick["upper"])
                )

                continue
            intersecting_plane = {(_[0], _[1], _[2] - 1) for _ in brick["lower"]}

            for brick2 in sorted(
                input_data, key=lambda _: -max(pt[2] for pt in _["upper"])
            ):
                if not brick2["settled"]:
                    continue

                if brick2["upper"].intersection(intersecting_plane):
                    brick["settled"] = True
                    max_height_so_far = max(
                        max_height_so_far, max(_[2] for _ in brick["upper"])
                    )

                    break
            else:
                input_data.remove(brick)
                brick_lowest = min(_[2] for _ in brick["lower"])
                if brick_lowest == 1:
                    brick["settled"] = True

                brick["lower"] = {(_[0], _[1], _[2] - 1) for _ in brick["lower"]}
                brick["upper"] = {(_[0], _[1], _[2] - 1) for _ in brick["upper"]}
                input_data.append(brick)
    return input_data


def determine_removeability(
    input_data: List[Dict[str, Set[Tuple[int]]]]
) -> Tuple[dict]:
    _supports = {_["id"]: set() for _ in input_data}
    _supported_by = {_["id"]: set() for _ in input_data}

    for brick in input_data:
        if min(pt[2] for pt in brick["lower"]) == 1:
            _supported_by[brick["id"]].add(-1)
            continue

        intersecting_plane = {(_[0], _[1], _[2] - 1) for _ in brick["lower"]}

        for brick2 in input_data:
            if brick2["upper"].intersection(intersecting_plane):
                _supported_by[brick["id"]].add(brick2["id"])
                _supports[brick2["id"]].add(brick["id"])
    return _supports, _supported_by


print("Creating raw data")
_data = create_data(_raw)
print("Settling bricks")
data = settle_bricks(_data)
print("Determining support structure")
supports, supported_by = determine_removeability(data)

print("Determining removeability")
# 518 - answer is too high
# 531 is too high (no surprise)
# 332 is too low
# 437 is the wrong answer

blacklisted = set()
removeable_blocks = set()
for block in data:
    removeable_blocks.add(block["id"])
    for k, v in supported_by.items():
        if block["id"] in v and len(v) == 1:
            blacklisted.add(block["id"])


removeable_blocks = removeable_blocks - blacklisted
# This gives 437 which is the wrong answer


if False:
    removeable_blocks_alpha = set()
    for k, v in supports.items():
        if len(v) == 0:
            removeable_blocks_alpha.add(k)

    beta = {k: v for k, v in supported_by.items() if len(v) >= 2}
    all_multiple_supports = {inner for outer in beta.values() for inner in outer}
    gamma = {}
    for k, v in supported_by.items():
        if len(v.intersection(all_multiple_supports)) > 0:
            gamma[k] = v

    removeable_blocks_beta = deepcopy(all_multiple_supports)
    for k, v in gamma.items():
        if len(v) == 1:
            for item in v:
                if item in removeable_blocks_beta:
                    removeable_blocks_beta.remove(item)

    removeable_blocks = removeable_blocks_alpha | removeable_blocks_beta

    print(removeable_blocks)
    print(len(removeable_blocks))
