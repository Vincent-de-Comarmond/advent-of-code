from collections import defaultdict


hands_bids = []
with open("./input.txt", "r") as txtin:
    for ln in txtin:
        hand, bid = map(str.strip, ln.split(" "))
        hands_bids.append((hand, int(bid)))


##################
# 5 of a kind: 0 #
# 4 of a kind: 1 #
# full house:  2 #
# 3 of a kind: 3 #
# two pairs:   4 #
# one pair:    5 #
# high card:   6 #
##################


def test_hands(_in: str) -> str:
    chars = defaultdict(int)
    for char in _in:
        chars[char] += 1

    if len(chars) == 1:
        return 0  # top rank
    if len(chars) == 2:
        if "J" in chars:
            # 5 of a kind
            return 0
        # 4 of a kind or full house
        return 1 if max(chars.values()) == 4 else 2
    if len(chars) == 3:
        if "J" in chars:
            if chars["J"] in (2, 3):  # For or 2 3 Js we have 4 of a kind
                return 1
            # 4 of a kind or full house
            return 1 if max(chars.values()) == 3 else 2
        # 3 of a kind if we have 3 of something else 2 pair
        return 3 if max(chars.values()) == 3 else 4
    if len(chars) == 4:
        if "J" in chars:
            # Any Js means we can make 3 of a kind
            return 3
        # Otherwise we just have 1 pair
        return 5
    if "J" in chars:
        return 5  # We just have 1 pair
    return 6


cards = {
    "A": 0,
    "K": 1,
    "Q": 2,
    "T": 3,
    "9": 4,
    "8": 5,
    "7": 6,
    "6": 7,
    "5": 8,
    "4": 9,
    "3": 10,
    "2": 11,
    "J": 12,
}
base = len(cards)


def straight_strength(hand: str) -> int:
    score = 0
    for idx, char in enumerate(hand):
        if char == "A":
            continue
        score += cards[char] * pow(base, len(hand) - 1 - idx)
    return score


typed_hands = [
    (hand, bid, (test_hands(hand), straight_strength(hand))) for hand, bid in hands_bids
]
sorted_hands = sorted(typed_hands, key=lambda _: _[2], reverse=True)
sorted_hands

winnings = 0
for idx, (hand, bid, _type) in enumerate(sorted_hands):
    winnings += (idx + 1) * bid

print(winnings)
