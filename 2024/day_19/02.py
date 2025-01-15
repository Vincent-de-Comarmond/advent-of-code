# stdlib
from functools import lru_cache, partial
from sys import argv


def load_input(filepath: str) -> dict[frozenset[str], list[str]]:

    hit_blank = False
    arrangements = list()
    with open(filepath, "r") as txtin:
        for ln in txtin:
            stripped = ln.strip()
            if stripped == "":
                hit_blank = True
            elif hit_blank:
                arrangements.append(stripped)
            else:
                towels = frozenset(map(str.strip, stripped.split(",")))
    return towels, arrangements


@lru_cache(maxsize=None)
def get_grand_subset(towels: frozenset[str], target: str) -> frozenset[str]:
    return frozenset((_ for _ in towels if _ in target))


@lru_cache(maxsize=None)
def get_towel_subset(towels: frozenset[str], start: str) -> frozenset[str]:
    return frozenset((_ for _ in towels if _.startswith(start)))


@lru_cache(maxsize=None)
def count_possible_arrangements(desired: str, towels: frozenset[str]) -> int:

    if len(desired) == 0:
        return 1

    ways = 0
    towel_subset = get_towel_subset(towels, desired[0])
    for towel in towel_subset:
        if desired.startswith(towel):
            ways += count_possible_arrangements(desired[len(towel) :], towels)
    return ways


def main(file_path: str) -> None:
    towels, desired_arrangements = load_input(file_path)

    total = 0
    for idx, desired_arrangement in enumerate(desired_arrangements):
        grand_subset = get_grand_subset(towels, desired_arrangement)
        possibilities = count_possible_arrangements(desired_arrangement, grand_subset)
        print(f"Arrangment: {idx:03d}, possibilities: {possibilities}")
        total += possibilities
    print(total)
    

if __name__ == "__main__":
    main(argv[1])
    # 650354687260341 is the right answer for part 2
