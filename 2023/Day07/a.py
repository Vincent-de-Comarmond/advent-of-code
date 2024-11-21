from functools import cmp_to_key


hands_bids = []
with open("./input.txt", "r") as txtin:
    for ln in txtin:
        hand, bid = map(str.strip, ln.split(" "))
        hands_bids.append((hand, int(bid)))


def test_5(_in: str) -> bool:
    return _in.count(_in[0]) == 5


def test_4(_in: str) -> bool:
    return max(_in.count(_in[0]), _in.count(_in[1])) == 4


def test_full(_in: str) -> bool:
    chars = set(_in)
    # Note this is only true if we know it's not 4
    return len(chars) == 2


def test_3(_in: str) -> bool:
    chars = set(_in)
    if len(chars) != 3:
        return False
    for _char in chars:
        if _in.count(_char) == 3:
            return True
    return False


def test_22(_in: str) -> bool:
    # Note this is only true if we know it's not 4
    return len(set(_in)) == 3


def test_12(_in: str) -> bool:
    return len(set(_in)) == 4


# kind_5 = {}         0
# kind_4 = {}         1
# kind_full = {}      2
# kind_3 = {}         3
# kind_22 = {}        4
# kind_12 = {}        5
# kind_high = {}      6

hands_with_types = []
for hand, bid in hands_bids:
    for idx, test_func in enumerate(
        (test_5, test_4, test_full, test_3, test_22, test_12)
    ):
        if test_func(hand):
            hands_with_types.append((hand, bid, idx))
            break
    else:
        hands_with_types.append((hand, bid, 6))


cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


def compare(hand1: tuple, hand2: tuple):
    if hand1[2] == hand2[2]:
        for i in range(5):
            char1, char2 = hand1[0][i], hand2[0][i]
            idx1, idx2 = cards.index(char1), cards.index(char2)
            if idx1 != idx2:
                return idx1 - idx2
        return 0
    return hand1[2] - hand2[2]


sorted_hands = sorted(hands_with_types, key=cmp_to_key(compare), reverse=True)

winnings = 0
for idx, detail in enumerate(sorted_hands):
    winnings += (idx + 1) * detail[1]

print(winnings)
# 251058093 is correct
