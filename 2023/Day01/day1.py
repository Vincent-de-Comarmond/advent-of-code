##########
# Part 1 #
##########
lines = []
with open("./input.txt", "r") as txtin:
    for ln in txtin:
        digits = [char for char in ln if char.isdigit()]
        if len(digits) > 0:
            number = int(digits[0] + digits[-1])
            lines.append(number)
print(sum(lines))

##########
# Part 2 #
##########
import re

digits = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
digits_rev = {k[::-1]: v for k, v in digits.items()}
pattern = re.compile("|".join(digits))
rev_pattern = re.compile("|".join(digits_rev))

lines2 = []
with open("./input.txt", "r") as txtin:
    for ln in txtin:
        forwards = pattern.sub(lambda m: digits[m.group(0)], ln)
        backwards = rev_pattern.sub(lambda m: digits_rev[m.group(0)], ln[::-1])

        first = next(filter(str.isdigit, forwards))
        last = next(filter(str.isdigit, backwards))

        print(ln, first, last)
        print()
        lines2.append(int(first + last))
print(sum(lines2))
