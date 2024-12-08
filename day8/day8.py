from collections import defaultdict
from itertools import combinations

Coord = tuple[int, int]

def read_file(filename: str) -> list[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

def get_nodes(lines: list[str]) -> dict[str, list[Coord]]:
    pairs = defaultdict(list)
    for j in range(0, len(lines)):
        for i in range(0, len(lines[j])):
            if lines[j][i] != '.':
                pairs[lines[j][i]].append((i, j))
    return pairs

def in_bounds(coord: Coord, boundx: int, boundy: int) -> bool:
    x, y = coord
    return x >= 0 and x < boundx and y >= 0 and y < boundy

def get_antinodes(nodes: dict[str, list[Coord]], boundx: int, boundy: int) -> list[Coord]:
    res = set()
    for coords in nodes.values():
        for (x1, y1), (x2, y2) in combinations(coords, 2):
            diffx = abs(x2 - x1)
            diffy = abs(y2 - y1)
            newx1 = x1 + diffx if x1 > x2 else x1 - diffx
            newy1 = y1 + diffy if y1 > y2 else y1 - diffy
            newx2 = x2 + diffx if x2 > x1 else x2 - diffx
            newy2 = y2 + diffy if y2 > y1 else y2 - diffy
            new1 = (newx1, newy1)
            new2 = (newx2, newy2)
            if in_bounds(new1, boundx, boundy):
                res.add(new1)
            if in_bounds(new2, boundx, boundy):
                res.add(new2)
    return res

def get_antinodes2(nodes: dict[str, list[Coord]], boundx: int, boundy: int) -> list[Coord]:
    res = set()
    for coords in nodes.values():
        for (x1, y1), (x2, y2) in combinations(coords, 2):
            diffx = abs(x2 - x1)
            diffy = abs(y2 - y1)
            cur = (x1, y1)
            while in_bounds(cur, boundx, boundy):
                res.add(cur)
                (curx, cury) = cur
                newx1 = curx + diffx if x1 > x2 else curx - diffx
                newy1 = cury + diffy if y1 > y2 else cury - diffy
                cur = (newx1, newy1)
            cur = (x1, y1)
            while in_bounds(cur, boundx, boundy):
                res.add(cur)
                (curx, cury) = cur
                newx2 = curx + diffx if x2 > x1 else curx - diffx
                newy2 = cury + diffy if y2 > y1 else cury - diffy
                cur = (newx2, newy2)
    return res

# filename = "day8/test-input.txt"
filename = "day8/input.txt"
lines = read_file(filename)
nodes = get_nodes(lines)
antinodes = get_antinodes(nodes, len(lines[0]), len(lines))
part1 = len(antinodes)
print(part1)
antinodes2 = get_antinodes2(nodes, len(lines[0]), len(lines))
part2 = len(antinodes2)
print(part2)