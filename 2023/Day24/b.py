from math import floor
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

DATA = {}
for k, v in _data.items():
    DATA[k] = {
        **v,
        "traj": tuple(lambda t: v["pos"][i] + v["vel"][i] * t for i in (0, 1, 2)),
    }


for k, v in DATA.items():
    # z = v["pos"][2] + v["vel"][2] * t = 0
    # t = - v["pos"][2] / v["vel"][2]
    v["crash_time"] = floor(-v["pos"][2] / v["vel"][2])
