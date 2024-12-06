from enum import Enum
from typing import List, Tuple

class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

def get_start_pos(lines: List[str]) -> Tuple[int, int]:
    for j in range(0, len(lines)):
        i = lines[j].find('^')
        if i != -1:
            return (i, j)
    raise Exception("start position not found")

def has_barrier(lines: List[str], x: int, y: int) -> bool:
    return lines[y][x] == '#'

def in_range(lines: List[str], x: int, y: int) -> bool:
    return x >= 0 and y >= 0 and x < len(lines[0]) and y < len(lines)

def get_next_square(x: int, y: int, dir: Direction) -> Tuple[int, int]:
    if dir == Direction.NORTH:
        return (x, y-1)
    if dir == Direction.SOUTH:
        return (x, y+1)
    if dir == Direction.EAST:
        return (x+1, y)
    if dir == Direction.WEST:
        return (x-1, y)
    
def rotate_dir(dir: Direction) -> Direction:
    if dir == Direction.NORTH:
        return Direction.EAST
    if dir == Direction.EAST:
        return Direction.SOUTH
    if dir == Direction.SOUTH:
        return Direction.WEST
    if dir == Direction.WEST:
        return Direction.NORTH

def do_part_1(lines: List[str]) -> int:
    path = set()
    i, j = get_start_pos(lines)
    dir = Direction.NORTH
    while True:
        path.add((i, j))
        i2, j2 = get_next_square(i, j, dir)
        if not in_range(lines, i2, j2):
            break
        if has_barrier(lines, i2, j2):
            dir = rotate_dir(dir)
        else:
            i = i2
            j = j2
    return len(path)

def is_loop(lines: List[str]) -> int:
    path = set()
    i, j = get_start_pos(lines)
    dir = Direction.NORTH
    while True:
        if (i, j, dir) in path:
            return True
        path.add((i, j, dir))
        i2, j2 = get_next_square(i, j, dir)
        if not in_range(lines, i2, j2):
            return False
        if has_barrier(lines, i2, j2):
            dir = rotate_dir(dir)
        else:
            i = i2
            j = j2

# a little brute force, but it works
def do_part_2(lines: List[str]) -> int:
    res = 0
    for j in range(0, len(lines)):
        for i in range(0, len(lines[j])):
            if lines[j][i] == '#' or lines[j][i] == '^':
                continue
            if i == len(lines[j])-1:
                newline = lines[j][:i] + '#'
            else:
                newline = lines[j][:i] + '#' + lines[j][i+1:]
            newlines = lines.copy()
            newlines[j] = newline
            if is_loop(newlines):
                res += 1
    return res

filename = "day6/test-input.txt"
filename = "day6/input.txt"
lines = read_file(filename)
part1 = do_part_1(lines)
print(part1)
part2 = do_part_2(lines)
print(part2)