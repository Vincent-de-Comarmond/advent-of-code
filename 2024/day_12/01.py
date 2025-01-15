from collections import defaultdict
from pprint import pp
import sys


def get_regions(
    region: set[tuple[int, int]], marked: list[set[tuple[int, int]]]
) -> list[set[tuple[int, int]]]:

    if len(region) == 0:
        return marked

    copy = region.copy()
    current_marked = set()

    row, col = copy.pop()
    current_marked.add((row, col))

    while True:
        tmp = set()
        for r, c in current_marked:
            for pt in [(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)]:
                if pt not in current_marked and pt in copy:
                    tmp.add(pt)
                    copy.remove(pt)
        if len(tmp) == 0:
            break
        current_marked |= tmp
    marked.append(current_marked)
    return get_regions(copy, marked)


def get_region_peri_area_cost(region: set[tuple[int, int]]) -> dict[str, int]:
    area = 0
    peri = 0

    for r, c in region:
        area += 1
        peri += 4

        for rr, cc in [(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)]:
            if (rr, cc) in region:
                peri -= 1

    cost = area * peri
    return {"area": area, "peri": peri, "cost": cost}


if __name__ == "__main__":

    grid = defaultdict(set)
    with open(sys.argv[1], "r") as txtin:
        for row, line in enumerate(txtin):
            for col, char in enumerate(line.rstrip()):
                grid[char].add((row, col))

    total_cost = 0
    for plant_type, plant_grid in grid.items():
        print(f"Calculating for plant type: {plant_type}")
        regions = get_regions(plant_grid, list())
        for region in regions:
            cost = get_region_peri_area_cost(region)
            pp(cost)
            total_cost += cost["cost"]

    print(f"Total cost: {total_cost}")
    # 1359028 is the right answer for part 1
