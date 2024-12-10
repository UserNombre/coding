from operator import add, lt, le

sample_input = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

sample_result = (36, 81)

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def solve(input_string):
    topographic_map = [[int(x) for x in row] for row in input_string.split()]
    map_score_v1 = compute_map_score(topographic_map, True)
    map_score_v2 = compute_map_score(topographic_map, False)
    return map_score_v1, map_score_v2

def compute_map_score(topographic_map, unique):
    map_score = 0
    for i in range(len(topographic_map)):
        for j in range(len(topographic_map[0])):
            if topographic_map[i][j] == 0:
                trailhead_tops = compute_trailhead_tops(topographic_map, (i, j), [])
                if unique:
                    trailhead_tops = set(trailhead_tops)
                map_score += len(trailhead_tops)
                if debug:
                    print((i, j), len(trailhead_tops), trailhead_tops)
    return map_score

def compute_trailhead_tops(topographic_map, position, path):
    height = topographic_map[position[0]][position[1]]
    path.append((height, position))
    if height == 9:
        if debug:
            print(path)
        path.pop()
        return [position]

    tops = []
    dimensions = (len(topographic_map), len(topographic_map[0]))
    for direction in directions:
        next_position = tuple(map(add, position, direction))
        if all(map(le, (0, 0), next_position)) and all(map(lt, next_position, dimensions)):
            next_height = topographic_map[next_position[0]][next_position[1]]
            if next_height == height+1:
                tops.extend(compute_trailhead_tops(topographic_map, next_position, path))
    path.pop()
    return tops
