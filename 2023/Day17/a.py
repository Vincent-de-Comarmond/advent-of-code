import pdb
import numpy as np


TEST = True

if TEST:
    raw = [
        "2413432311323",
        "3215453535623",
        "3255245654254",
        "3446585845452",
        "4546657867536",
        "1438598798454",
        "4457876987766",
        "3637877979653",
        "4654967986887",
        "4564679986453",
        "1224686865563",
        "2546548887735",
        "4322674655533",
    ]
else:
    with open("./input.txt", "r") as txtin:
        raw = [ln.strip() for ln in txtin]

DATA = np.array([[_ for _ in row] for row in raw])


def t_add(t1: tuple, t2: tuple) -> tuple:
    return tuple(t1[i] + t2[i] for i in range(len(t1)))


def t_minus(t1: tuple, t2: tuple) -> tuple:
    return tuple(t1[i] - t2[i] for i in range(len(t1)))


burnt = {}
step_counter = {}
active = {((0, 0), (1, 0), 0, 0), ((0, 0), (0, 1), 0, 0)}

FML = {((0, 0),): 0}

while len(active) != 0:
    new_edge = set()

    for datum in active:
        point, direction, energy_loss, steps = datum

        new_point = t_add(point, direction)

        if new_point[0] < 0 or new_point[0] > DATA.shape[0] - 1:
            continue
        if new_point[1] < 0 or new_point[1] > DATA.shape[1] - 1:
            continue

        if point in burnt:
            if energy_loss <= burnt[point]:
                burnt[point] = energy_loss
            else:
                continue
        else:
            burnt[point] = energy_loss

        for new_direction in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            # print(f"New direction: {new_direction}")
            # Can't do a u-turn

            if t_add(direction, new_direction) == (0, 0):
                continue

            if direction != new_direction:
                new_edge.add(
                    (new_point, new_direction, energy_loss + int(DATA[new_point]), 1)
                )
            else:
                # We can't continue in the same direction more than 3 steps
                if steps > 3:
                    continue
                new_edge.add(
                    (
                        new_point,
                        new_direction,
                        energy_loss + int(DATA[new_point]),
                        steps + 1,
                    )
                )

    active = new_edge

test = np.full(DATA.shape, -1)
for k, v in burnt.items():
    test[k] = v
print(test)


def reverse_map(test_array: np.ndarray):
    points = [t_minus(test_array.shape, (1, 1))]
    point = points[-1]

    while point != (0, 0):
        choices = {}
        for i, j in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            if point[0] + i < 0 or point[0] + i > test_array.shape[0] - 1:
                continue
            if point[1] + j < 0 or point[1] + j > test_array.shape[1] - 1:
                continue

            new_point = t_add(point, (i, j))
            choices[new_point] = test_array[new_point]
        point = min(choices.items(), key=lambda _: _[1])[0]
        points.append(point)

    return points


traversed = reverse_map(test)
reverse_journey = DATA.astype(str)
for pt in traversed:
    reverse_journey[pt] = "·"
print(reverse_journey)
