from collections import defaultdict
from itertools import cycle
from math import lcm

locations = []
instructionset = []
nodes = defaultdict(dict)

with open("./input.txt", "r", encoding="utf8") as txtin:
    for idx, ln in enumerate(txtin):
        if idx == 0:
            instructionset = ln.strip()

        if idx > 1:
            parts = list(map(str.strip, ln.split("=")))
            choices = tuple(parts[1].replace("(", "").replace(")", "").split(", "))
            nodes["L"][parts[0]] = choices[0]
            nodes["R"][parts[0]] = choices[1]
            if parts[0].endswith("A"):
                locations.append(parts[0])

moves = []

for location in locations:
    steps = 0
    current_location = location
    for instruction in cycle(instructionset):
        current_location = nodes[instruction][current_location]
        steps += 1
        if current_location.endswith("Z"):
            moves.append(steps)
            break

print(moves)
print(f"Total steps: {lcm(*moves)}")
# [19637, 18023, 21251, 16409, 11567, 14257]
# Total steps: 14449445933179
