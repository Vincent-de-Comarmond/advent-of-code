# stdlib
from dataclasses import dataclass
from pprint import pprint
from sys import argv, setrecursionlimit

# 3rd party
import numpy as np

setrecursionlimit(1000000)


@dataclass(eq=True, frozen=True)
class Point:
    row: int
    col: int
    nesw: int
    burndown: int
    score: int


def load_input(txt_file: str) -> np.ndarray:
    racetrack: list[list[str]] = []
    with open(txt_file, "r") as txtin:
        racetrack = [[_ for _ in line if _ != "\n"] for line in txtin]
    return np.array(racetrack)


def get_action_space(racetrack: np.ndarray, point: Point) -> set[Point]:
    r, c = point.row, point.col
    neighbours = set()
    _shape = racetrack.shape
    for row, col, nesw in [(r - 1, c, 0), (r, c + 1, 1), (r + 1, c, 2), (r, c - 1, 3)]:
        if any((row < 0, col < 0, row >= _shape[0], col >= _shape[1])):
            continue
        if racetrack[row, col] not in (".", "E"):
            continue

        burndown = 1 if nesw == point.nesw else 1001
        neighbours.add(Point(row, col, nesw, burndown, point.score + burndown))

    return neighbours


def get_start(racetrack: np.ndarray) -> tuple[int, int, tuple[int, int]]:
    row, col = (_[0] for _ in np.where(racetrack == "S"))
    return Point(row, col, 1, 1, 0)


def solve(
    racetrack: np.ndarray, active: set[Point], burnt: None | set[tuple[int, int]] = None
) -> int:
    new_active = set()
    burnt = set() if burnt is None else burnt

    # Reduce recursion and recursive stack frame size by burning as much time
    # as possible for each iteration.
    # Python does not optimize tail-call recursion, so even something uninvolved
    # can blow up. Then again, I'm probably not organizing my stack correctly
    timelapse = min((_.burndown for _ in active))

    for old_pt in active:
        r, c, n = old_pt.row, old_pt.col, old_pt.nesw
        point = Point(r, c, n, old_pt.burndown - timelapse, old_pt.score)
        if point.burndown == 0:
            location = (point.row, point.col)
            burnt.add(location)
            neighbours = get_action_space(racetrack, point)
            for neighbour in neighbours:
                if racetrack[neighbour.row, neighbour.col] == "E":
                    return neighbour.score

                if (neighbour.row, neighbour.col) not in burnt:
                    new_active.add(neighbour)
        else:

            new_active.add(point)

    return solve(racetrack, new_active, burnt)


if __name__ == "__main__":
    racetrack = load_input(argv[1])
    start = get_start(racetrack)
    low_score = solve(racetrack, {start})

    print(low_score)

    # 186576 is too high
    # 98484 is the right answer for part 1
