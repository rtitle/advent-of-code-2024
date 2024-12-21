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


def find_paths(start: str, code: str, numeric: bool, path: list[str] = []) -> list[list[str]]:
    if not code:
        return [path]
    
    paths = []
    directions = get_directions(start, code[0], numeric)
    for d in directions:
        new_start = move(start, d, numeric)
        if new_start:
            new_code = code[1:] if d == "A" else code
            new_path = path + [d]
            paths.extend(find_paths(new_start, new_code, numeric, new_path))

    return paths

def find_min_path(code: str, depth: int = 1) -> int:
    if depth == 4:
        return len(code)
    
    paths = find_paths("A", code, depth == 1)
    res = math.inf
    for p in paths:
        path_len = find_min_path(p, depth + 1)
        if path_len < res:
            res = path_len

    return res

def do_part_1(codes: list[str]) -> int:
    res = 0
    for c in codes:
        path_len = find_min_path(c)
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
part1 = do_part_1(codes)
print(part1)