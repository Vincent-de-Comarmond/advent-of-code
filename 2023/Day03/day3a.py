from collections import defaultdict
import numpy as np
from pprint import pprint
from typing import List

if False:
    ###########################################
    # First pass ... see what the symbols are #
    ###########################################

    symbolcounter = defaultdict(int)

    with open("./input.txt", "r", encoding="utf8") as txtin:
        for ln in txtin:
            for symbol in ln:
                symbolcounter[symbol] += 1

    pprint(symbolcounter)

symbol_counts = {
    "\n": 140,
    "#": 39,
    "$": 42,
    "%": 47,
    "&": 39,
    "*": 350,
    "+": 35,
    "-": 53,
    ".": 15437,
    "/": 48,
    "0": 219,
    "1": 361,
    "2": 380,
    "3": 343,
    "4": 333,
    "5": 348,
    "6": 360,
    "7": 364,
    "8": 376,
    "9": 347,
    "=": 42,
    "@": 37,
}

debug = False
symbols = {"#", "$", "%", "&", "*", "+", "-", "/", "=", "@"}


raw_dataset: List[List[str]] = []
with open("./input.txt", "r", encoding="utf8") as txtin:
    for ln in txtin:
        raw_dataset.append(ln)  # [_ for _ in ln if _ != "\n"])

numbers = []
for i, row in enumerate(raw_dataset):
    number_cache = []
    number = ""

    if debug:
        print()
        if i > 0:
            print("".join(["." if _.isdigit() else _ for _ in raw_dataset[i - 1]]))
        print("".join(row))
        if i < len(raw_dataset) - 1:
            print("".join(["." if _.isdigit() else _ for _ in raw_dataset[i + 1]]))

    for j, char in enumerate(row):
        if char.isdigit():
            number_cache.append(j)
            number += char
        else:
            if len(number_cache) > 0:
                left = max(0, min(number_cache) - 1)
                right = min(len(row) - 1, max(number_cache) + 1)
                up = max(0, i - 1)
                down = min(len(raw_dataset) - 1, i + 1)

                for ii in range(up, down + 1):
                    for jj in range(left, right + 1):
                        if raw_dataset[ii][jj] in symbols:
                            numbers.append(int(number))
                            if debug:
                                print(number, sep=" ")
                            break
                number_cache = []
                number = ""
print(sum(numbers))

# 506273 is too low
