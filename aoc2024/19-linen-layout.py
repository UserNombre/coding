from functools import cache

sample_input = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

sample_result = (6, 16)

def solve(input_string):
    lines = input_string.strip().split("\n")
    patterns = tuple(lines[0].split(", "))
    designs = lines[2:]
    design_combinations = [compute_design_combinations(design, patterns) for design in designs]
    possible_designs = len(list(filter(None, design_combinations)))
    design_combinations = sum(design_combinations)
    return possible_designs, design_combinations

@cache
def compute_design_combinations(design, patterns):
    if len(design) == 0:
        return 1
    design_combinations = 0
    for pattern in patterns:
        if design.startswith(pattern):
            design_combinations += compute_design_combinations(design[len(pattern):], patterns)
    return design_combinations
