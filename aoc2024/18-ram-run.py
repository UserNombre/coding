import re
import numpy as np

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

sample_result = (22,)

def solve(input_string):
    if mode == "check":
        dimensions = (7, 7)
        fallen_bytes = 12
    else:
        dimensions = (71, 71)
        fallen_bytes = 1024

    maze = np.full(dimensions, ord("."))
    steps_map = np.full(dimensions, float("inf"))
    corrupted_positions = [(int(i), int(j)) for i, j in re.findall(r"(\d+),(\d+)", input_string)]
    for position in corrupted_positions[:fallen_bytes]:
        maze[position] = ord("#")

    end_position = np.array(maze.shape) - (1, 1)
    compute_maze_steps(maze, end_position, np.array([0, 0]), 0, steps_map)
    min_steps = int(steps_map[*end_position])
    return min_steps,

def compute_maze_steps(maze, end_position, position, steps, steps_map):
    if (maze[*position] == ord("#") or
        not steps < steps_map[*end_position] or
        not steps < steps_map[*position]):
        return

    steps_map[*position] = steps
    maze[*position] = ord("o")
    if debug:
        print_debug_info(maze, position, steps, steps_map[*end_position])
    for direction in helpers.directions:
        next_position = position + direction
        if (((0, 0) <= next_position) & (next_position < maze.shape)).all():
            compute_maze_steps(maze, end_position, next_position, steps+1, steps_map)
    maze[*position] = ord(".")

def print_debug_info(maze, position, steps, min_steps):
    header = f"POS: {tuple(position)}, STEP: {steps}, MIN_STEPS: {min_steps}"
    helpers.print_2d_debug_info(header, maze, position, 0.1)
