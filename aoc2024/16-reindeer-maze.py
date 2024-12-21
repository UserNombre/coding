import numpy as np

sample_input = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

sample_result = (7036,)

def solve(input_string):
    maze = np.array([list(row.encode()) for row in input_string.split()])

    start_present = maze == ord("S")
    assert start_present.any(), "start tile not present in map"
    start_position = np.array(np.unravel_index(np.argmax(start_present), maze.shape))
    end_present = maze == ord("E")
    assert end_present.any(), "end tile not present in map"
    end_position = np.array(np.unravel_index(np.argmax(end_present), maze.shape))

    score_map = np.full(maze.shape, float("inf"))
    compute_maze_scores(maze, end_position, start_position, (0, 1), 0, score_map)
    lowest_end_score = int(score_map[*end_position])
    return lowest_end_score,

def compute_maze_scores(maze, end_position, position, direction, score, score_map):
    cell = maze[*position]
    if (cell in [ord("#"), ord("o")] or
        not score < score_map[*end_position] or
        not score < score_map[*position]):
        return

    score_map[*position] = score
    if cell == ord("E"):
        return

    maze[*position] = ord("o")
    if debug:
        print_debug_info(maze, position, direction, score, score_map[*end_position])
    for next_direction in helpers.directions:
        next_position = position + next_direction
        new_score = score + 1 if next_direction == direction else score + 1001
        compute_maze_scores(maze, end_position, next_position, next_direction , new_score, score_map)
    maze[*position] = ord(".")

def print_debug_info(maze, position, direction, score, lowest_score):
    header = f"POS: {tuple(position)}, DIR: {direction}, SCORE: {score}, LOWEST_SCORE: {lowest_score}"
    helpers.print_2d_debug_info(header, maze, position, 0.1)
