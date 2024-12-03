from typing import List

def parse_reports(filename: str) -> List[List[int]]:
    reports = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            levels = []
            sp = line.split()
            for s in sp:
                levels.append(int(s))
            reports.append(levels)
        return reports

def is_valid(report: List[int]) -> bool:
    safe = True
    prev = None
    increasing = None
    for level in report:
        if not prev:
            prev = level
            continue
        diff = level - prev
        prev = level
        if increasing == None:
            increasing = diff > 0
        if increasing and diff >= 1 and diff <= 3:
            continue
        if not increasing and diff <= -1 and diff >= -3:
            continue
        safe = False
        break
    return safe

def part1(reports: List[List[int]]) -> int:
    return len(list(filter(is_valid, reports)))

def part2(reports: List[List[int]]) -> int:
    total = 0
    for report in reports:
        if is_valid(report):
            total += 1
            continue
        for i in range(len(report)):
            # copy of the list without the current element
            sublist = report[:i] + report[i+1:]
            if is_valid(sublist):
                total += 1
                break
    return total

# filename = 'day2/test-input.txt'
filename = 'day2/input.txt'
reports = parse_reports(filename)
print(part1(reports))
print(part2(reports))
