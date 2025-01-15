from collections import Counter, defaultdict
from copy import copy
from functools import lru_cache, partial
from pprint import pp
from sys import argv

Point = tuple[int, int]
Track = frozenset[Point]


def load_input(txt_file: str) -> tuple[Point, Point, Track, Track]:
    track = set()
    walls = set()
    start, end = None, None

    with open(txt_file, "r") as txtin:
        for row, line in enumerate(txtin):
            cleaned = line.strip()
            for col, char in enumerate(cleaned):
                if char in ("S", "E", "."):
                    track.add((row, col))
                else:
                    walls.add((row, col))

                end = (row, col) if char == "E" else end
                start = (row, col) if char == "S" else start

    return start, end, frozenset(track), frozenset(walls)


@lru_cache(maxsize=None)
def get_neighbours(
    track: Track, point: Point, min_rad: int = 1, max_rad: int = 1
) -> set[tuple[Point, int]]:
    y, x = point
    neighbours = set()
    for dy in range(-max_rad, max_rad + 1):
        for dx in range(-max_rad, max_rad + 1):
            hamming = abs(dx) + abs(dy)
            if hamming < min_rad or max_rad < hamming:
                continue

            ngh = y + dy, x + dx
            if ngh in track:
                neighbours.add((ngh, hamming))

    return neighbours


def get_best(active_routes: set[Point, int]) -> int:
    return min(map(lambda _: _[-1][-1], active_routes))


def solve_optimally(
    track: Track, start: Point, end: Point
) -> tuple[int, dict[Point, int]]:

    nearest_neighbours = partial(get_neighbours, track)

    route: None | tuple[tuple[Point, int], ...] = None
    routes = {((start, 0),)}
    while len(routes) > 0:
        route = routes.pop()
        visited = {_[0] for _ in route}
        point, time = route[-1]

        if point == end:
            break

        neighbours = {_ for _ in nearest_neighbours(point) if _[0] not in visited}
        for ngh in neighbours:
            routes.add(route + ((ngh[0], time + 1),))

    best_time = route[-1][-1]
    time_map = {_[0]: best_time - _[1] for _ in route}
    return best_time, time_map


def solve_with_cheat(
    track: Track, start: Point, end: Point, min_time_saved: int, cheat_length: int
) -> dict[int, int]:

    best_time, route_map = solve_optimally(track, start, end)
    max_finish_time = best_time - min_time_saved
    print(f"Found best (only) route with time: {best_time}")

    results = defaultdict(int)
    routes = {((start, False, 0),)}  # Read point, used_cheat, track_time
    nearest_neighbours = partial(get_neighbours, track)
    cheat_options = partial(get_neighbours, track, min_rad=2, max_rad=cheat_length)

    counter = 0

    while get_best(routes) < max_finish_time and len(routes) > 0:
        counter += 1

        route = routes.pop()
        point, used_cheat, time = route[-1]

        if counter % 100000 == 0:
            print(f"Iteration: {counter}")
            print(f"Point: {point}")
            print(f"Routes: {len(routes)}")
            if point in route_map:
                print(f"Time to go: {route_map[point]} / {best_time}")

        if used_cheat and point in route_map:
            finish_time = time + route_map[point]
            if finish_time <= max_finish_time:
                results[finish_time] += 1
        else:
            if max_finish_time < time:
                continue

            if point == end:
                print(f"Found newly possible route with time: {time}")
                results[time] += 1
                continue

            visited = {_[0] for _ in route}
            neighbours = {_ for _ in nearest_neighbours(point) if _[0] not in visited}
            for ngh in neighbours:
                routes.add(route + ((ngh[0], used_cheat, time + 1),))

            if not used_cheat:
                cheats = {_ for _ in cheat_options(point) if _[0] not in neighbours}
                for cheat in cheats:
                    routes.add(route + ((cheat[0], True, time + cheat[1]),))
    time_savings = {best_time - k: v for k, v in results.items()}
    return dict(sorted(time_savings.items()))


if __name__ == "__main__":
    FILE_PATH = argv[1]
    CHEAT_LENGTH = int(argv[2])
    MIN_TIME_SAVING = int(argv[3])

    start, end, track, walls = load_input(FILE_PATH)

    cheat_solns = solve_with_cheat(track, start, end, MIN_TIME_SAVING, CHEAT_LENGTH)
    print(f"Number of cheats which save you {MIN_TIME_SAVING} or more seconds:")
    print(sum(cheat_solns.values()))
    # 993178 is the right answer for part 2
