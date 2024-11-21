from collections import defaultdict

scores = {}

with open("./input.txt", "r") as txtin:
    for idx, _ in enumerate(txtin):
        scores[idx + 1] = 1


number_of_cards = max(scores)


with open("./input.txt", "r") as txtin:
    for idx, ln in enumerate(txtin):
        card_num = idx + 1

        parts = ln.split("|")
        _winners = filter(lambda _: len(_) > 0, parts[0].split(":")[1].split(" "))
        _numbers = filter(lambda _: len(_) > 0, parts[1].split(" "))

        winners = list(map(int, _winners))
        numbers = list(map(int, _numbers))

        # print(sorted(winners))
        # print(sorted(numbers))

        matches = 0
        for winner in winners:
            if winner in numbers:
                matches += 1
        print(matches)

        for _idx in range(card_num + 1, card_num + 1 + matches):
            scores[_idx] += scores[card_num]
        print(scores)


sum(map(lambda _: _[1], filter(lambda _: _[0] <= number_of_cards, scores.items())))

# 12515 is too low

# 5489599 is too low

