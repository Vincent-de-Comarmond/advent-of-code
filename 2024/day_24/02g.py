from functools import lru_cache, partial
from itertools import combinations
from operator import add, and_, xor, or_
from sys import argv
from typing import Callable

BFunc = Callable[[int, int], int]


def _formalize_inputs(input_defs: list[str]) -> dict[str, int]:
    input_vals = dict()

    for ln in input_defs:
        node, val = map(str.strip, ln.split(":"))
        input_vals[node] = int(val)
    return input_vals


def _formalize_relationships(
    raw_relationships: list[str],
) -> dict[str, tuple[BFunc, str, str]]:
    _func_map = {"AND": and_, "XOR": xor, "OR": or_}
    output = dict()
    for ln in raw_relationships:
        parents, child = map(str.strip, ln.split("->"))
        parent1, func, parent2 = parents.split(" ")
        output[child] = (_func_map[func], *sorted((parent1, parent2)))
    return output


def _sort_relationships(
    inputs: dict[str, int],
    relationships: dict[str, tuple[BFunc, str, str]],
) -> dict[str, tuple[BFunc, str, str]]:

    sorted_relns = dict()
    outputs = dict()
    sort_keys = {xor: 0, and_: 1, or_: 2}

    for k, v in relationships.items():
        if v[1] in inputs and v[2] in inputs:
            sorted_relns[k] = v
    sorted_relns = dict(
        sorted(sorted_relns.items(), key=lambda _: (_[1][1:], sort_keys[_[1][0]]))
    )

    num_captured = len(sorted_relns) + len(outputs)
    while num_captured != len(relationships):
        pre = num_captured
        for k, v in relationships.items():
            if k in sorted_relns:
                continue

            _, parent1, parent2 = v
            have_parent1 = parent1 in inputs or parent1 in sorted_relns
            have_parent2 = parent2 in inputs or parent2 in sorted_relns

            if have_parent1 and have_parent2:
                if k.startswith("z") and k[1:].isdigit():
                    outputs[k] = v
                else:
                    sorted_relns[k] = v
        num_captured = len(sorted_relns) + len(outputs)
        if pre == num_captured:
            raise RecursionError("Not solvable")

    outputs = dict(sorted(outputs.items()))
    return sorted_relns | outputs


@lru_cache(maxsize=None)
def read_input(
    input_fp: str,
) -> tuple[dict[str, int], dict[str, tuple[BFunc, str, str]]]:
    input_defns: list[str] = list()
    relations: list[str] = list()

    with open(input_fp, "r") as flin:
        raw = flin.read().split("\n")

    part1_end = raw.index("")
    input_defns = raw[:part1_end]
    raw_relations = [_ for _ in raw[part1_end + 1 :] if "->" in _]

    inputs = _formalize_inputs(input_defns)
    relations = _formalize_relationships(raw_relations)
    relations = _sort_relationships(inputs, relations)
    return inputs, relations


def solve(
    inputs: dict[str, int], relationships: dict[str, tuple[BFunc, str, str]]
) -> tuple[dict[str, int], ...]:

    allout = inputs.copy()
    rel = _sort_relationships(inputs, relationships.copy())

    for child, (func, parent1, parent2) in rel.items():
        allout[child] = func(allout[parent1], allout[parent2])

    return allout, {k: v for k, v in sorted(allout.items()) if k.startswith("z")}


@lru_cache(maxsize=None)
def create_repr(input_num: int, max_symb: str) -> dict[str, int]:
    bin_list = [_ for _ in reversed(bin(input_num))]
    bin_list = bin_list[: bin_list.index("b")]

    output = dict()
    target_wires = [f"{max_symb[0]}{_:02d}" for _ in range(int(max_symb[1:]) + 1)]

    for idx, val in enumerate(target_wires):
        output[val] = int(bin_list[idx]) if idx < len(bin_list) else 0

    return output


@lru_cache(maxsize=None)
def create_input(max_symb: str, idx: int | None) -> dict[str, int]:
    symb, max_ = max_symb[0], int(max_symb[1:])
    return {f"{symb}{_:02d}": 1 if idx == _ else 0 for _ in range(max_ + 1)}


def test(
    relationships: dict[str, tuple[BFunc, str, str]], operator: BFunc = add
) -> bool:

    all_ = set()
    for child, (_, parent1, parent2) in relationships.items():
        all_ |= {child, parent1, parent2}

    xs = sorted([_ for _ in all_ if _.startswith("x")])
    ys = sorted([_ for _ in all_ if _.startswith("y")])
    zs = sorted([_ for _ in all_ if _.startswith("z")])

    for xbit in range(len(xs)):
        # print(f"{100*xbit/44:.2f} %")
        for ybit in range(len(ys)):
            expectation = operator(2**xbit, 2**ybit)
            zbits = create_repr(expectation, max(zs))
            xin = create_repr(2**xbit, max(xs))
            yin = create_repr(2**ybit, max(ys))
            _, result = solve(xin | yin, relationships)

            if zbits != result:
                print(f"Failed on {(xbit, ybit)}")
                return False
    return True


def get_parents(relns: dict[str, tuple[BFunc, set[str]]], node: str) -> set[str]:

    accum = list()

    def recurse(n: str, index: str = ""):
        if n in relns:
            accum.append((index, n, relns[n]))
            a, b = relns[n][1:]
            recurse(a, "0" + index)
            recurse(b, "1" + index)

    recurse(node)
    accum = sorted(accum, key=lambda _: 0 if len(_[0]) == 0 else 1 + int(_[0], 2))
    accum = [_[1:] for _ in accum]

    return dict(accum)


def make_switches(
    relations: dict[str, tuple[BFunc, str, str]], switches: list[set[str]]
) -> dict[str, tuple[BFunc, set, str]]:
    result = relations.copy()
    for a, b in switches:
        result[a], result[b] = result.pop(b), result.pop(a)
    return result


def check(relns, beat_me=float("inf")):
    valid = dict()
    needed_switches = set()

    ###################################################################
    # THESE ARE ALL CACHED SO WE DON'T NEED TO WORRY ABOUT EFFICIENCY #
    ###################################################################
    create_x = partial(create_input, "x44")
    create_y = partial(create_input, "y44")
    create_z = partial(create_input, "z45")

    x0, y0, z0 = create_x(None), create_y(None), create_z(None)

    for i in range(46):
        x, y, z = create_x(i), create_y(i), create_z(i)
        x_, y_ = create_x(i - 1), create_y(i - 1)

        try:
            correct = [solve(x0 | y0, relns)[1] == z0]
            correct += [solve(x | y0, relns)[1] == z]
            correct += [solve(x0 | y, relns)[1] == z]
            correct += [solve(x_ | y_, relns)[1] == z] if i > 0 else []
        except:
            return False  # Catch and pass invalid solutions

        if all(correct):
            valid |= get_parents(relns, f"z{i:02d}")
            if i > beat_me:  # If switch branch is better than parent branch adopt it
                return True
            continue

        # If already investigating a switch branch don't try further corrections
        if beat_me != float("inf"):
            return False

        switches = list(combinations(set(relns) - set(valid), 2))
        print(f"Searching solution for bit {i} (of {len(switches)} possibilities)")

        for count, (a, b) in enumerate(switches):
            if count % 1000 == 0:
                print(f"Switching: {a} and {b} ({100*count/len(switches):.2f} %)")

            tmp = make_switches(relns, [{a, b}])
            improvement = check(tmp, beat_me=i)
            if improvement:
                needed_switches.add(frozenset((a, b)))  # Add better switch
                relns = tmp  # Include switch in parent circuit
                break  # Stop searching for other switches

    return needed_switches


if __name__ == "__main__":
    INPUT_FP = argv[1]
    defns, relations = read_input(INPUT_FP)

    switches_to_make = check(relations)
    DOUBLE_CHECK = test(make_switches(relations, list(switches_to_make)))
    SWITCH_LETTERS = ",".join(sorted([y for _set in switches_to_make for y in _set]))
    print(f"Is solved: {DOUBLE_CHECK}")
    print(f"Solution:\n{SWITCH_LETTERS}")
