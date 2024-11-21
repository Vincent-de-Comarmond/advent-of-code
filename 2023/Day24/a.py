from typing import List, Optional, Tuple

TEST = False

MIN, MAX = (
    ((7, 7), (27, 27))
    if TEST
    else (
        (200000000000000, 200000000000000),
        (400000000000000, 400000000000000),
    )
)


if TEST:
    _raw = [
        "19, 13, 30 @ -2,  1, -2",
        "18, 19, 22 @ -1, -1, -2",
        "20, 25, 34 @ -2, -2, -4",
        "12, 31, 28 @ -1, -2, -1",
        "20, 19, 15 @  1, -5, -3",
    ]
else:
    with open("./input.txt", "r") as txtin:
        _raw = [ln for ln in txtin]

__data = {idx: dict(zip(("pos", "vel"), _.split("@"))) for idx, _ in enumerate(_raw)}
_data = {
    k: {kk: tuple(map(int, vv.split(","))) for kk, vv in v.items()}
    for k, v in __data.items()
}

DATA = {
    k: {**v, "traj": tuple(lambda t: v["pos"][i] + v["vel"][i] * t for i in (0, 1, 2))}
    for k, v in _data.items()
}


def determine_collision0(hailstone1: dict, hailstone2: dict) -> Optional[tuple]:
    t = tuple()
    try:
        t = tuple(
            (hailstone1["pos"][i] - hailstone2["pos"][i])
            / (hailstone2["vel"][i] - hailstone1["vel"][i])
            for i in (0, 1)
        )
    except ZeroDivisionError:
        # An exception in this case means these never intersect
        return

    if len(set(t)) != 1:
        return

    return tuple(_(t[0]) for _ in hailstone1["traj"])


def determine_collision1(h1: dict, h2: dict) -> Optional[tuple]:
    # PAINFUL
    # y1 = (x1 - h1["pos"][0]) * h1["vel"][1] / h1["vel"][0] + h1["pos"][1]
    # y2 = (x2 - h2["pos"][0]) * h2["vel"][1] / h2["vel"][0] + h2["pos"][1]

    # y = (x - h1["pos"][0]) * h1["vel"][1] / h1["vel"][0] + h1["pos"][1]
    # y = (x - h2["pos"][0]) * h2["vel"][1] / h2["vel"][0] + h2["pos"][1]

    p1, v1 = h1["pos"], h1["vel"]
    p2, v2 = h2["pos"], h2["vel"]

    try:
        x = (
            v1[0] * v2[0] * p2[1]
            - v1[0] * v2[0] * p1[1]
            + p1[0] * v1[1] * v2[0]
            - p2[0] * v1[0] * v2[1]
        ) / (v1[1] * v2[0] - v1[0] * v2[1])

        y = (x - p1[0]) * v1[1] / v1[0] + p1[1]

        if x < p1[0] and v1[0] > 0:
            return None
        if y < p1[1] and v1[1] > 0:
            return None
        if x > p1[0] and v1[0] < 0:
            return None
        if y > p1[1] and v1[1] < 0:
            return None

        if x < p2[0] and v2[0] > 0:
            return None
        if y < p2[1] and v2[1] > 0:
            return None
        if x > p2[0] and v2[0] < 0:
            return None
        if y > p2[1] and v2[1] < 0:
            return None

        return x, y
    except ZeroDivisionError:
        return None


def in_area(points: List[Tuple[int, ...]]) -> List[Tuple[int, ...]]:
    output = []
    for point in points:
        if (
            MIN[0] <= point[0]
            and point[0] <= MAX[0]
            and MIN[1] <= point[1]
            and point[1] <= MAX[1]
        ):
            output.append(point)
    return output


intersection_points = {}

for k1, v1 in sorted(DATA.items()):
    for k2, v2 in sorted(DATA.items()):
        if k2 <= k1:
            continue

        collision_point = determine_collision1(v1, v2)

        if collision_point is not None:
            intersection_points[(k1, k2)] = collision_point


points_in_area = in_area(intersection_points.values())
print(len(points_in_area))
# 23760 is the right answer for part 1
