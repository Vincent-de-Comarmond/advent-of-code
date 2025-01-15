from collections import defaultdict
from enum import Enum
from functools import lru_cache
from itertools import permutations, product
from sys import argv


class KeyPad(Enum):
    """Enum class describing the different kinds of keypads and their relative locations"""

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
    """
    Given the target key lists all optimal ways to move there from the current key
    :param input_keypad: KeyPad in use
    :type input_keypad: KeyPad
    :param target: Target key
    :type target: str
    :param current:  Current key, defaults to "A"
    :type current: str, optional
    :return: Set of possible directional movements to get from the current key to the target key
    :rtype: set[str]
    """
    keypad = input_keypad.value
    current_loc, next_loc = keypad[current], keypad[target]
    dy, dx = next_loc[0] - current_loc[0], next_loc[1] - current_loc[1]

    vert = "^" * -dy if dy < 0 else "v" * dy
    horiz = "<" * -dx if dx < 0 else ">" * dx
    possible_keypresses = list(map("".join, permutations(vert + horiz)))

    diffs = {"<": (0, -1), "^": (-1, 0), ">": (0, 1), "v": (1, 0)}
    combinations = set()
    for next_keypress in possible_keypresses:
        (y, x), bad = current_loc, False

        for _c in next_keypress:
            dy, dx = diffs[_c]
            y, x = y + dy, x + dx
            if (y, x) == keypad["NULL"]:
                break
        else:
            combinations.add(next_keypress)
    return set(filter(lambda _: len(_) == min(map(len, combinations)), combinations))


@lru_cache(maxsize=None)
def seq2seq(
    input_keypad: KeyPad,
    target_seq: str,
    current: str = "A",
    accum: None | tuple[frozenset[str]] = None,
) -> tuple[frozenset[str]]:
    """
    Returns optimal movements to make to enter the specified sequence on the specified keypad
    Optimal movements are described in a tuple of key-by-key movments. Each element of the tuple is a frozenset of optimal equivalents.
    If no current key is given assumes "A"

    :param input_keypad: KeyPad in use
    :type input_keypad: KeyPad
    :param target_seq: Sequence to enter on input_keypad
    :type target_seq: str
    :param current: Current location on input_keypad, defaults to "A"
    :type current: str, optional
    :param accum: accumulator for possible movement sequences, defaults to None
    :type accum: None|tuple[frozenset[str]], optional
    :return: Tuple containing frozenset of optimal equivalent keypresses to make to get to the key (by index) of the input sequence
    :rtype: tuple[frozenset[str]]
    """

    keypad = input_keypad.value
    accum = tuple() if accum is None else accum
    if len(target_seq) == 0:
        return tuple(frozenset(seq + "A" for seq in fs) for fs in accum)
    next_moves = next_key(input_keypad, target_seq[0], current)

    return seq2seq(
        input_keypad, target_seq[1:], target_seq[0], accum + (frozenset(next_moves),)
    )


@lru_cache
def optimal_move_matrix(input_keypad: KeyPad) -> dict[tuple[str, str], frozenset[str]]:
    """
    Makes optimal move matrix for all transitions of the given input_keypad

    :param input_keypad: KeyPad in use
    :type input_keypad: KeyPad
    :return: Dictionary with start->end input_keys as keys and optimal movements as values
    :rtype: dict[tuple[str, str], frozenset[str]]
    """

    matrix: dict[tuple[str, str], frozenset[str]] = dict()
    for start in input_keypad.value:
        if start == "NULL":
            continue

        for end in input_keypad.value:
            if end == "NULL":
                continue
            matrix[start, end] = seq2seq(input_keypad, end, start)[0]

    # We can decide what the real optimal levels are by looking at future levels
    dirs = KeyPad.DIRECTION_KEYS
    filtered_matrix: dict[tuple[str, str], frozenset[str]] = dict()
    for k, sequences in matrix.items():
        seq_dict = dict()
        for seq in sequences:
            seq_dict[seq] = "".join([min(_, key=len) for _ in seq2seq(dirs, seq)])
        min_seq_len = min([len(_) for _ in seq_dict.values()])
        filtered_matrix[k] = frozenset(
            (k for k, v in seq_dict.items() if len(v) == min_seq_len)
        )

    return matrix, filtered_matrix


def subseq_solve(
    target_sequences: list[dict[tuple[str, str], int]],
    depth: int,
    keypad: KeyPad = KeyPad.NUMERIC_KEYS,
) -> dict[tuple[str, str], int]:
    """
    Solves a target sequence by breaking it down into numbers of keypress pairs

    :param target_sequences: list of optimal target sequences.
        Each a dictionary containing keypress pairs  as keys and the nubmer of these subsequences in the target sequence as values
    :type target_sequences: list[dict[tuple[str,str],int]]
    :param depth: How many recursions to do
    :type depth: int
    :param keypad: The keypad in use, defaults to KeyPad.NUMERIC_KEYS
    :type keypad: KeyPad, optional
    :return: The dictionary of keypress pairs and the number of those keypress pairs which is minimal to recreate the target sequence
    :rtype: dict[tuple[str, str], int]
    """

    print(f"\tResolving for depth: {depth}")
    if depth == 0:
        return dict(min(target_sequences, key=lambda _: sum(_.values())))

    next_level = list()
    for target in target_sequences:
        following_sequences = list()

        for seq, num in target.items():
            subsequent_seq = optimal_move_matrix(keypad)[seq]
            following_sequences.append([(nxt, num) for nxt in subsequent_seq])

        for option in product(*following_sequences):
            following = defaultdict(int)
            for seq, num in option:
                t = "A" + seq
                for a, b in [(t[i], t[i + 1]) for i in range(len(seq))]:
                    following[a, b] += num
            next_level.append(following)

    fewest_keypresses = min((sum(_.values()) for _ in next_level))
    optimal = [_ for _ in next_level if sum(_.values()) <= fewest_keypresses]
    return subseq_solve(optimal, depth - 1, keypad=KeyPad.DIRECTION_KEYS)


def determine_input_score(target_sequence: str, depth: int) -> int:
    """
    Determines the "score" for a given input sequence

    :param target_sequence: The target sequence
    :type target_sequence: str
    :param depth: The number of keypads in use
    :type depth: int
    :return: The resulting score
    :rtype: int
    """
    targ = "A" + target_sequence
    seed = [{(targ[i], targ[i + 1]): 1 for i in range(len(target_sequence))}]
    human_input = subseq_solve(seed, depth, keypad=KeyPad.NUMERIC_KEYS)
    human_input_length = sum(human_input.values())
    numeric_code = int(target_sequence[:-1])

    print(f"For {target_sequence}, adding {numeric_code} * {human_input_length}")
    return numeric_code * human_input_length


def main(input_fp: str, depth: int) -> int:
    """
    Reads the input file and determines the total score for all of the inputs added together
    :param input_fp: File path to input file
    :type input_fp: str
    :param depth: The number of keypads in use
    :type depth: int
    :return: Total score
    :rtype: int
    """
    accumulator: int = 0
    with open(input_fp, "r") as flin:
        for ln in flin:
            accumulator += determine_input_score(ln.strip(), depth)
    return accumulator


if __name__ == "__main__":
    print(main(argv[1], 3))
    # 157230 is the right answer for part 1
    print(main(argv[1], 26))
    # 195969155897936 is the right answer for part 2
