# stdlib
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
import os
import sys

# 3rd party
import numpy as np
from PIL import Image


class Robot:
    width = None
    height = None

    def __init__(
        self, x: int | float, y: int | float, vx: int | float, vy: int | float
    ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self, time: int | float) -> tuple[int | float, int | float]:

        new_x = self.x + time * self.vx
        new_y = self.y + time * self.vy
        self.x = new_x % Robot.width
        self.y = new_y % Robot.height
        return (self.x, self.y)


def safety_factor_at_time(robots: list[Robot], time: int | float) -> int:

    width, height = Robot.width, Robot.height
    robot_positions = defaultdict(int)
    for robot in robots:
        robot_positions[robot.move(time)] += 1

    print_robots(width, height, robot_positions)
    quadrant_counts = {1: 0, 2: 0, 3: 0, 4: 0}

    cx, cy = width // 2, height // 2

    for (x, y), v in robot_positions.items():
        if (x, y) == (cx, cy):
            print(f"Ignoring robot at {x, y}")
            continue

        quadrant = None
        if x < cx and y < cy:
            quadrant = 1
        elif x > cx and y < cy:
            quadrant = 2
        elif x < cx and y > cy:
            quadrant = 3
        elif x > cx and y > cy:
            quadrant = 4

        if quadrant is not None:
            quadrant_counts[quadrant] += v
    print(quadrant_counts)

    return reduce(lambda a, b: a * b, quadrant_counts.values())


def write_robots(
    width: int, height: int, robot_positions: dict[tuple[int | float, int | float], int]
) -> np.ndarray:

    grid = np.zeros((height, width))
    for k, v in robot_positions.items():
        x, y = k
        grid[y, x] = v
    return grid


def print_robots(
    width: int,
    height: int,
    robot_positions: dict[tuple[int | float, int | float], int],
    flout=None,
) -> None:

    _str = "\n".join(
        [
            "".join(["." if char == 0 else str(int(char)) for char in line])
            for line in write_robots(width, height, robot_positions)
        ]
    )

    if flout is None:
        print(_str)
    else:
        with open(flout, "w") as txtout:
            print(_str, file=txtout)


@dataclass
class Inputs:
    width: int
    height: int
    robots: list[Robot]


def initialize() -> Inputs:
    width, height = int(sys.argv[1]), int(sys.argv[2])
    input_fp = sys.argv[3]

    Robot.width = width
    Robot.height = height
    robots: list[Robot] = list()

    with open(input_fp, "r") as flin:
        for ln in flin:
            position, velocity = map(lambda _: _.split("=")[1], ln.split(" "))
            (x, y), (vx, vy) = position.split(","), velocity.split(",")
            robots.append(Robot(int(x), int(y), int(vx), int(vy)))

    return Inputs(width, height, robots)


def part1(robot_list: list[Robot], timestamp: int) -> int:
    return safety_factor_at_time(robot_list, timestamp)


def part2(robot_list: list[Robot], output_dir: str) -> None:

    width, height = robot_list[0].width, robot_list[0].height
    fresh_robot_list_copy = deepcopy(robot_list)

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "txts"), exist_ok=True)

    # Step 1
    # Compute size of the stat space
    # state_space = set()
    # time = -1
    # while True:
    #     time += 1
    #     if time % 100 == 0:
    #         print(f"Time elapsed: {time}")
    #     robot_positions = defaultdict(int)
    #     for robot_id, robot in enumerate(robot_list):
    #         x, y = robot.move(time)
    #         robot_positions[(robot_id, x, y)] += 1
    #     state = tuple(sorted(robot_positions.items()))
    #     if state in state_space:
    #         break
    #     state_space.add(state)

    # state_space_size = len(state_space)
    # print(f"State space size: {state_space_size}")

    # format_str = int(np.log10(len(state_space))) + 1
    # format_str = "{:0" + str(format_str) + "d}.{}"

    state_space_size = 1000000 - 5
    format_str = "{:07d}.{}"
    # Step 2
    # Safe snapshots for as big/little as the state space is (with a bit extra for safety)
    robot_list = fresh_robot_list_copy
    for time in range(state_space_size + 5):
        if time % 100 == 0:
            print(f"Time elapsed: {time}")
        robot_positions = defaultdict(int)
        for robot in robot_list:
            robot_positions[robot.move(1)] += 1
        data = write_robots(width, height, robot_positions)
        norm_factor = 250 / data.max()
        data = (data * norm_factor).astype(np.uint8)
        img = Image.fromarray(data)
        img = img.resize((10 * img.width, 10 * img.height), Image.Resampling.LANCZOS)
        img.save(os.path.join(output_dir, format_str.format(time, "jpg")))
        print_robots(
            width,
            height,
            robot_positions,
            os.path.join(output_dir, "txts", format_str.format(time, "txt")),
        )


if __name__ == "__main__":

    inputs = initialize()
    if sys.argv[4] == "part1":
        safety_factor = part1(inputs.robots, int(sys.argv[5]))
        print(safety_factor)
        # 228457125 is the right answer for part 1
    elif sys.argv[4] == "part2":
        part2(inputs.robots, "./images")
        # 21 is wrong
        # 20 is wrong
        # 2142 is too low ???? - But I clearly see a christmas tree -  okay ... this time I screwed up
        # 6492 is still wrong - but again, I clearly see a christmas tree
        # - okay ... you start at 1 rather than 0 - i.e. you label second 1 as second 0 -  so you label second 6493 as 6492
        # Try 6493 then
        ##### Okay 6493 is right
