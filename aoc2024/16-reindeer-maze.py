import numpy as np
from collections import defaultdict
from heapq import heappop, heappush

sample_input = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

sample_result = (11048, 64)

def solve(input_string):
    maze = np.array([list(row.encode()) for row in input_string.split()])
    start_present = maze == ord("S")
    assert start_present.any(), "start tile not present in map"
    start_position = np.unravel_index(np.argmax(start_present), maze.shape)
    end_present = maze == ord("E")
    assert end_present.any(), "end tile not present in map"
    end_position = np.unravel_index(np.argmax(end_present), maze.shape)

    score, paths = compute_best_paths(maze, start_position, end_position)
    total_tiles = len(set([tile for path in paths for tile in path]))
    return score, total_tiles

def compute_best_paths(maze, start_position, end_position):
    paths = []
    best_score = float("inf")
    scores = defaultdict(lambda: float("inf"))
    pending = [(0, start_position, (0, 1), [start_position])]
    while pending:
        score, position, direction, path = heappop(pending)
        if position == end_position and score <= best_score:
            paths.append(path)
            best_score = score
        scores[*position, direction] = score
        for next_direction in direction, helpers.cw_direction[direction], helpers.ccw_direction[direction]:
            next_position = tuple(np.array(position) + next_direction)
            next_score = score + 1 if next_direction == direction else score + 1001
            # TODO: improve condition to avoid unnecessarily revisting cells
            if maze[*next_position] != ord("#") and next_score <= scores[*next_position, next_direction]:
                maze[*next_position] = helpers.direction_to_cell[next_direction]
                heappush(pending, ((next_score, next_position, next_direction, path + [next_position])))
        if debug:
            maze[*position] = ord("X")
            print_debug_info(maze, position, direction, score, best_score)
        maze[*position] = ord("o")
    if debug:
        tiles = set([tile for path in paths for tile in path])
        for position, _ in np.ndenumerate(maze):
            if maze[*position] != ord("#") and position not in tiles:
                maze[*position] = ord(".")
        print_debug_info(maze, position, direction, best_score, best_score)
    return best_score, paths

def print_debug_info(maze, position, direction, score, best_score):
    header = f"POS: {tuple(position)}, DIR: {direction}, SCORE: {score}, BEST_SCORE: {best_score}"
    helpers.print_2d_debug_info(header, maze, position, 0.1)
