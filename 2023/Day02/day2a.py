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
# Limits #
##########

red, green, blue = 12, 13, 14

passed_games = {}
for game_id, hands in dataset.items():
    for r, g, b in hands:
        if r > red or g > green or b > blue:
            fail_col = "red" if r > red else "green" if g > green else "blue"
            print(f"Game {game_id} failed on {fail_col} with numbers: {(r,g,b)}")
            break
    else:
        passed_games[game_id] = hands

sum(passed_games)
