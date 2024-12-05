sample_input = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

sample_result = (2, 4)

def solve(input_string):
    reports = list(map(lambda s: list(map(int, s.split())), input_string.strip().split("\n")))
    safe_reports_v1 = compute_safe_reports_v1(reports)
    safe_reports_v2 = compute_safe_reports_v2(reports)
    return safe_reports_v1, safe_reports_v2

def compute_safe_reports_v1(reports):
    safe_reports = 0
    for report in reports:
        safety_score = compute_safety_score(report)
        safe_reports += (safety_score == len(report) - 1)
    return safe_reports

def compute_safe_reports_v2(reports):
    safe_reports = 0
    for report in reports:
        safety_score = compute_safety_score(report)
        if safety_score == len(report) - 1:
            safe_reports += 1
        elif safety_score >= (len(report) - 1) - 3:
            # TODO: only attempt to remove levels where unsafe differences were detected
            for i in range(len(report)):
                dampened_report = report[:i] + report[i+1:]
                safety_score = compute_safety_score(dampened_report)
                if safety_score == len(dampened_report) - 1:
                    safe_reports += 1
                    break
    return safe_reports

def compute_safety_score(report):
    differences = map(lambda x, y: x - y, report[:-1], report[1:])
    safe_differences = filter(lambda x: 0 < abs(x) <= 3, differences)
    safety_score = abs(sum(map(lambda x: min(1, max(-1, x)), safe_differences)))
    return safety_score
