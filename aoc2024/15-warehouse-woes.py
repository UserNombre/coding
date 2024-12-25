import os
import sys
import time
import numpy as np

sample_input = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

sample_result = (10092, 9021)

movement_to_direction = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}

def solve(input_string):
    warehouse_map, _, robot_movements = input_string.strip().partition("\n\n")
    wide_warehouse_map = widen_warehouse_map(warehouse_map)
    warehouse_map = np.array([list(row.encode()) for row in warehouse_map.split()])
    wide_warehouse_map = np.array([list(row.encode()) for row in wide_warehouse_map.split()])
    robot_movements = robot_movements.replace("\n", "")

    simulate_warehouse_robot(warehouse_map, robot_movements)
    simulate_warehouse_robot(wide_warehouse_map, robot_movements)
    gps_coordinates = compute_gps_coordinates(warehouse_map, "O")
    gps_coordinates_wide = compute_gps_coordinates(wide_warehouse_map, "[")
    return gps_coordinates, gps_coordinates_wide

def widen_warehouse_map(warehouse_map):
    widened_warehouse = "\n".join("".join(cell*2 for cell in row) for row in warehouse_map.split())
    widened_warehouse = widened_warehouse.replace("OO", "[]").replace("@@", "@.")
    return widened_warehouse

def simulate_warehouse_robot(warehouse_map, robot_movements):
    robot_present = warehouse_map == ord("@")
    assert robot_present.any(), "robot not present in map"
    robot_position = np.array(np.unravel_index(np.argmax(robot_present), warehouse_map.shape))
    for movement in robot_movements:
        direction = movement_to_direction[movement]
        if simulate_move(warehouse_map, robot_position, direction):
            robot_position += direction
        if debug:
            print_debug_info(warehouse_map, robot_position, movement)

def simulate_move(warehouse_map, start_position, direction):
    changes = []
    visited = []
    pending = [(start_position, ord("."))]
    while pending:
        position, new_cell = pending.pop()
        changes.append((position, new_cell))
        cell = warehouse_map[*position]
        if cell == ord("#"):
            return False
        elif cell == ord("."):
            continue

        visited.append(tuple(position))
        pending.append((position + direction, cell))
        if cell not in [ord("@"), ord("O")] and direction[0]:
            side_position = position + (0, 1) if cell == ord("[") else position + (0, -1)
            if tuple(side_position) not in visited:
                pending.append((side_position, ord(".")))

    for position, cell in changes:
        warehouse_map[*position] = cell
    return True

def compute_gps_coordinates(warehouse_map, target):
    box_positions = np.where(warehouse_map == ord(target))
    return int(sum(100*i + j for (i, j) in zip(*box_positions)))

def print_debug_info(warehouse_map, robot_position, movement):
    header = f"POS: {tuple(robot_position)} [{movement}]"
    helpers.print_2d_debug_info(header, warehouse_map, robot_position, 0.1)
