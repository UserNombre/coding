from functools import cache

sample_input = """
125 17
"""

sample_result = (55312, 65601038650482)

def solve(input_string):
    stones = [int(n) for n in input_string.split()]
    processed_stones = process_stones(stones.copy(), count=25)
    total_stones_v1 = compute_total_stones(stones, count=25)
    total_stones_v2 = compute_total_stones(stones, count=75)
    return total_stones_v1, total_stones_v2

def process_stones(stones, count):
    for k in range(count):
        if debug:
            print(k, stones)
        i = 0
        while i != len(stones):
            string = str(stones[i])
            length = len(string)
            if stones[i] == 0:
                stones[i] = 1
            elif length%2 == 1:
                stones[i] *= 2024
            else:
                stones.pop(i)
                stones.insert(i, int(string[:length//2]))
                i += 1
                stones.insert(i, int(string[length//2:]))
            i += 1
    return stones

def compute_total_stones(stones, count):
    total_stones = 0
    for stone in stones:
        total_stones += compute_total_stones_single(stone, count)
    return total_stones

@cache
def compute_total_stones_single(stone, count):
    if count == 0:
        return 1

    string = str(stone)
    length = len(string)
    if stone == 0:
        return compute_total_stones_single(1, count-1)
    elif length%2 == 1:
        return compute_total_stones_single(stone*2024, count-1)
    else:
        return (compute_total_stones_single(int(string[:length//2]), count-1) +
                compute_total_stones_single(int(string[length//2:]), count-1))
