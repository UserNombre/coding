import numpy as np
from itertools import combinations

sample_input = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

sample_result = (1, 285)

def solve(input_string):
    if mode == "check":
        required_save = 50
    else:
        required_save = 100

    maze = np.array([list(row.encode()) for row in input_string.split()])
    start_present = maze == ord("S")
    assert start_present.any(), "start tile not present in map"
    start_position = np.array(np.unravel_index(np.argmax(start_present), maze.shape))
    path = compute_path(maze, start_position)

    total_cheats_v1 = total_cheats_v2 = 0
    for p_distance, p in enumerate(path[:-required_save]):
        min_distance = p_distance + required_save
        for q_distance, q in enumerate(path[min_distance:], min_distance):
            cheat_distance = abs(q[0]-p[0]) + abs(q[1]-p[1])
            if q_distance - p_distance - cheat_distance >= required_save:
                total_cheats_v1 += (cheat_distance <= 2)
                total_cheats_v2 += (cheat_distance <= 20)
    return total_cheats_v1, total_cheats_v2

def compute_path(maze, position):
    path = []
    while maze[*position] != ord("o"):
        maze[*position] = ord("o")
        path.append(position)
        for direction in helpers.directions:
            next_position = position + direction
            if maze[*next_position] not in [ord("#"), ord("o")]:
                position = next_position
                break
        if debug:
            print_debug_info(maze, position, len(path)-1)
    return path

def print_debug_info(maze, position, distance):
    header = f"POS: {tuple(position)}, DISTANCE: {distance}"
    helpers.print_2d_debug_info(header, maze, position, 0.1)
