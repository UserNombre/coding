from operator import lt, add

sample_input = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""

sample_result = (3)

def solve(input_string):
    patterns = [pattern for pattern in input_string.strip().split("\n\n")]
    locks = [compute_heights(pattern.split()) for pattern in patterns if pattern[0][0] == "#"]
    keys = [compute_heights(pattern.split()[::-1]) for pattern in patterns if pattern[0][0] == "."]
    matches = compute_matches(locks, keys)
    return matches

def compute_heights(rows):
    heights = [0]*len(rows[0])
    for height, row in enumerate(rows):
        for pin, cell in enumerate(row):
            if cell == "#":
                heights[pin] = height
    return heights

def compute_matches(locks, keys):
    matches = 0
    for lock in locks:
        for key in keys:
            total_heights = map(add, lock ,key)
            if all(map(lt, total_heights, [6, 6, 6, 6, 6])):
                if debug:
                    print(lock, key)
                matches += 1
    return matches
