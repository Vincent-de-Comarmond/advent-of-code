from functools import reduce

race_stats = [(54, 239), (70, 1142), (82, 1295), (75, 1253)]

ways_to_win = []
for time, record in race_stats:
    winning_strategies = 0
    for button_time in range(0, time + 1):
        speed = button_time
        travel_time = time - button_time
        distance = travel_time * speed
        if distance > record:
            winning_strategies += 1
    ways_to_win.append(winning_strategies)

print(ways_to_win)
reduce(lambda a, b: a * b, ways_to_win)
