from itertools import cycle

instructionset = []
nodes = {}

with open("./input.txt", "r", encoding="utf8") as txtin:
    for idx, ln in enumerate(txtin):
        if idx == 0:
            instructionset = [
                int(_) for _ in ln.strip().replace("L", "0").replace("R", "1")
            ]

        if idx > 1:
            parts = list(map(str.strip, ln.split("=")))
            choices = tuple(parts[1].replace("(", "").replace(")", "").split(", "))
            nodes[parts[0]] = choices

steps = 0
location = "AAA"

for instruction in cycle(instructionset):
    location = nodes[location][instruction]
    steps += 1
    if location == "ZZZ":
        break

print(steps)
# Correct answer: 18023
