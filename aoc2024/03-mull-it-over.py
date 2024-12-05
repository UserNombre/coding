import re

sample_input = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""

sample_result = (161, 48)

def solve(input_string):
    instructions = re.findall(r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))", input_string)
    program_result_v1 = compute_program_result_v1(instructions)
    program_result_v2 = compute_program_result_v2(instructions)
    return program_result_v1, program_result_v2

def compute_program_result_v1(instructions):
    instructions = filter(lambda x: x.startswith("mul"), instructions)
    program_result = sum(map(compute_mul_result, instructions))
    return program_result

def compute_program_result_v2(instructions):
    program_result = 0
    execute = True
    for instruction in instructions:
        if instruction == "do()":
            execute = True
        elif instruction == "don't()":
            execute = False
        elif execute:
            program_result += compute_mul_result(instruction)
    return program_result

def compute_mul_result(instruction):
    factors = instruction[4:-1].split(",")
    result = int(factors[0])*int(factors[1])
    return result
