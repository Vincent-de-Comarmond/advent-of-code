"""
Advent Of Code 2023, Day 16, Part 2
"""
from collections import defaultdict
from pprint import pprint
from textwrap import dedent
from typing import DefaultDict, List, Set, Tuple

# 3rd party
import numpy as np

TEST = False

if TEST:
    raw = dedent(
        r"""
        .|...\....
        |.-.\.....
        .....|-...
        ........|.
        ..........
        .........\
        ..../.\\..
        .-.-/..|..
        .|....-|.\
        ..//.|...."""
    )

    print(raw)
else:
    with open("./input.txt", "r") as txtin:
        raw = txtin.read()

info_grid = np.array(
    [[_ for _ in row.strip()] for row in filter(lambda _: len(_) > 0, raw.splitlines())]
)


def add(tuple1: Tuple[int], tuple2: Tuple[int]) -> Tuple[int]:
    return tuple(tuple1[i] + tuple2[i] for i in range(max(len(tuple1), len(tuple2))))


def np_print(np_array: np.ndarray) -> None:
    print("\n".join(["".join([_ for _ in row]) for row in np_array]))


def paint1(
    np_array: np.ndarray, beams: DefaultDict[Tuple[Tuple[int]], List[Tuple[Tuple[int]]]]
) -> DefaultDict[Tuple[int], Set[Tuple[int]]]:

    score = defaultdict(set)
    for k, v in beams.items():
        score[k[0]].add(k[1])

        for beam_seg in v:
            score[beam_seg[0]].add(beam_seg[1])

    copy = np_array.copy()

    for k, v in score.items():
        if copy[*k] != ".":
            continue

        img = ""
        if len(v) > 1:
            img = str(len(v))
        else:
            _dir = next(iter(v))
            img = (
                ">"
                if _dir == (0, 1)
                else "<"
                if _dir == (0, -1)
                else "v"
                if _dir == (1, 0)
                else "^"
            )
        copy[*k] = img
    print()
    np_print(copy)
    return score


def determine_beams(
    grid: np.ndarray,
    beams: DefaultDict[Tuple[Tuple[int]], List[Tuple[Tuple[int]]]],
    burnt: Set[Tuple[Tuple[int]]],
    executions: int = 0,
    printme: bool = False,
) -> None:

    NR, NC = grid.shape
    _print = print if printme else lambda *args: None
    _print(f"Execution: {executions}")

    for key in set(beams) - burnt:
        ni, nj = add(*beams[key][-1])
        _dir = beams[key][-1][1]

        # Have we gone ouside of the boundary ?
        # If so burn this beam ...  there's no-where left to go
        # Skip to the next point
        if ni < 0 or ni > NR - 1 or nj < 0 or nj > NC - 1:
            _print(f"Burning {key}")
            burnt.add(key)
            continue

        topo = grid[ni, nj]
        if topo == "/":
            newdir = (-_dir[1], -_dir[0])
            beams[key].append(((ni, nj), newdir))
            continue
        if topo == "\\":
            newdir = (_dir[1], _dir[0])
            beams[key].append(((ni, nj), newdir))
            continue

        if topo == "-" and _dir in ((1, 0), (-1, 0)):
            _print(f"Burning {key}")
            burnt.add(key)

            beams[((ni, nj), (0, -1))].append(((ni, nj), (0, -1)))
            beams[((ni, nj), (0, 1))].append(((ni, nj), (0, 1)))
            continue

        if topo == "|" and _dir in ((0, 1), (0, -1)):
            _print(f"Burning {key}")
            burnt.add(key)

            beams[((ni, nj), (-1, 0))].append(((ni, nj), (-1, 0)))
            beams[((ni, nj), (1, 0))].append(((ni, nj), (1, 0)))
            continue

        beams[key].append(((ni, nj), _dir))

    if len(set(beams) - burnt) <= 0:
        return

    return determine_beams(grid, beams, burnt, executions + 1, printme)


def determine_energy_level(
    beams: DefaultDict[Tuple[Tuple[int]], List[Tuple[Tuple[int]]]],
    lower_boundary: Tuple[int],
    upper_boundary: Tuple[int],
) -> int:
    def inside(point: Tuple[int]) -> bool:
        for idx, pt in enumerate(point):
            if pt < lower_boundary[idx]:
                return False
            if pt > upper_boundary[idx]:
                return False
        return True

    points_touched = set()
    for k, v in beams.items():
        if inside(k[0]):
            points_touched.add(k[0])
        segments = {_[0] for _ in v if inside(_[0])}
        points_touched.update(segments)

    return len(points_touched)


top_edge = [((-1, _), (1, 0)) for _ in range(info_grid.shape[1])]
bot_edge = [((info_grid.shape[0], _), (-1, 0)) for _ in range(info_grid.shape[1])]
left_edge = [((_, -1), (0, 1)) for _ in range(info_grid.shape[0])]
right_edge = [((_, info_grid.shape[1]), (0, -1)) for _ in range(info_grid.shape[0])]
all_edges = top_edge + right_edge + bot_edge + left_edge

ENERGY_DICT = {}
for idx, starting_info in enumerate(all_edges):
    percent = 100 * (idx + 1) / len(all_edges)
    print(f"{percent:2.2f} %")

    beam_dict = defaultdict(list)
    beam_dict[starting_info].append(starting_info)
    determine_beams(info_grid, beam_dict, set())
    energy = determine_energy_level(beam_dict, (0, 0), add(info_grid.shape, (-1, -1)))

    ENERGY_DICT[starting_info[0]] = energy

# pprint(ENERGY_DICT, sort_dicts=False)
print(max(ENERGY_DICT.values()))

# point_traversals = paint1(info_grid, beam_dict)

# Part 1
# 6975 - answer is too low
# 6978 - is the right answer

# Part 2
# 7315 - answer is the right answer
