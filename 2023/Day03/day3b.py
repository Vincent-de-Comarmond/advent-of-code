from functools import reduce
from operator import mul
from typing import List

symbols = {"#", "$", "%", "&", "*", "+", "-", "/", "=", "@"}


raw_dataset: List[List[str]] = []
with open("./input.txt", "r", encoding="utf8") as txtin:
    for ln in txtin:
        raw_dataset.append(ln)  # [_ for _ in ln if _ != "\n"])

gears = []
for i, row in enumerate(raw_dataset):
    for j, char in enumerate(row):
        if char == "*":

            multi_index = []
            number_cache = {}
            traversed = []

            for sq in range(9):
                _i = max(0, min(len(raw_dataset) - 1, i + sq // 3 - 1))
                _j = max(0, min(len(row) - 1, j + sq % 3 - 1))

                if (_i, _j) in traversed:
                    continue

                if raw_dataset[_i][_j].isdigit():
                    multi_index.append((_i, _j))

                    # Check for multi-digit numbers
                    if _j - 1 >= 0 and raw_dataset[_i][_j - 1].isdigit():
                        multi_index.append((_i, _j - 1))
                        if _j - 2 >= 0 and raw_dataset[_i][_j - 2].isdigit():
                            multi_index.append((_i, _j - 2))
                    if _j + 1 < len(row) and raw_dataset[_i][_j + 1].isdigit():
                        multi_index.append((_i, _j + 1))
                        if _j + 2 >= 0:
                            if raw_dataset[_i][_j + 2].isdigit():
                                multi_index.append((_i, _j + 2))

                    # Cool create value for multi-digit numbers
                    traversed.extend(multi_index)
                    key = tuple(sorted(multi_index))
                    multi_index = []
                    number = ""
                    for ii, jj in key:
                        number += raw_dataset[ii][jj]
                    number_cache[key] = int(number)
            if len(number_cache) == 2:
                gears.append(number_cache)

sum_gear_ratios = sum(map(lambda _: reduce(mul, _.values()), gears))
print(sum_gear_ratios)
