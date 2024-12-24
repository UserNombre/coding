import re
import numpy as np
from bisect import bisect

sample_input = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

sample_result = (22, "6,1")

def solve(input_string):
    if mode == "check":
        dimensions = (7, 7)
        fallen_bytes = 12
    else:
        dimensions = (71, 71)
        fallen_bytes = 1024

    maze = np.full(dimensions, ord("."))
    corrupted_positions = [(int(i), int(j)) for i, j in re.findall(r"(\d+),(\d+)", input_string)]
    exit_distance = compute_exit_distance(maze, corrupted_positions[:fallen_bytes])
    unreachable_index = bisect(range(len(corrupted_positions)), 1e9-1,
                               key=lambda i: compute_exit_distance(maze, corrupted_positions[:i]))-1
    unreachable_coords = ",".join(str(x) for x in corrupted_positions[unreachable_index])
    return exit_distance, unreachable_coords

def compute_exit_distance(maze, corrupted_positions):
    maze = maze.copy()
    iterations = len(corrupted_positions)
    for position in corrupted_positions:
        maze[position] = ord("#")

    exit_distance = 1e9
    exit_position = np.array(maze.shape) - (1, 1)
    pending = [(0, np.array([0, 0]))]
    while pending:
        distance, position = pending.pop(0)
        maze[*position] = ord("o")
        if (position == exit_position).all():
            return distance
        for direction in helpers.directions:
            next_position = position + direction
            if ((((0, 0) <= next_position) & (next_position < maze.shape)).all() and
                maze[*next_position] not in [ord("#"), ord("o"), ord("x")]):
                maze[*next_position] = ord("x")
                pending.append((distance+1, next_position))
        if debug:
            print_debug_info(maze, position, iterations)
    return exit_distance

def print_debug_info(maze, position, iterations):
    header = f"POS: {tuple(position)} ITER: {iterations}"
    helpers.print_2d_debug_info(header, maze, position, 0.1)
