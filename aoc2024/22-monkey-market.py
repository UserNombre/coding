import numpy as np
from itertools import pairwise
from collections import defaultdict

sample_input = """
1
2
3
2024
"""

sample_result = (37990510, 23)

def solve(input_string):
    seeds = [int(n) for n in input_string.split()]
    secret_lists = [list(compute_secrets(seed, 2000)) for seed in seeds]
    price_lists = [np.array([secret % 10 for secret in secrets]) for secrets in secret_lists]
    change_lists = [np.array([b - a for a,b in pairwise(prices)]) for prices in price_lists]
    sequence_benefits = compute_sequence_benefits(price_lists, change_lists)
    secret_sum = sum(secrets[2000] for secrets in secret_lists)
    max_benefit = max(sequence_benefits.values())
    return secret_sum, max_benefit

def compute_secrets(secret, n):
    for i in range(n+1):
        yield secret
        secret = compute_next_secret(secret)

def compute_next_secret(secret):
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret

def compute_sequence_benefits(price_lists, change_lists):
    sequence_benefits = defaultdict(int)
    for changes, prices in zip(change_lists, price_lists):
        sequence_visited = defaultdict(bool)
        for i, price in enumerate(prices[4:-4]):
            sequence = tuple(changes[i:i+4])
            if price and not sequence_visited[sequence]:
                sequence_benefits[sequence] += price
                sequence_visited[sequence] = True
    return sequence_benefits
