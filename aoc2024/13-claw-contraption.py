import re
import numpy as np

try:
    from itertools import batched
except:
    def batched(iterable, n):
        return zip(*[iter(iterable)]*n)

sample_input = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

sample_result = (480, 875318608908)

def solve(input_string):
    numbers = [int(x) for x in re.findall(r"\d+", input_string)]
    claws = [([a_x, a_y],[b_x, b_y],[p_x, p_y]) for a_x, a_y, b_x, b_y, p_x, p_y in batched(numbers, 6)]
    total_tokens_v1 = compute_total_tokens(claws, (0, 0))
    total_tokens_v2 = compute_total_tokens(claws, (10000000000000, 10000000000000))
    return total_tokens_v1, total_tokens_v2

def compute_total_tokens(claws, prize_offset):
    total_tokens = 0
    for claw in claws:
        tokens = compute_machine_tokens(*claw, prize_offset)
        if tokens >= 0:
            total_tokens += tokens
    return total_tokens

def compute_machine_tokens(a_movement, b_movement, prize_position, prize_offset):
    prize_position = np.array(prize_position) + prize_offset
    pushes_to_position = np.array([a_movement, b_movement]).T
    position_to_pushes = np.linalg.inv(pushes_to_position)
    button_pushes = position_to_pushes.dot(prize_position).round().astype(int)
    computed_prize_position = pushes_to_position.dot(button_pushes)

    if not (computed_prize_position == prize_position).all():
        return -1
    if prize_offset == (0, 0):
        if not 0 < button_pushes[0] <= 100 or not 0 < button_pushes[1] <= 100:
            return -2
    else:
        if not 0 < button_pushes[0] or not 0 < button_pushes[1]:
            return -2

    tokens = button_pushes[0]*3 + button_pushes[1]
    return tokens
