sample_input = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

sample_result = (11, 31)

def solve(input_string):
    numbers = [int(n) for n in input_string.split()]
    left_list = sorted(numbers[::2])
    right_list = sorted(numbers[1::2])
    distance = compute_distance(left_list, right_list)
    similarity = compute_similarity(left_list, right_list)
    return distance, similarity

def compute_distance(left_list, right_list):
    distances = map(lambda x, y: abs(x - y), left_list, right_list)
    total_distance = sum(distances)
    return total_distance

def compute_similarity(left_list, right_list):
    similarities = [i*right_list.count(i) for i in left_list]
    total_similarity = sum(similarities)
    return total_similarity
