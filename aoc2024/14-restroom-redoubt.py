import re
import os
import sys
import time
from operator import mul
from functools import reduce

try:
    from itertools import batched
except:
    def batched(iterable, n):
        return zip(*[iter(iterable)]*n)

sample_input = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

sample_result = (12)

def solve(input_string):
    if debug:
        sys.stdout.write("\033[?25l")
    if mode == "check":
        dimensions = (7, 11)
    else:
        dimensions = (103, 101)
    numbers = [int(x) for x in re.findall(r"-?\d+", input_string)]
    positions = []
    speeds = []
    for p_x, p_y, v_x, v_y in batched(numbers, 4):
        positions.append((p_y, p_x))
        speeds.append((v_y, v_x)) 
    bathroom_map = simulate_bathroom_robots(dimensions, positions, speeds, 10000)
    safety_score = compute_safety_score(bathroom_map, dimensions)
    return safety_score

def simulate_bathroom_robots(dimensions, positions, speeds, seconds):
    bathroom_map = [[0]*dimensions[1] for _ in range(dimensions[0])]
    for position in positions:
        bathroom_map[position[0]][position[1]] += 1
    if debug:
        print_debug_info(bathroom_map, dimensions, 0)
    for i in range(1, seconds+1):
        for j in range(len(positions)):
            position = positions[j]
            speed = speeds[j]
            bathroom_map[position[0]][position[1]] -= 1
            next_position = ((position[0] + speed[0]) % dimensions[0], (position[1] + speed[1]) % dimensions[1])
            bathroom_map[next_position[0]][next_position[1]] += 1
            positions[j] = next_position
        if debug:
            time.sleep(0.1)
            print_debug_info(bathroom_map, dimensions, i)
    return bathroom_map

def compute_safety_score(bathroom_map, dimensions):
    quadrant_score = [0]*4
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            quadrant = get_quadrant(i, j, dimensions)
            if bathroom_map[i][j] and quadrant != -1:
                quadrant_score[quadrant] += bathroom_map[i][j]
    safety_score = reduce(mul, quadrant_score)
    return safety_score

def print_debug_info(bathroom_map, dimensions, step):
    terminal_size = os.get_terminal_size()
    height = terminal_size.lines - 2
    width = terminal_size.columns
    sys.stdout.write("\033[2J\033[H")
    print(f"MAP_DIM: {dimensions} SCREEN_DIM: {(height, width)} STEP: {step}")
    print("\n".join("".join([str(n) if n else "." for n in row[:width]]) for row in bathroom_map[:height]))

def get_quadrant(i, j, dimensions):
    if i < dimensions[0]//2:
        if j < dimensions[1]//2:
            return 0
        elif j > dimensions[1]//2:
            return 1
    elif i > dimensions[0]//2:
        if j < dimensions[1]//2:
            return 2
        elif j > dimensions[1]//2:
            return 3
    return -1
