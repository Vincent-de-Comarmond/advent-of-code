dataset = {}

with open("./input.txt", "r", encoding="utf8") as txtin:
    for ln in txtin:
        parts = ln.split(":")
        game_id = int(parts[0].split(" ")[1])
        raw_hands = parts[1].split(";")
        refined_hands = []
        for hand in raw_hands:
            r, g, b = 0, 0, 0
            for num_col in [_.strip() for _ in hand.split(",")]:
                num, col = num_col.split(" ")
                r = int(num) if "red" in col else r
                g = int(num) if "green" in col else g
                b = int(num) if "blue" in col else b
            refined_hands.append((r, g, b))
        dataset[game_id] = refined_hands

##########
# Powers #
##########

powers = {}
power_sum = 0
for game_id, hands in dataset.items():
    min_r, min_g, min_b = 0, 0, 0
    # print(hands)
    for r, g, b in hands:
        min_r, min_g, min_b = max(min_r, r), max(min_g, g), max(min_b, b)
    powers[game_id] = (min_r, min_g, min_b)
    # print(powers[game_id])
    power_sum += min_r * min_g * min_b
print(power_sum)
