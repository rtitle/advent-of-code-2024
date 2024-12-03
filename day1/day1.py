from collections import defaultdict
from typing import List, Tuple

def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        return file.readlines()

def partition(lines: List[str]) -> Tuple[List[int], List[int]]:
    left = []
    right = []
    for line in lines:
        s = line.split()
        left.append(int(s[0]))
        right.append(int(s[1]))
    return (left, right)

def part1(lines: List[str]) -> int:
    (left, right) = partition(lines)
    left.sort()
    right.sort()
    total = 0
    for i in range(0, len(left)):
        distance = abs(left[i] - right[i])
        total += distance
    return total

def part2(lines: List[str]) -> int:
    (left, right) = partition(lines)
    counts = defaultdict(int)
    for n in right:
        counts[n] = counts[n] + 1
    similarity = 0
    for n in left:
        similarity += (n * counts[n])
    return similarity


# file = 'day1/test-input.txt'
file = 'day1/input.txt'
lines = read_file(file)

print(part1(lines))
print(part2(lines))