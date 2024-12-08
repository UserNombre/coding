from operator import add, sub, lt, le
from itertools import combinations
from collections import defaultdict

sample_input = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

sample_result = (14, 34)

def solve(input_string):
    antenna_map = [bytearray(row.encode()) for row in input_string.split()]
    dimensions = (len(antenna_map), len(antenna_map[0]))
    antenna_groups = locate_antenna_groups(antenna_map, dimensions)
    antinode_count_v1 = compute_antinode_count_v1(antenna_groups, dimensions)
    antinode_count_v2 = compute_antinode_count_v2(antenna_groups, dimensions)
    return antinode_count_v1, antinode_count_v2

def locate_antenna_groups(antenna_map, dimensions):
    antenna_groups = defaultdict(list)
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            cell = antenna_map[i][j]
            if cell != ord("."):
                antenna_groups[cell].append((i, j))
    return antenna_groups

def compute_antinode_count_v1(antenna_groups, dimensions):
    antinodes = set()
    for frequency, antennae in antenna_groups.items():
        for A, B in combinations(antennae, 2):
            C = tuple(map(add, B, map(sub, B, A)))
            D = tuple(map(add, A, map(sub, A, B)))
            if is_valid_position(C, dimensions):
                antinodes.add(C)
            if is_valid_position(D, dimensions):
                antinodes.add(D)
    return len(antinodes)

def compute_antinode_count_v2(antenna_groups, dimensions):
    antinodes = set()
    for frequency, antennae in antenna_groups.items():
        for A, B in combinations(antennae, 2):
            AB = tuple(map(sub, B, A))
            BA = tuple(map(sub, A, B))
            C = tuple(map(add, B, AB))
            while is_valid_position(C, dimensions):
                antinodes.add(C)
                C = tuple(map(add, C, AB))
            C = tuple(map(add, C, BA))
            while is_valid_position(C, dimensions):
                antinodes.add(C)
                C = tuple(map(add, C, BA))
    return len(antinodes)

def is_valid_position(position, dimensions):
    return all(map(le, (0, 0), position)) and all(map(lt, position, dimensions))
