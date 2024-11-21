time = 54708275
distance = 239114212951253

winning_strategies = 0
for button_time in range(0, time + 1):
    speed = button_time
    travel_time = time - button_time
    potential_distance = travel_time * speed
    if potential_distance > distance:
        winning_strategies += 1

print(winning_strategies)
