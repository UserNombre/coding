import os
import sys
import time
import numpy as np

sample_input = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""

sample_result = (2028,)

movement_to_direction = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}

def solve(input_string):
    warehouse_map, _, robot_movements = input_string.strip().partition("\n\n")
    warehouse_map = np.array([list(row.encode()) for row in warehouse_map.split()])
    robot_movements = robot_movements.replace("\n", "")
    simulate_warehouse_robot(warehouse_map, robot_movements)
    gps_coordinates = compute_gps_coordinates(warehouse_map)
    return gps_coordinates,

def simulate_warehouse_robot(warehouse_map, robot_movements):
    robot_present = warehouse_map == ord("@")
    assert robot_present.any(), "robot not present in map"
    robot_position = np.array(np.unravel_index(np.argmax(robot_present), warehouse_map.shape))

    for movement in robot_movements:
        if debug:
            print_debug_info(warehouse_map, robot_position)
        direction = movement_to_direction[movement]
        next_position = robot_position + direction
        next_cell = warehouse_map[*next_position]
        if next_cell == ord("#"):
            pass
        elif next_cell == ord("."):
            warehouse_map[*robot_position] = ord(".")
            warehouse_map[*next_position] = ord("@")
            robot_position = next_position
        elif next_cell == ord("O"):
            push_position = next_position.copy()
            while warehouse_map[*push_position] != ord("#"):
                if warehouse_map[*push_position] == ord("."):
                    warehouse_map[*push_position] = ord("O")
                    warehouse_map[*robot_position] = ord(".")
                    warehouse_map[*next_position] = ord("@")
                    robot_position = next_position
                    break
                push_position += direction
        else:
            raise AssertionError(f"invalid cell value {next_cell}")
    if debug:
        print_debug_info(warehouse_map, robot_position)

    return warehouse_map

def compute_gps_coordinates(warehouse_map):
    box_positions = np.where(warehouse_map == ord("O"))
    return int(sum(100*i + j for (i, j) in zip(*box_positions)))

def print_debug_info(warehouse_map, robot_position):
    header = f"POS: {tuple(robot_position)}"
    helpers.print_2d_debug_info(header, warehouse_map, robot_position, 0.1)
