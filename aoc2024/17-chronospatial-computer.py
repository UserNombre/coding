import re
import sys
import time

sample_input = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

sample_result = "4,6,3,5,6,3,5,2,1,0"

def solve(input_string):
    if debug:
        sys.stdout.write("\033[?25l")
    numbers = [int(x) for x in re.findall(r"\d+", input_string)]
    registers = [0, 1, 2, 3, *numbers[:3], 0]
    program = numbers[3:]
    output = execute_program(registers, program)
    return ",".join([str(x) for x in output])

def execute_program(registers, program):
    output = []
    if debug:
        print_debug_info(registers, program, output)
    while registers[7] < len(program):
        execute_instruction(registers, program, output)
        if debug:
            time.sleep(1)
            print_debug_info(registers, program, output)
    return output

def execute_instruction(registers, program, output):
    opcode = program[registers[7]]
    operand = program[registers[7]+1]
    try:
        if opcode == 0: # adv
            registers[4] = registers[4]//(2**registers[operand])
        elif opcode == 1: # bxl
            registers[5] = registers[5] ^ operand
        elif opcode == 2: # bst
            registers[5] = registers[operand]%8
        elif opcode == 3: # jnz
            if registers[4]:
                registers[7] = operand
                return
        elif opcode == 4: # bxc
            registers[5] = registers[5] ^ registers[6]
        elif opcode == 5: # out
            output.append(registers[operand]%8)
        elif opcode == 6: # bdv
            registers[5] = registers[4]//(2**registers[operand])
        elif opcode == 7: # cdv
            registers[6] = registers[4]//(2**registers[operand])
        else:
            raise UserWarning(f"Invalid instruction opcode '{opcode}'")
    except IndexError:
        raise UserWarning(f"Invalid register number '{operand}'")
    registers[7] += 2

def print_debug_info(registers, program, output):
    sys.stdout.write("\033[2J\033[H")
    print("A", registers[4])
    print("B", registers[5])
    print("C", registers[6])
    print("PC", registers[7])
    print("PROGRAM")
    print(program)
    print(" " * (1 + registers[7]*3) + "^")
    print("OUTPUT")
    print(output)
