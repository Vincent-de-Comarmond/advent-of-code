# stdlib
from collections import defaultdict
from dataclasses import dataclass
from pprint import pp
from sys import argv
from typing import Generator

# 3rd party
import numpy as np

Point = tuple[int, int]


def load_input(txt_file: str) -> np.ndarray:
    racetrack: list[list[str]] = []
    with open(txt_file, "r") as txtin:
        racetrack = [[_ for _ in line if _ != "\n"] for line in txtin]
    return np.array(racetrack)


def get_start(racetrack: np.ndarray) -> Point:
    row, col = map(int, (_[0] for _ in np.where(racetrack == "S")))
    return row, col


def get_end(racetrack: np.ndarray) -> Point:
    row, col = map(int, (_[0] for _ in np.where(racetrack == "E")))
    return row, col


def get_neighbours(racetrack: np.ndarray, point: Point) -> set[tuple[Point]]:
    r, c = point
    neighbours = set()
    _shape = racetrack.shape

    # Normal Racing
    for row, col in [(r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)]:
        if any((row < 0, col < 0, row >= _shape[0], col >= _shape[1])):
            continue
        if racetrack[row, col] not in (".", "E", "C"):
            continue
        neighbours.add((row, col))
    return neighbours


def solve(racetrack: np.ndarray, start: Point, end: Point) -> int:
    active = {start: -1}
    burnt = set()
    time = -1  # To acount for intiialization step

    while len(active) > 0:
        point, time = min(active.items(), key=lambda _: _[1])
        _ = active.pop(point)  # Remove the minimum point from the active list

        if point == end:
            return time + 1

        burnt.add(point)
        neighbours = get_neighbours(racetrack, point) - burnt
        active |= {pt: time + 1 for pt in neighbours}


def determine_cheat_locations(racetrack: np.ndarray) -> list[Point]:
    cheat_locations = set()
    my, mx = racetrack.shape
    walls = list(zip(*map(np.ndarray.tolist, np.where(racetrack == "#"))))

    # Exclude all external walls
    walls = list(
        filter(lambda _: all((_[0] > 0, _[0] < my - 1, _[1] > 0, _[1] < mx - 1)), walls)
    )

    for y, x in walls:
        left, right = racetrack[y, x - 1], racetrack[y, x + 1]
        up, down = racetrack[y - 1, x], racetrack[y + 1, x]

        if left in (".", "S", "E") and right in (".", "S", "E"):
            cheat_locations.add((y, x))
            continue
        if up in (".", "S", "E") and down in (".", "S", "E"):
            cheat_locations.add((y, x))

    return sorted(cheat_locations)


def print_ndarray(input_array: np.ndarray) -> None:
    print("\n".join(["".join([str(_) for _ in line]) for line in input_array]))


def generate_cheat_possibilities(
    racetrack: np.ndarray,
) -> Generator[np.ndarray, None, None]:

    cheat_locations = determine_cheat_locations(racetrack)
    print(f"Cheat possibilities: {len(cheat_locations)}")
    for idx, location in enumerate(cheat_locations):
        if idx % 100 == 0:
            print(f"Computing possibility {idx+1}/{len(cheat_locations)}")
        copy = racetrack.copy()  # Shallow copy should be fine
        copy[location] = "C"
        yield copy


if __name__ == "__main__":
    racetrack = load_input(argv[1])
    start = get_start(racetrack)
    end = get_end(racetrack)
    # We need the base time to evaluate how good the cheats are
    base_time = solve(racetrack, start, end)

    time_savings = defaultdict(int)
    for cheat_track in generate_cheat_possibilities(racetrack):
        cheat_time = solve(cheat_track, start, end)
        time_saving = base_time - cheat_time
        time_savings[time_saving] += 1

    pp(dict(sorted(time_savings.items(), key=lambda _: (-_[1], _[0]))))

    better_eq_100ps_cheats = {k: v for k, v in time_savings.items() if k >= 100}

    print("Number of cheats of at least 100 picoseconds:")
    print(sum(better_eq_100ps_cheats.values()))
    # 1395 is the number of correct cheats for part 1
