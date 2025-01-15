from collections import defaultdict
from copy import deepcopy
from functools import lru_cache
from typing import List


@lru_cache(maxsize=None)
def get_children(element: int) -> List[int]:
    if element == 0:
        return [1]

    str_element = str(element)
    if len(str_element) % 2 == 0:
        return [
            int(str_element[: int(len(str_element) / 2)]),
            int(str_element[int(len(str_element) / 2) :]),
        ]

    return [element * 2024]


def blink(input_dict: dict) -> defaultdict:
    output_dict = defaultdict(int)
    for k, v in input_dict.items():
        children = get_children(k)
        for child in children:
            output_dict[child] += v
    return output_dict


with open("input.txt", "r") as txtin:
    DATA = {int(_): 1 for _ in txtin.read().split(" ")}

input_data = deepcopy(DATA)

for i in range(75):
    print(f"Computing for blink: {i:02d}")
    input_data = blink(input_data)

print(sum(input_data.values()))
# 218817038947400 is the right answer for part 2
