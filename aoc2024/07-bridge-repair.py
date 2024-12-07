from operator import add, mul

sample_input = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

sample_result = (3749, 11387)

def solve(input_string):
    lines = input_string.strip().replace(":", "").split("\n")
    equations = [[int(x) for x in line.split()] for line in lines]
    calibration_result_v1 = compute_calibration_result(equations, [add, mul])
    calibration_result_v2 = compute_calibration_result(equations, [add, mul, lambda x,y: int(str(x) + str(y))])
    return calibration_result_v1, calibration_result_v2

def compute_calibration_result(equations, valid_operators):
    calibration_result = 0
    for equation in equations:
        if is_equation_satisfiable(equation[0], equation[1:], [], valid_operators):
            calibration_result += equation[0]
    return calibration_result

def is_equation_satisfiable(result, operands, operators, valid_operators):
    if len(operators) < len(operands)-1:
        return any(is_equation_satisfiable(result, operands, operators + [operator], valid_operators)
                   for operator in valid_operators)
    computed_result = compute_operations(operands, operators)
    return result == computed_result

def compute_operations(operands, operators):
    value = operands[0]
    for i in range(len(operators)):
        value = operators[i](value, operands[i+1])
    return value
