# Stdlib
from functools import lru_cache
from typing import Any, Set, Tuple

# 3rd party
import regex as re

Test = False
raw = []

if Test:
    raw = [
        "???.### 1,1,3",  # 1
        ".??..??...?##. 1,1,3",  # 4
        "?#?#?#?#?#?#?#? 1,3,1,6",  # 1
        "????.#...#... 4,1,1",  # 1
        "????.######..#####. 1,6,5",  # 4
        "?###???????? 3,2,1",  # 10
    ]
else:
    with open("./input.txt", "r") as txtin:
        raw = [ln.strip() for ln in txtin]

info = [
    (row.split(" ")[0], tuple(map(int, row.split(" ")[1].split(",")))) for row in raw
]

PATTERN = re.compile(r"#+")


def expand_record(input_str: str, input_numbers: Tuple[int]) -> Tuple[str, Tuple[int]]:
    return "?".join(input_str for _ in range(5)), tuple(list(input_numbers) * 5)


def try_remove(collection: list, item: Any, printme: bool = True):

    if printme:
        print(f"Trying to remove {item} from {collection}")
    try:
        collection.remove(item)
    except:
        if printme:
            print(f"Failed to remove {item} from {collection}")


@lru_cache(maxsize=None)
def generate_subpattern(num_broken: int) -> re.Pattern:
    return re.compile(r"(#|\?){" + str(num_broken) + "}")


@lru_cache(maxsize=None)
def regex_from_numbers(numbers: Tuple[int]) -> re.Pattern:

    broken = r"(#|\?)"
    regex_pattern = r"(\.|\?)*"
    for idx, numbroken in enumerate(numbers):
        if numbroken == 1:
            regex_pattern += broken
        else:
            regex_pattern += broken + "{" + str(numbroken) + "}"

        if idx == len(numbers) - 1:
            regex_pattern += r"(\.\?)*"
        else:
            regex_pattern += r"(\.|\?)+"

    return re.compile(regex_pattern)


@lru_cache(maxsize=None)
def compl_regex_from_nums(numbers: Tuple[int]) -> re.Pattern:

    pattern = "\.*"
    for idx, numbroken in enumerate(numbers):
        pattern += "#" if numbroken == 1 else "#{" + str(numbroken) + "}"
        pattern += "\.*" if idx == len(numbers) - 1 else "\.+"
    return re.compile(pattern)


def generative_algo(
    cache: Set[str], input_nums: Tuple[int], printme: bool = False, idx: int = 0
) -> Set[str]:

    print(f"\tindex {idx} of {len(input_nums)}: {100*idx / len(input_nums) : 2.2f} %")

    if printme:
        print(f"{idx}: {input_nums}")
        print(cache)

    if idx > len(input_nums) - 1:
        filter_pat = compl_regex_from_nums(input_nums)
        return {_ for _ in cache if filter_pat.match(_)}

    filter_pat = regex_from_numbers(input_nums)
    pattern = re.compile(r"(#|\?){}".format("{" + str(input_nums[idx]) + "}"))

    # if idx == 1:
    #     pdb.set_trace()

    for string in cache.copy():
        # Nothing to do

        for match in pattern.finditer(string, overlapped=True):

            string_array = [_ for _ in string]
            start, end = match.start(), match.end()
            if printme:
                print(match)

            # if "?" not in match.group():
            #     continue

            for i in range(start, end):
                if string[i] == "?":
                    string_array[i] = "#"

            if end <= len(string) - 1:
                if string[end] == "?":
                    string_array[end] = "."
                if string[end] == "#":
                    continue
                    # try_remove(cache, "".join(string_array), printme)
            newstring = "".join(string_array)

            if start > 0:
                if string[start - 1] == "#":
                    # try_remove(cache, newstring, printme)
                    continue

            for i in range(start):
                if string[i] == "?":
                    string_array[i] = "."
            if printme:
                print(newstring)
                # print(filter_pat)
            if filter_pat.match(newstring):
                cache.add("".join(string_array))
        # try_remove(cache, string, printme)

    return generative_algo(cache, input_nums, printme, idx + 1)


total_possibilities = 0
for idx, record in enumerate(info):
    expanded_rec = expand_record(*record)
    print(f"INDEX: {idx}")
    total_possibilities += len(generative_algo({expanded_rec[0]}, expanded_rec[1]))
    completion = 100 * (idx + 1) / len(info)
    print(f"{completion:2.2f} %")

print(total_possibilities)
