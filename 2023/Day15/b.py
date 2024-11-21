from collections import defaultdict
from typing import List

#####################################################################
# Determine the ASCII code for the current character of the string. #
# Increase the current value by the ASCII code you just determined. #
# Set the current value to itself multiplied by 17.                 #
# Set the current value to the remainder of dividing itself by 256. #
#####################################################################

########################################################################
# Each step begins with a sequence of letters that indicate the label  #
# of the lens on which the step operates. The result of running the    #
# HASH algorithm on the label indicates the correct box for that step. #
########################################################################


############################################################################
# If there is already a lens in the box with the same label, replace       #
# the old lens with the new lens: remove the old lens and put the new lens #
# in its place, not moving any other lenses in the box.                    #
# If there is not already a lens in the box with the same label, add the   #
# lens to the box immediately behind any lenses already in the box.        #
# Don't move any of the other lenses when you do this.                     #
# If there aren't any lenses in the box, the new lens goes                 #
# all the way to the front of the box.                                     #
############################################################################


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


def operate(input_dict: dict, operation_str: str):

    operator = "=" if "=" in operation_str else "-"
    operation_parts = operation_str.split(operator)
    lens = operation_parts[0]
    focal_length = None if operator == "-" else int(operation_parts[1])

    if operator == "-":
        if lens in input_dict:
            input_dict.pop(lens)
    else:
        input_dict[lens] = focal_length


boxes = defaultdict(dict)

for _input in checklist:
    _box_id = string_helper_algo(_input.split("-" if "-" in _input else "=")[0])
    operate(boxes[_box_id], _input)

foc_power = 0

for box_no, box_config in boxes.items():

    lens_slot = 1
    sum_lens_pow = 0
    for lens_type, foc_len in box_config.items():
        sum_lens_pow += lens_slot * foc_len
        lens_slot += 1

    foc_power += (box_no + 1) * sum_lens_pow

print(foc_power)

# 244342 is the right answer
