import math
from typing import Optional

def parse_input(filename: str) -> list[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def grid_to_dict(grid: list[str]) -> dict[str, tuple[int]]:
    res = {}
    for j, line in enumerate(grid):
        for i, c in enumerate(line):
            if c != " ":
                res[c] = (i, j)
    return res

def get_directions(start: str, end: str, numeric: bool) -> str:
    d = _numeric if numeric else _directional
    sx, sy = d[start]
    ex, ey = d[end]
    if sx == ex:
        if sy == ey:
            return "A"
        if sy < ey:
            return "v"
        if sy > ey:
            return "^"
    if sx < ex:
         if sy == ey:
            return ">"
         if sy < ey:
            return "v>"
         if sy > ey:
            return "^>"
    if sx > ex:
        if sy == ey:
            return "<"
        if sy < ey:
            return "<v"
        if sy > ey:
            return "<^"
        
def move(start: str, direction: str, numeric: bool) -> Optional[str]:
    d = _numeric if numeric else _directional
    d_inverse = _numeric_inverse if numeric else _directional_inverse
    x, y = d[start]
    x2, y2 = x, y
    if direction == "<":
        x2 -= 1
    elif direction == ">":
        x2 += 1
    elif direction == "^":
        y2 -= 1
    elif direction == "v":
        y2 += 1
    
    if (x2, y2) in d_inverse and d_inverse[(x2, y2)] != " ":
        return d_inverse[(x2, y2)]
    
    return None

def find_paths(start: str, end: str, numeric: bool) -> list[str]:
    if start == end:
        return ["A"]
    
    directions = get_directions(start, end, numeric)
    res = []
    for d in directions:
        new_start = move(start, d, numeric)
        if new_start:
            paths = [d + x for x in find_paths(new_start, end, numeric)]
            res.extend(paths)

    return res

def min_for_code(code: str, depth: int, cache: dict[tuple[str, str, int], int], part1: bool) -> int:
    if part1 and depth == 4 or not part1 and depth == 27:
        return len(code)

    res = 0
    for i in range(0, len(code)):
        a = code[i-1] if i > 0 else "A"
        b = code[i]
        cache_key = (a, b, depth)
        if cache_key in cache:
            res += cache[cache_key]
            continue

        min = math.inf
        expanded_paths = find_paths(a, b, depth == 1)
        for path in expanded_paths:
            c = min_for_code(path, depth+1, cache, part1)
            if c < min:
                min = c
        
        cache[cache_key] = min
        res += min

    return res

def get_total_complexity(codes: list[str], part1: bool = True) -> int:
    res = 0
    cache = {}
    for c in codes:
        path_len = min_for_code(c, 1, cache, part1)
        path_num = int(c.replace("A", ""))
        complexity = path_len * path_num
        res += complexity
    return res

filename = "day21/input.txt"
_numeric = grid_to_dict(["789", "456", "123", " 0A"])
_directional = grid_to_dict([" ^A", "<v>"])
_numeric_inverse = {v:k for k, v in _numeric.items()}
_directional_inverse = {v:k for k, v in _directional.items()}
codes = parse_input(filename)
part1 = get_total_complexity(codes)
print(part1)
part2 = get_total_complexity(codes, part1=False)
print(part2)