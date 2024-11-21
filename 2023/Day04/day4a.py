points = []
with open("./input.txt") as txtin:
    for ln in txtin:

        current_score = 0

        parts = ln.split("|")
        _winners = filter(lambda _: len(_) > 0, parts[0].split(":")[1].split(" "))
        _numbers = filter(lambda _: len(_) > 0, parts[1].split(" "))

        winners = list(map(int, _winners))
        numbers = list(map(int, _numbers))

        for winner in winners:
            if winner in numbers:
                current_score = 1 if current_score == 0 else 2 * current_score
        points.append(current_score)


sum(points)
