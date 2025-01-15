from copy import deepcopy
from operator import add
from functools import reduce

with open("input.txt", "r") as txtin:
    for line in txtin:
        data = [
            [idx // 2] * int(char) if (idx % 2 == 0) else [None] * int(char)
            for idx, char in filter(lambda _: _[1] != "\n", enumerate(line))
        ]
data = list(filter(lambda _: len(_) > 0, data))


def organize_data(input_data):
    for b_idx, b_list in enumerate(reversed(input_data)):
        if (len(list(filter(None, b_list)))) == 0:
            continue  # Move entire blocks as once - don't fragment. Ignore empty space
        needed_space = len(b_list)
        rev_idx = len(input_data) - 1 - b_idx
        for f_idx, f_list in enumerate(input_data):
            if f_idx >= rev_idx:
                continue
            available_space = len([_ for _ in f_list if _ is None])

            if available_space >= needed_space:
                new_list = (
                    list(filter(None, f_list))
                    + b_list
                    + [None] * (available_space - needed_space)
                )
                # print(f"Putting new_list {new_list} in at index {f_idx}")
                input_data[f_idx] = new_list
                input_data[rev_idx] = [None for _ in b_list]
                break


dat_copy = deepcopy(data)
organize_data(dat_copy)
# print(dat_copy)

flat_data = [x for y in dat_copy for x in y]


print(
    reduce(add, map(lambda _: 0 if _[1] is None else _[0] * _[1], enumerate(flat_data)))
)
# 6321896265143 is the right answer
