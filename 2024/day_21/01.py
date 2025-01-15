from enum import Enum
from functools import lru_cache
from itertools import permutations
from sys import argv

DIFFERENCES = {"<": (0, -1), "^": (-1, 0), ">": (0, 1), "v": (1, 0)}


class KeyPad(Enum):
    NUMERIC_KEYS = {
        "7": (0, 0),
        "8": (0, 1),
        "9": (0, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "1": (2, 0),
        "2": (2, 1),
        "3": (2, 2),
        "NULL": (3, 0),
        "A": (3, 2),
        "0": (3, 1),
    }

    DIRECTION_KEYS = {
        "NULL": (0, 0),
        "^": (0, 1),
        "A": (0, 2),
        "<": (1, 0),
        "v": (1, 1),
        ">": (1, 2),
    }


@lru_cache(maxsize=None)
def next_key(input_keypad: KeyPad, target: str, current: str = "A") -> set[str]:

    keypad = input_keypad.value
    current_loc, next_loc = keypad[current], keypad[target]
    dy, dx = next_loc[0] - current_loc[0], next_loc[1] - current_loc[1]

    vert = "^" * -dy if dy < 0 else "v" * dy
    horiz = "<" * -dx if dx < 0 else ">" * dx
    possible_keypresses = list(map("".join, permutations(vert + horiz)))

    combinations = set()
    for next_keypress in possible_keypresses:
        (y, x), bad = current_loc, False

        for _c in next_keypress:
            dy, dx = DIFFERENCES[_c]
            y, x = y + dy, x + dx
            if (y, x) == keypad["NULL"]:
                break
        else:
            combinations.add(next_keypress)
    return set(filter(lambda _: len(_) == min(map(len, combinations)), combinations))


def seq2seq(
    input_keypad: KeyPad,
    target_seq: str,
    current: str = "A",
    accum: None | frozenset[str] = None,
) -> frozenset[str]:

    keypad = input_keypad.value
    accum = frozenset({""}) if accum is None else accum
    if len(target_seq) == 0:
        return accum
    target, rest = target_seq[0], target_seq[1:]
    next_moves = next_key(input_keypad, target, current)

    combinations = set()
    for sequence in accum:
        for next_move in next_moves:
            combinations.add(sequence + next_move + "A")

    return seq2seq(input_keypad, rest, target, frozenset(combinations))


def determine_all_possible_inputs(target_seq: str) -> set[str]:

    NUMERIC_KEYS, DIRECTION_KEYS = KeyPad.NUMERIC_KEYS, KeyPad.DIRECTION_KEYS
    r1: set[str] = seq2seq(NUMERIC_KEYS, target_seq)
    min_r1 = min(map(len, r1))
    r1 = set(filter(lambda _: len(_) == min_r1, r1))
    # print(f"R1 lengths: {min_r1}")
    # print(f"Computed robot 1's inputs. Input possibilities: {len(r1)}")

    r2: set[str] = {_ for i in r1 for _ in seq2seq(DIRECTION_KEYS, i)}
    min_r2 = min(map(len, r2))
    r2 = set(filter(lambda _: len(_) == min_r2, r2))
    # print(f"R2 lengths: {min_r2}")
    # print(f"Computed robot 2's inputs. Input possibilities: {len(r2)}")

    # r3: set[str] = {_ for i in r2 for _ in seq2seq(DIRECTION_KEYS, i)}
    # min_r3 = min(map(len, r3))
    # r3 = set(filter(lambda _: len(_) == min_r3, r3))
    # print(f"R3 lengths: {min_r3}")
    # print(f"Computed robot 3's inputs. Input possibilities: {len(r3)}")

    me: set[str] = {_ for i in r2 for _ in seq2seq(DIRECTION_KEYS, i)}
    min_me = min(map(len, me))
    # print(f"HUMAN lengths: {min_me}")
    # print(f"Computed humans inputs. Input possibilities: {len(me)}")
    for sequence in me:
        if len(sequence) == min_me:
            return sequence


def determine_input_score(target_sequence: str) -> int:
    human_input = determine_all_possible_inputs(target_sequence)
    numeric_code = int(target_sequence[:-1])

    print(f"For {target_sequence}, adding {numeric_code} * {len(human_input)}")
    return numeric_code * len(human_input)


def main(input_fp: str) -> int:
    accumulator: int = 0
    with open(input_fp, "r") as flin:
        for ln in flin:
            accumulator += determine_input_score(ln.strip())
    return accumulator


if __name__ == "__main__":
    print(main(argv[1]))
    # 157230 is the right answer for part 1
