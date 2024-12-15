from operator import add, lt, le

sample_input = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

sample_result = (1930, 1206)

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def solve(input_string):
    plot_map = [bytearray(row.encode()) for row in input_string.split()]
    areas, perimeters, vertices = explore_plot_map(plot_map)
    if debug:
        print("Areas:", areas)
        print("Perimeters:", perimeters)
        print("Vertices:", vertices)
    fencing_price_v1 = sum([area*perimeter for area, perimeter in zip(areas, perimeters)])
    fencing_price_v2 = sum([area*vertex_number for area, vertex_number in zip(areas, vertices)])
    return fencing_price_v1, fencing_price_v2

def explore_plot_map(plot_map):
    region = 0
    areas = []
    perimeters = []
    dimensions = (len(plot_map), len(plot_map[0]))
    region_map = [[-1]*dimensions[0] for _ in range(dimensions[1])]
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            if region_map[i][j] == -1:
                area, perimeter = explore_plot_region(plot_map, region_map, plot_map[i][j], region, (i, j))
                areas.append(area)
                perimeters.append(perimeter)
                region += 1
    vertices = [0]*region
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            region = map_get(region_map, (i, j))
            vertices[region] += compute_vertex_number(region_map, (i, j))
    if debug:
        print("\n".join(row.decode() for row in plot_map))
        print("\n".join(str(row) for row in region_map))
    return areas, perimeters, vertices

def explore_plot_region(plot_map, region_map, plot_type, region, position):
    region_map[position[0]][position[1]] = region
    area = 1
    perimeter = 0
    dimensions = (len(plot_map), len(plot_map[0]))
    for direction in directions:
        next_position = tuple(map(add, position, direction))
        if not is_valid_position(next_position, dimensions):
            perimeter += 1
        else:
            next_plot_type = plot_map[next_position[0]][next_position[1]]
            next_region = region_map[next_position[0]][next_position[1]]
            if next_plot_type != plot_type:
                perimeter += 1
            elif next_region == -1:
                next_area, next_perimeter = explore_plot_region(plot_map, region_map, plot_type, region, next_position)
                area += next_area
                perimeter += next_perimeter
    return area, perimeter

def compute_vertex_number(region_map, position):
    vertex_number = 0
    up_region = map_get(region_map, tuple(map(add, position, (-1, 0))))
    down_region = map_get(region_map, tuple(map(add, position, (1, 0))))
    left_region = map_get(region_map, tuple(map(add, position, (0, -1))))
    right_region = map_get(region_map, tuple(map(add, position, (0, 1))))
    region = region_map[position[0]][position[1]]
    if up_region != region:
        if left_region != region:
            vertex_number += 1
        if right_region != region:
            vertex_number += 1
    else:
        up_left_region = map_get(region_map, tuple(map(add, position, (-1, -1))))
        up_right_region = map_get(region_map, tuple(map(add, position, (-1, 1))))
        if left_region == region and up_left_region != region:
            vertex_number += 1
        if right_region == region and up_right_region != region:
            vertex_number += 1
    if down_region != region:
        if left_region != region:
            vertex_number += 1
        if right_region != region:
            vertex_number += 1
    else:
        down_left_region = map_get(region_map, tuple(map(add, position, (1, -1))))
        down_right_region = map_get(region_map, tuple(map(add, position, (1, 1))))
        if left_region == region and down_left_region != region:
            vertex_number += 1
        if right_region == region and down_right_region != region:
            vertex_number += 1
    return vertex_number

def map_get(grid, position):
    dimensions = (len(grid), len(grid[0]))
    return grid[position[0]][position[1]] if is_valid_position(position, dimensions) else -1

def is_valid_position(position, dimensions):
    return all(map(le, (0, 0), position)) and all(map(lt, position, dimensions))
