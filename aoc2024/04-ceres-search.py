import re
from collections import defaultdict

sample_input = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

sample_result = (18, 9)

def solve(input_string):
    array = input_string.split()
    xmas_count_v1 = compute_xmas_count_v1(array)
    xmas_count_v2 = compute_xmas_count_v2(array)
    return xmas_count_v1, xmas_count_v2

def compute_xmas_count_v1(array):
    xmas_count = 0
    sequences = []
    sequences += groups(array, lambda x, y: x)
    sequences += groups(array, lambda x, y: y)
    sequences += groups(array, lambda x, y: x + y)
    sequences += groups(array, lambda x, y: x - y)
    for sequence in sequences:
        matches = re.findall(r"(?=(XMAS|SAMX))", "".join(sequence))
        xmas_count += len(matches)
    return xmas_count

def compute_xmas_count_v2(array):
    xmas_count = 0
    for i in range(1, len(array)-1):
        for j in range(1, len(array[0])-1):
            if array[i][j] == "A":
                if not ((   (array[i-1][j-1] == "M" and array[i+1][j+1] == "S") or
                            (array[i-1][j-1] == "S" and array[i+1][j+1] == "M")) and
                        (   (array[i-1][j+1] == "M" and array[i+1][j-1] == "S") or
                            (array[i-1][j+1] == "S" and array[i+1][j-1] == "M"))):
                    continue
                xmas_count += 1
    return xmas_count

# Based on https://stackoverflow.com/a/43311126
def groups(array, func):
    grouping = defaultdict(list)
    for i in range(len(array)):
        for j in range(len(array[0])):
            grouping[func(j, i)].append(array[i][j])
    return list(map(grouping.get, sorted(grouping)))
