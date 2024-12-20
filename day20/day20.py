from itertools import combinations
from typing import Callable

def parse_input(filename: str) -> list[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

type Coord = tuple[int]

def find_start_end(racetrack: list[str]) -> tuple[Coord]:
    start = end = None
    for y, line in enumerate(racetrack):
        for x, c in enumerate(line):
            if c == 'S':
                start = (x, y)
            elif c == 'E':
                end = (x, y)
            if start and end:
                break
        if start and end:
            break
    return start, end

def in_bounds(racetrack: list[str], coord: Coord) -> bool:
    xlen = len(racetrack[0])
    ylen = len(racetrack)
    x, y = coord
    return x >= 0 and x < xlen and y >= 0 and y < ylen

def is_wall(racetrack: list[str], coord: Coord) -> bool:
    x, y = coord
    return racetrack[y][x] == '#'

def add(coord1: Coord, coord2: Coord) -> Coord:
    x1, y1 = coord1
    x2, y2 = coord2
    return x1 + x2, y1 + y2

def get_adjacent(racetrack: list[str], coord: Coord) -> list[Coord]:
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    adj = [add(coord, x) for x in moves]
    return [x for x in adj if in_bounds(racetrack, x) and not is_wall(racetrack, x)]

def get_distance(coord1: Coord, coord2: Coord) -> tuple[int]:
    x1, y1 = coord1
    x2, y2 = coord2
    return abs(x1 - x2), abs(y1 - y2)

def get_path(racetrack: list[str]) -> list[Coord]:
    start, end = find_start_end(racetrack)
    cur = start
    visited = set()
    path = []
    while cur != end:
        path.append(cur)
        visited.add(cur)
        cur = next(x for x in get_adjacent(racetrack, cur) if x not in visited)
    path.append(cur)
    return path

def find_cheats(racetrack: list[str], part1: bool, criteria: Callable[[int], bool]) -> int:
    path = get_path(racetrack)
    res = 0
    for ((i1, coord1), (i2, coord2)) in combinations(enumerate(path), 2):
        distance = get_distance(coord1, coord2)
        if (part1 and (distance == (2, 0) or distance == (0, 2))) or (not part1 and sum(distance) <= 20):
            savings = abs(i1 - i2) - sum(distance)
            if criteria(savings):
                res += 1
    return res

filename = "day20/input.txt"
racetrack = parse_input(filename)
part1 = find_cheats(racetrack, True, lambda x: x >= 100)
print(part1)
part2 = find_cheats(racetrack, False, lambda x: x >= 100)
print(part2)