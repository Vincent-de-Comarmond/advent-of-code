from collections import defaultdict
from pprint import pp
import sys


def get_regions(
    region: set[tuple[int, int]], marked: None | list[set[tuple[int, int]]] = None
) -> list[set[tuple[int, int]]]:

    if marked is None:
        marked = list()

    if len(region) == 0:
        return marked

    current_marked = set()
    row, col = region.pop()
    current_marked.add((row, col))

    while True:
        tmp = set()
        for r, c in current_marked:
            for pt in [(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)]:
                if pt not in current_marked and pt in region:
                    tmp.add(pt)
                    region.remove(pt)
        if len(tmp) == 0:
            break
        current_marked |= tmp
    marked.append(current_marked)
    return get_regions(region, marked)


def __get_outside(region: set[tuple[int, int]]) -> set[tuple[float | int, float | int]]:
    outside = set()
    for r, c in region:
        for rr, cc in [(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)]:
            if (rr, cc) not in region:
                outside.add(((r + rr) / 2, (c + cc) / 2))
    return outside


def __edge_parity(
    region: set[tuple[int, int]], edge: tuple[float | int, float | int]
) -> int:
    block = tuple(map(int, edge))
    return -1 if block in region else 1


def __get_sides(
    region: set[tuple[int, int]],
    region_outside: set[tuple[float | int, float | int]],
    sides: None | list[set[tuple[int, int]]] = None,
):
    if sides is None:
        sides = list()

    if len(region_outside) == 0:
        return sides

    current_side = set()
    row, col = region_outside.pop()
    horizontal = row % 1 == 0.5
    parity = __edge_parity(region, (row, col))
    current_side.add((row, col))

    while True:
        tmp = set()
        for r, c in current_side:
            edges = [(r, c - 1), (r, c + 1)] if horizontal else [(r - 1, c), (r + 1, c)]
            for edge in edges:
                if edge not in current_side and edge in region_outside:
                    _parity = __edge_parity(region, edge)
                    if parity == _parity:
                        tmp.add(edge)
                        region_outside.remove(edge)
        if len(tmp) == 0:
            break
        current_side |= tmp
    sides.append(current_side)
    return __get_sides(region, region_outside, sides)


def get_sides(region: set[tuple[int, int]]) -> list[set[tuple[int, int]]]:
    outside = __get_outside(region)
    return __get_sides(region, outside)


def get_region_side_area_cost(region: set[tuple[int, int]]) -> dict[str, int]:
    area = len(region)
    sides = get_sides(region)
    return {
        "area": area,
        "sides": sides,
        "num_sides": len(sides),
        "cost": area * len(sides),
    }


if __name__ == "__main__":

    grid = defaultdict(set)
    with open(sys.argv[1], "r") as txtin:
        for row, line in enumerate(txtin):
            for col, char in enumerate(line.rstrip()):
                grid[char].add((row, col))

    total_cost = 0
    for plant_type, plant_grid in grid.items():
        # print(f"Calculating for plant type: {plant_type}")
        regions = get_regions(plant_grid)
        for region in regions:
            cost = get_region_side_area_cost(region)
            # pp(cost)
            total_cost += cost["cost"]

    print(f"Total cost: {total_cost}")
    # 1359028 is the right answer for part 1
    # Part 2
    # 834546 is too low
    # 839780 is correct for part 2
