from sys import argv


def load_inputs(input_fp: str):
    isnew = True
    lines: list[str] = list()
    locks_rep: list[tuple[int]] = list()
    keys_rep: list[tuple[int]] = list()

    with open(input_fp, "r") as txtin:
        lines = txtin.read().splitlines()

    locks_and_keys = [lines[i : i + 7] for i in range(0, len(lines), 8)]
    locks_rep = [_[1:] for _ in locks_and_keys if _[0] == "#####"]
    keys_rep = [_[:-1] for _ in locks_and_keys if _[-1] == "#####"]

    locks = list()
    for lock in locks_rep:
        tmp = [0, 0, 0, 0, 0]
        for pinset in lock:
            for idx, c in enumerate(pinset):
                tmp[idx] += 1 if c == "#" else 0
        locks.append(tuple(tmp))

    keys = list()
    for key in keys_rep:
        tmp = [0, 0, 0, 0, 0]
        for pinset in key:
            for idx, c in enumerate(pinset):
                tmp[idx] += 1 if c == "#" else 0
        keys.append(tuple(tmp))

    return locks, keys


def check_no_overlap(
    lock: list[tuple[int]], key: list[tuple[int]], height: int = 5
) -> bool:

    for idx, pinheight in enumerate(lock):
        if key[idx] + pinheight > height:
            return False

    return True


def main_part1(input_fp: str) -> int:
    locks, keys = load_inputs(input_fp)
    possibilities = 0
    for lock in locks:
        for key in keys:
            possibilities += check_no_overlap(lock, key)
    return possibilities


if __name__ == "__main__":

    part1_possibilities = main_part1(argv[1])
    print(f"Part 1 key possibilities: {part1_possibilities}")
    # 3508 is the right answer for part 1
