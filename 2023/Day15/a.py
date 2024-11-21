from typing import List

#####################################################################
# Determine the ASCII code for the current character of the string. #
# Increase the current value by the ASCII code you just determined. #
# Set the current value to itself multiplied by 17.                 #
# Set the current value to the remainder of dividing itself by 256. #
#####################################################################


start_value = 0
TEST = False
raw: str = ""
if TEST:
    raw = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
else:
    with open("./input.txt", "r") as txtin:
        raw = "".join(ln.strip() for ln in txtin)

checklist: List[str] = raw.split(",")


def string_helper_algo(in_string: str, idx: int = 0, current_hash: int = 0) -> int:
    if idx >= len(in_string):
        return current_hash

    current_hash = ((current_hash + ord(in_string[idx])) * 17) % 256
    return string_helper_algo(in_string, idx=idx + 1, current_hash=current_hash)


sum_total = 0
for _input in checklist:
    sum_total += string_helper_algo(_input)
print(sum_total)

# 519603 is the right answer
