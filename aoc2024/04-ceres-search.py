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

def process_input(input_string):
    rows = input_string.split()
    return rows

def compute_result(data):
    xmas_count_v1 = compute_xmas_count_v1(data)
    xmas_count_v2 = compute_xmas_count_v2(data)
    return xmas_count_v1, xmas_count_v2

def compute_xmas_count_v1(data):
    xmas_count = 0
    sequences = []
    sequences += groups(data, lambda x, y: x)
    sequences += groups(data, lambda x, y: y)
    sequences += groups(data, lambda x, y: x + y)
    sequences += groups(data, lambda x, y: x - y)
    for sequence in sequences:
        matches = re.findall(r"(?=(XMAS|SAMX))", "".join(sequence))
        xmas_count += len(matches)
    return xmas_count

def compute_xmas_count_v2(data):
    xmas_count = 0
    for i in range(1, len(data)-1):
        for j in range(1, len(data[0])-1):
            if data[i][j] == "A":
                if not ((   (data[i-1][j-1] == "M" and data[i+1][j+1] == "S") or
                            (data[i-1][j-1] == "S" and data[i+1][j+1] == "M")) and
                        (   (data[i-1][j+1] == "M" and data[i+1][j-1] == "S") or
                            (data[i-1][j+1] == "S" and data[i+1][j-1] == "M"))):
                    continue
                xmas_count += 1
    return xmas_count

# Based on https://stackoverflow.com/a/43311126
def groups(data, func):
    grouping = defaultdict(list)
    for i in range(len(data)):
        for j in range(len(data[0])):
            grouping[func(j, i)].append(data[i][j])
    return list(map(grouping.get, sorted(grouping)))
