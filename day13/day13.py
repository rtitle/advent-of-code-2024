import re
from itertools import groupby

def parse_button(line: str) -> tuple[int]:
    plus_pattern = r"X\+(\d+), Y\+(\d+)"

    match = re.search(plus_pattern, line)
    if match:
        x = int(match.group(1))
        y = int(match.group(2))
        return x, y
    
    raise Exception("unable to parse button")

def parse_prize(line: str) -> tuple[int]:
    eq_pattern = r"X=(\d+), Y=(\d+)"

    match = re.search(eq_pattern, line)
    if match:
        x = int(match.group(1))
        y = int(match.group(2))
        return x, y
    
    raise Exception("unable to parse prize")

def parse_machine(lines: list[str]) -> tuple[tuple[int]]:
    x1, y1 = parse_button(lines[0])
    x2, y2 = parse_button(lines[1])
    px, py = parse_prize(lines[2])

    return ((x1, x2, px), (y1, y2, py))

def parse_input(filename: str) -> list[tuple[tuple[int]]]:
    with open(filename, 'r') as file:
        data = file.read()
    chunks = [x.split("\n") for x in data.split("\n\n")]
    return [parse_machine(chunk) for chunk in chunks]

def solve(input: tuple[tuple[int]], part1: bool) -> int:
    x_eq, y_eq = input
    (x1, x2, px) = x_eq
    (y1, y2, py) = y_eq

    if not part1:
        px += 10000000000000
        py += 10000000000000

    # x1*a + x2*b = px
    # y1*a + y2*b = py

    # (x1*y1)*a + (x2*y1)*b = y1*px
    # (y1*x1)*a + (y2*x1)*b = x1*py

    # (x2*y1-y2*x1)*b = y1*px-x1*py
    # b = (y1*px-x1*py) / (x2*y1-y2*x1)
    # a = (px-x2*b) / x1

    b = (y1*px-x1*py) / (x2*y1-y2*x1)
    a = (px-x2*b) / x1

    if int(a) == a and int(b) == b:
        return 3*int(a) + int(b)
    
    return 0

filename = "day13/test-input.txt"
filename = "day13/input.txt"
input = parse_input(filename)
part1 = sum([solve(i, True) for i in input])
print(part1)
part2 = sum([solve(i, False) for i in input])
print(part2)