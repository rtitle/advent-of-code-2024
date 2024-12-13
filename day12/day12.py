from collections import deque
from enum import Enum
from itertools import product
from typing import Optional

type Coord = tuple[int, int]

class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

all_directions = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]

def parse_map(filename: str) -> list[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

def in_range(map: list[str], coord: Coord) -> bool:
    x, y = coord
    return x >= 0 and x < len(map[0]) and y >= 0 and y < len(map)

def move(coord: Coord, dir: Direction) -> Coord:
    x, y = coord
    match dir:
        case Direction.NORTH:
            return (x, y-1)
        case Direction.SOUTH:
            return (x, y+1)
        case Direction.EAST:
            return (x+1, y)
        case Direction.WEST:
            return (x-1, y)
        
def get_plant(map: list[str], coord: Coord) -> int:
    x, y = coord
    return map[y][x]

def get_neighbor(map: list[str], coord: Coord, dir: Direction) -> Optional[Coord]:
    new_coord = move(coord, dir)
    if in_range(map, new_coord) and get_plant(map, coord) == get_plant(map, new_coord):
        return new_coord
    return None

def get_neighbors(map: list[str], coord: Coord) -> list[Coord]:
    return filter(lambda x: x, [get_neighbor(map, coord, d) for d in all_directions])

def get_perimeter_directions(map: list[str], coord: Coord) -> list[Direction]:
    res = []
    for dir in all_directions:
        if get_neighbor(map, coord, dir) == None:
            res.append(dir)
    return res

def get_perimeter_part2(map: list[str], coord: Coord, dirs: list[Direction]) -> int:
    res = 0
    for dir in dirs:
        if dir == Direction.WEST or dir == Direction.EAST:
            c2 = get_neighbor(map, coord, Direction.NORTH)
            if c2:
                if dir not in get_perimeter_directions(map, c2):
                    res += 1
            else:
                res += 1
        if dir == Direction.NORTH or dir == Direction.SOUTH:
            c2 = get_neighbor(map, coord, Direction.WEST)
            if c2:
                if dir not in get_perimeter_directions(map, c2):
                    res += 1
            else: 
                res += 1
    return res

def get_price(map: list[str], start: Coord, visited: set[Coord], part2: bool) -> int:
    queue = deque([start])
    area = 0
    perimeter = 0

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            area += 1
            dirs = get_perimeter_directions(map, node)
            p = get_perimeter_part2(map, node, dirs) if part2 else len(dirs)
            perimeter += p
            for neighbor in get_neighbors(map, node):
                if neighbor not in visited:
                    queue.append(neighbor)

    return area * perimeter

def get_total_price(map: list[str], part2: bool) -> int:
    visited = set()
    total = 0
    for coord in product(range(0, len(map)), range(0, len(map[0]))):
        if coord not in visited:
            p = get_price(map, coord, visited, part2)
            total += p
    return total

# filename = "day12/test-input.txt"
filename = "day12/input.txt"
map = parse_map(filename)
part1 = get_total_price(map, False)
print(part1)
part2 = get_total_price(map, True)
print(part2)