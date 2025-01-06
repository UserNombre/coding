from functools import cache

sample_input = """
029A
980A
179A
456A
379A
"""

sample_result = (126384, 154115708116294)

numeric_to_position = {
    "7": (0, 0), "8": (0, 1), "9": (0, 2),
    "4": (1, 0), "5": (1, 1), "6": (1, 2),
    "1": (2, 0), "2": (2, 1), "3": (2, 2),
    " ": (3, 0), "0": (3, 1), "A": (3, 2),
}

directional_to_position = {
    " ": (0, 0), "^": (0, 1), "A": (0, 2),
    "<": (1, 0), "v": (1, 1), ">": (1, 2),
}

def solve(input_string):
    codes = input_string.split()
    total_complexity_v1 = sum(int(code[:-1]) * compute_remote_length(code, 0, 3) for code in codes)
    total_complexity_v2 = sum(int(code[:-1]) * compute_remote_length(code, 0, 26) for code in codes)
    return (total_complexity_v1, total_complexity_v2)

@cache
def compute_remote_length(keys, depth, operator_depth):
    if depth == operator_depth:
        return len(keys)
    elif depth == 0:
        key_to_position = numeric_to_position
    else:
        key_to_position = directional_to_position
    remote_length = 0
    for start_key, end_key in zip("A" + keys, keys):
        remote_keys = movement_to_keys(key_to_position[start_key], key_to_position[end_key], key_to_position[" "])
        remote_length += compute_remote_length(remote_keys, depth+1, operator_depth)
    return remote_length

@cache
def movement_to_keys(start_position, end_position, forbidden_position):
    movement = (end_position[0]-start_position[0], end_position[1]-start_position[1])
    vertical_key = "^" if movement[0] < 0 else "v"
    horizontal_key = "<" if movement[1] < 0 else ">"
    if horizontal_key == "<":
        if (start_position[0], end_position[1]) != forbidden_position:
            keys = horizontal_key * abs(movement[1]) + vertical_key * abs(movement[0])
        else:
            keys = vertical_key * abs(movement[0]) + horizontal_key * abs(movement[1])
    else:
        if (end_position[0], start_position[1]) != forbidden_position:
            keys = vertical_key * abs(movement[0]) + horizontal_key * abs(movement[1])
        else:
            keys = horizontal_key * abs(movement[1]) + vertical_key * abs(movement[0])
    return keys + "A"
