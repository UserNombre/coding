import os
import sys
import time
import copy

sample_input = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

sample_result = (41, 6)

cell_to_direction = {ord("^"): (-1, 0), ord(">"): (0, 1), ord("v"): (1, 0), ord("<"): (0, -1)}
direction_to_cell = {v: k for k, v in cell_to_direction.items()}

def solve(input_string):
    if debug:
        sys.stdout.write("\033[J\033[?25l")
    lab_map = [bytearray(row.encode()) for row in input_string.split()]
    visited_map, loop = explore_lab_map(copy.deepcopy(lab_map))
    visited_count = compute_visited_count(visited_map)
    loop_count = compute_loop_count(lab_map, visited_map)
    return visited_count, loop_count

def explore_lab_map(lab_map):
    has_loop = False
    visited_map = copy.deepcopy(lab_map)
    collisions = []

    guard_position, guard_direction = locate_guard(lab_map)
    visited_map[guard_position[0]][guard_position[1]] = ord("o")
    next_position = compute_next_position(guard_position, guard_direction)
    while (0 <= next_position[0] < len(lab_map)) and (0 <= next_position[1] < len(lab_map[0])):
        if debug:
            print_debug_info(lab_map, guard_position, guard_direction)
            time.sleep(0.1)
        cell = lab_map[next_position[0]][next_position[1]]
        if cell == ord("#"):
            collision = (next_position, guard_direction)
            if (collision in collisions):
                has_loop = True
                break
            collisions.append(collision)
            guard_direction = compute_next_direction(guard_direction)
        elif cell == ord("."):
            lab_map[guard_position[0]][guard_position[1]] = ord(".")
            lab_map[next_position[0]][next_position[1]] = direction_to_cell[guard_direction]
            visited_map[next_position[0]][next_position[1]] = ord("o")
            guard_position = next_position
        else:
            raise UserWarning(f"Invalid cell value {cell}")
        next_position = compute_next_position(guard_position, guard_direction)
    return visited_map, has_loop

def locate_guard(lab_map):
    for i in range(len(lab_map)):
        for j in range(len(lab_map[0])):
            if lab_map[i][j] in cell_to_direction:
                return (i, j), cell_to_direction[lab_map[i][j]]

def compute_next_position(position, direction):
    return (position[0] + direction[0], position[1] + direction[1])

def compute_next_direction(direction):
    return (direction[1], direction[0]*-1)

def print_debug_info(lab_map, guard_position, guard_direction):
    terminal_size = os.get_terminal_size()
    height = terminal_size.lines - 2
    width = terminal_size.columns
    row_start = max(0, guard_position[0] - height//2)
    row_end = min(len(lab_map), row_start + height)
    column_start = max(0, guard_position[1] - width//2)
    column_end = min(len(lab_map[0]), column_start + width)
    row_slice, column_slice = slice(row_start, row_end), slice(column_start, column_end)
    sys.stdout.write("\033[H")
    print(f"POS: {guard_position}, DIR: {guard_direction}".ljust(width))
    print("\n".join(bytes(row[column_slice].ljust(width)).decode() for row in lab_map[row_slice]))

def compute_visited_count(visited_map):
    visited_count = sum(row.count(b"o") for row in visited_map)
    return visited_count

def compute_loop_count(lab_map, visited_map):
    loop_count = 0
    for i in range(len(lab_map)):
        for j in range(len(lab_map[0])):
            if visited_map[i][j] == ord("o") and lab_map[i][j] not in cell_to_direction:
                new_lab_map = copy.deepcopy(lab_map)
                new_lab_map[i][j] = ord("#")
                _, has_loop = explore_lab_map(new_lab_map)
                loop_count += has_loop
    return loop_count
