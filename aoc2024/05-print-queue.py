from functools import cmp_to_key
from collections import defaultdict

sample_input = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

sample_result = (143, 123)

def solve(input_string):
    rules, _, updates = input_string.partition("\n\n")
    rules = [[int(page) for page in rule.split("|")] for rule in rules.split()]
    updates = [[int(page) for page in update.split(",")] for update in updates.split()]
    rulemap = compute_rulemap(rules)
    correct_updates_result = compute_correct_updates(rulemap, updates)
    incorrect_updates_result = compute_incorrect_updates(rulemap, updates)
    return correct_updates_result, incorrect_updates_result

def compute_rulemap(rules):
    rulemap = defaultdict(list)
    for rule in rules:
        rulemap[rule[0]].append(rule[1])
    return rulemap

def compute_correct_updates(rulemap, updates):
    result = 0
    for update in updates:
        if is_update_correct(rulemap, update):
            result += update[len(update)//2]
    return result

def compute_incorrect_updates(rulemap, updates):
    result = 0
    for update in updates:
        if not is_update_correct(rulemap, update):
            update = sorted(update, key=cmp_to_key(lambda x, y: -1 if y in rulemap[x] else 1))
            result += update[len(update)//2]
    return result

def is_update_correct(rulemap, update):
    for i, target in enumerate(update[:-1]):
        for page in update[i+1:]:
            if page not in rulemap[target]:
                return False
    return True
