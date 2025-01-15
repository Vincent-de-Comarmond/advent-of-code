# stdlib
from copy import deepcopy
from dataclasses import dataclass
from pprint import pp
from sys import argv

# 3rd party
import numpy as np


@dataclass(eq=True, frozen=True)
class Point:
    row: int
    col: int
    nesw: int
    burndown: int
    score: int
    allow_turn: bool


def load_input(txt_file: str) -> np.ndarray:
    racetrack: list[list[str]] = []
    with open(txt_file, "r") as txtin:
        racetrack = [[_ for _ in line if _ != "\n"] for line in txtin]
    return np.array(racetrack)


def get_action_space(racetrack: np.ndarray, point: Point) -> set[Point]:
    r, c, n, s = point.row, point.col, point.nesw, point.score
    dirs = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}

    neighbours = set()
    if point.allow_turn:
        for dn in (-1, 1):
            new_dir = (n + dn) % 4
            # DO NOT CHANGE DIRECTION TO FACE WALL
            dy, dx = dirs[new_dir]
            y, x = r + dy, c + dx
            if racetrack[y, x] != "#":
                neighbours.add(Point(r, c, new_dir, 1000, s + 1000, False))

    dy, dx = dirs[n]
    y, x = r + dy, c + dx
    if racetrack[y, x] in (".", "E"):
        neighbours.add(Point(y, x, n, 1, s + 1, True))
    return neighbours


def solve_part1(
    racetrack: np.ndarray, active: set[Point], target: set[tuple[int, int, int]]
) -> tuple[int, set[tuple[int, int]]]:
    burnt = set()

    while len(active) > 0:
        timelapse = min((_.burndown for _ in active))
        new_active = set()
        winning_score = float("inf")
        for old in active:
            r, c, n, s = old.row, old.col, old.nesw, old.score
            point = Point(r, c, n, old.burndown - timelapse, s, old.allow_turn)
            if point.burndown == 0:
                burnt.add((r, c, n))
                for ngh in get_action_space(racetrack, point):
                    r, c, n = ngh.row, ngh.col, ngh.nesw
                    if (r, c, n) in target:
                        winning_score = min(winning_score, ngh.score)
                    if (r, c, n) not in burnt:
                        new_active.add(ngh)
            else:
                new_active.add(point)

        if winning_score != float("inf"):
            return winning_score, burnt
        active = new_active


def print_ndarray(input_array: np.ndarray) -> None:
    print("\n".join(["".join([str(_) for _ in line]) for line in input_array]))


def solve_part2(
    racetrack: np.ndarray,
    routes: set[tuple[Point]],
    target: set[tuple[int, int, int]],
    truncate_score: int,
):

    winners = set()
    winning_score = float("inf")
    routes_truncated = 0
    rounds = -1
    best = dict()

    while len(routes) > 0:
        rounds += 1
        new_routes = set()
        dt = min((_[-1].burndown for _ in routes))

        for route in routes:
            old = route[-1]
            r, c, n, s = old.row, old.col, old.nesw, old.score
            point = Point(r, c, n, old.burndown - dt, s, old.allow_turn)
            best[r, c, n] = s

            min_score = min((_[-1].score for _ in routes))
            if min_score % 100 == 0:
                print(
                    "\n\t".join(
                        [
                            f"Round: {rounds}",
                            f"Min score: {min_score}",
                            f"Target score: {truncate_score}",
                            f"Number routes: {len(routes)}",
                        ]
                    )
                )

            if s > truncate_score:
                routes_truncated += 1
                if routes_truncated % 10 == 0:
                    print(f"Truncated {routes_truncated} routes")
                continue

            if point.burndown > 0:
                new_routes.add(route)
                continue

            neighbours = get_action_space(racetrack, point)
            for ngh in neighbours:
                r, c, n, s = ngh.row, ngh.col, ngh.nesw, ngh.score
                matched = best.get((r, c, n))

                if matched is not None:
                    if matched < s:
                        continue

                if (r, c, n) in target and winning_score <= winning_score:
                    winning_score = min(winning_score, s)
                    print(f"Found winning score of {winning_score}")
                    winners.add(route + (ngh,))
                else:
                    if s < winning_score:
                        new_routes.add(route + (ngh,))
        routes = new_routes

    return winners


if __name__ == "__main__":
    racetrack = load_input(argv[1])
    sy, sx = (_[0] for _ in np.where(racetrack == "S"))
    ey, ex = (_[0] for _ in np.where(racetrack == "E"))

    ##########
    # part 1 #
    ##########
    low_score1, burnt1 = solve_part1(
        racetrack, {Point(sy, sx, 1, 1, 0, True)}, {(ey, ex, _) for _ in range(4)}
    )
    print(low_score1)
    # # 186576 is too high
    # # 98484 is the right answer for part 1

    print(len(burnt1))

    #########
    # part2 #
    #########
    winning = solve_part2(
        racetrack,
        {(Point(sy, sx, 1, 1, 0, True),)},
        {(ey, ex, _) for _ in range(4)},
        low_score1,
    )
    legit_points = {(point.row, point.col) for route in winning for point in route}

    print(len(legit_points))
    # 531 is the right answer for part 2
