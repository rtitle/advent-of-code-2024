from functools import cmp_to_key
from itertools import groupby
from typing import Dict, List, Tuple

def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

def get_rules_and_updates(lines: List[str]) -> Tuple[List[str], List[str]]:
    groups = [list(g) for k, g in groupby(lines, key=lambda x: x != '')]
    return groups[0], groups[2]

def process_rules(rules: List[str]) -> Dict[int, List[int]]:
    res = {}
    for rule in rules:
        split = rule.split("|")
        before = int(split[0])
        after = int(split[1])
        if before in res:
            res[before].append(after)
        else:
            res[before] = [after]
    return res

def process_updates(updates: List[str]) -> List[List[int]]:
    return [[int(x) for x in update.split(",")] for update in updates]

def get_comparator(rules: Dict[int, List[int]]):
    def compare(a: int, b: int) -> int:
        ar = rules.get(a)
        br = rules.get(b)
        # assume no cycles
        if ar and b in ar:
            return -1
        if br and a in br:
            return 1
        return 0
    return compare

def do_both_parts(rules: Dict[int, List[int]], updates: List[List[int]]) -> Tuple[int, int]:
    part1 = 0
    part2 = 0
    for update in updates:
        s = sorted(update, key=cmp_to_key(get_comparator(rules)))
        middle = s[int(len(s) / 2)]
        if s == update:
            part1 += middle
        else:
            part2 += middle
    return part1, part2

# filename = "day5/test-input.txt"
filename = "day5/input.txt"
lines = read_file(filename)
rules, updates = get_rules_and_updates(lines)
processed_rules = process_rules(rules)
processed_updates = process_updates(updates)
part1, part2 = do_both_parts(processed_rules, processed_updates)
print(part1)
print(part2)