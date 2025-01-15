from functools import lru_cache
import sys
from typing import Callable


def get_program(filepath: str) -> dict[str, int | list[int]]:
    res = dict()
    with open(filepath, "r") as txtin:
        for line in txtin:
            tmp = line.split(":")
            if "Register" in line:
                res[tmp[0][-1].lower()] = int(tmp[1])

            if "Program" in line:
                res["program"] = tuple(map(int, tmp[1].split(",")))
    a, b, c = res["a"], res["b"], res["c"]
    prog = res["program"]
    return a, b, c, prog


def compile_program(b: int, c: int, program: list[int]) -> Callable[[int], tuple[int]]:

    def inner(
        a: int, b: int = b, c: int = c, pointer: int = 0, accum: None | list[int] = None
    ) -> tuple[int]:
        accum = list() if accum is None else accum

        if pointer < 0 or pointer >= len(program):
            return tuple(accum)

        instruction = program[pointer]
        oper = program[pointer + 1]
        combo = a if oper == 4 else b if oper == 5 else c if oper == 6 else None
        combo = oper if oper <= 3 else combo
        p2 = pointer + 2

        match instruction:
            case 0:
                return inner(int(a / 2**combo), b, c, p2, accum)
            case 1:
                return inner(a, b ^ oper, c, p2, accum)
            case 2:
                return inner(a, combo % 8, c, p2, accum)
            case 3:
                return (
                    inner(a, b, c, oper, accum) if a != 0 else inner(a, b, c, p2, accum)
                )
            case 4:
                return inner(a, b ^ c, c, p2, accum)
            case 5:
                return inner(a, b, c, p2, accum + [combo % 8])
            case 6:
                return inner(a, int(a / 2**combo), c, p2, accum)
            case 7:
                return inner(a, b, int(a / 2**combo), p2, accum)

    return inner


def get_length_estimates(
    compiled_func: Callable[[int], tuple[int]], target: tuple[int], _guess: int = 0
) -> tuple[int]:

    result = compiled_func(_guess)

    if len(result) < len(target):
        _guess += _guess + 1
        return get_length_estimates(compiled_func, target, _guess)
    elif len(result) > len(target):
        _guess -= _guess + 2
        return get_length_estimates(compiled_func, target, _guess)

    _min, _max = _guess, _guess
    incr = _guess // 2

    while True:
        result = compiled_func(_min)
        if len(result) == len(target):
            if incr == 1:
                break
            _min -= incr
        else:
            _min += incr
            incr = max(1, incr // 2)

    incr = _guess // 2
    while True:
        result = compiled_func(_max)
        if len(result) == len(target):
            if incr == 1:
                break
            incr *= 2
            _max += incr
        else:
            _max -= incr
            incr = max(1, incr // 4)

    return _min, _max


def get_digit_max(
    compiled_func: Callable[[int], tuple[int]],
    estimate: int,
    increment: int,
    target: tuple[int],
    idx: int,
    lb: int,
    ub: int,
):
    compiled = compiled_func
    targ = target[idx:]
    inc0 = increment

    count = 0
    while True:
        count += 1
        if count % 10000 == 0:
            print(increment)
            print(estimate)
            count = 0

        result = compiled_func(estimate)
        increment = max(1, (increment * 99) // 100)
        if len(result) > len(target):
            estimate -= increment
            continue
        if len(result) < len(target):
            estimate += increment
            continue

        if result[idx:] == targ and compiled(estimate + 1)[idx:] != targ:
            break
        if result[idx:] != targ and compiled(estimate - 1)[idx:] == targ:
            estimate -= 1
            break

        estimate += increment if result[idx:] == targ else -increment
        if increment == 1:
            increment = inc0 + 1
    return estimate


def get_digit_min(
    compiled_func: Callable[[int], tuple[int]],
    estimate: int,
    increment: int,
    target: tuple[int],
    idx: int,
    lb: int,
    ub: int,
):
    compiled = compiled_func
    targ = target[idx:]
    inc0 = increment

    count = 0
    while True:
        count += 1
        if count % 10000 == 0:
            print(increment)
            print(estimate)
            count = 0

        if estimate < lb:
            return lb
        if estimate > ub:
            return ub

        result = compiled_func(estimate)
        increment = max(1, (increment * 99) // 100)
        if len(result) > len(target):
            estimate -= increment
            continue
        if len(result) < len(target):
            estimate += increment
            continue

        if result[idx:] == targ and compiled(estimate - 1)[idx:] != targ:
            break
        if result[idx:] != targ and compiled(estimate + 1)[idx:] == targ:
            estimate += 1
            break

        estimate += -increment if result[idx:] == targ else increment
        if increment == 1:
            increment = inc0 + 1
    return estimate


def solve_from_tail(
    compiled_func: Callable[[int], tuple[int]],
    target: tuple[int],
    _min_allowed: int,
    _max_allowed: int,
    idx: None | int = None,
):

    idx = len(target) - 1 if idx is None else idx
    targ = target[idx]
    compiled = compiled_func
    min0, max0 = _min_allowed, _max_allowed
    step = max(1, (max0 - min0) // 10)

    print(f"Searching index: {idx}")

    if compiled(min0)[idx] == targ and compiled(max0)[idx] == targ:
        return _min_allowed, _max_allowed

    for guess in range(min0, max0 + step, step):
        result = compiled(guess)
        if result[idx:] != target[idx:]:
            continue

        _min = get_digit_min(compiled, guess, step, target, idx, min0, max0)
        _max = get_digit_max(compiled, guess, step, target, idx, min0, max0)

        if idx <= 0 and _max > _min:
            return _min, _max
        elif _max > _min:
            soln = solve_from_tail(compiled, target, _min, _max, idx - 1)
            if soln is not None:
                return soln


if __name__ == "__main__":
    INPUT_FP = sys.argv[1]  #  "./input.txt"  # sys.argv[1]
    a, b, c, prog = get_program(INPUT_FP)
    compiled = lru_cache(compile_program(b, c, prog))

    _min, _max = get_length_estimates(compiled, prog)

    lb, ub = solve_from_tail(compiled, prog, _min, _max, len(prog) - 1)
    print(f"Search range: {lb}-{ub} = {ub-lb}")
    print(lb, ub)

    for a in range(lb, ub + 1):
        if a % 100000 == 0:
            print(a)
            print("{:.2f} %".format((a - lb) / 100000))

        output = compiled(a)
        if output == prog:
            print(f"An input of A={a} should cause the program to recreate itself")
            break

    print(a)
    print(",".join(map(str, compiled(a))))
