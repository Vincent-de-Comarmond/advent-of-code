from collections import defaultdict
from functools import reduce
from itertools import chain, combinations
from pprint import pp
from sys import argv


def load_inputs(input_fp: str) -> dict[str, set[str]]:
    cxns = defaultdict(set)
    with open(input_fp, "r") as txtin:
        for ln in txtin:
            c1, c2 = ln.strip().split("-")
            cxns[c1].add(c2)
            cxns[c2].add(c1)
    return cxns


# Itertools recipe - slightly modified to go from largest to smallest
def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable(combinations(xs, n) for n in range(len(xs), 0, -1))


def part1_make3(cxn_dict: dict[str, set[str]]) -> set[frozenset[str]]:
    result_set = set()

    for c1, cxns in cxn_dict.items():
        if not c1.startswith("t"):
            continue
        for c2 in cxns:
            for c3 in cxns.intersection(cxn_dict[c2]):
                result_set.add(frozenset((c1, c2, c3)))

    result_set = {_ for _ in result_set if len(_) == 3}
    return result_set


def part2_makelargest(cxn_dict: dict[str, set[str]]) -> set[str]:

    subnets = {frozenset((c1,)) | cxn_dict[c1] for c1 in cxn_dict}
    biggest_per_pc = set()

    for subnet in subnets:
        closed_networks = set()
        for potential_lan in powerset(subnet):
            if len(closed_networks) > 0:
                if len(potential_lan) < max(map(len, closed_networks)):
                    break

            closed_net = reduce(
                set.intersection, [cxn_dict[_] | {_} for _ in potential_lan]
            )
            if len(closed_net) > 0:
                closed_networks.add(frozenset(closed_net))
        biggest_per_pc.add(frozenset(closed_networks))
    biggest_subs = {
        frozenset({_ for _ in sub if len(_) == max(map(len, sub))})
        for sub in biggest_per_pc
    }
    biggest_nets = {net for sub in biggest_subs for net in sub}
    return {_ for _ in biggest_nets if len(_) == max(map(len, biggest_nets))}


def part2_makepassword(largest_lans: set[frozenset[str]]) -> str:
    size = len(largest_lans)
    if size != 1:
        if size > 1:
            msg = f"Multiple distinct largest sets ({size}). Problem not well defined."
            raise ValueError(msg)
        else:
            raise ValueError("No subnet found.")

    sorted_lans_pcs = [sorted(_) for _ in largest_lans]
    return ",".join(sorted_lans_pcs[0])


if __name__ == "__main__":
    cxns = load_inputs(argv[1])
    lans = part1_make3(cxns)
    print(f"Part 1 - number of t-computer lans: {len(lans)}")
    # 1366 is the correct answer for part 1

    largest_lans = part2_makelargest(cxns)
    password = part2_makepassword(largest_lans)
    print(f"Part 2 - password for largest lan is: {password}")
    # bs,cf,cn,gb,gk,jf,mp,qk,qo,st,ti,uc,xw is the right answer for part 2
