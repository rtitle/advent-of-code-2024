from itertools import product

def parse_map(filename: str) -> list[list[int]]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines = [[int(x) for x in line.strip()] for line in lines]
    return lines

type Coord = tuple[int, int]

def find_zeros(map: list[list[int]]) -> list[Coord]:
    return [(i, j) for i, j in product(range(0, len(map[0])), range(0, len(map))) if map[j][i] == 0]

def in_range(map: list[list[int]], x: int, y: int) -> bool:
    return x >= 0 and x < len(map[0]) and y >= 0 and y < len(map)

def get_adjacent(map: list[list[int]], x: int, y: int) -> list[Coord]:
    steps = [(x + sx, y + sy) for sx, sy in [(0, -1), (0, 1), (-1, 0), (1, 0)]]
    return [(sx, sy) for sx, sy in steps if in_range(map, sx, sy) and map[sy][sx] - map[y][x] == 1]

def get_peaks(map: list[list[int]], node: Coord, visited: set[Coord]) -> int:
    x, y = node
    if map[y][x] == 9 and node not in visited:
        visited.add(node)
        return 1
    
    return sum([get_peaks(map, x, visited) for x in get_adjacent(map, *node)])

def get_paths(map: list[list[int]], node: Coord) -> int:
    x, y = node
    if map[y][x] == 9:
        return 1
    
    return sum([get_paths(map, x) for x in get_adjacent(map, *node)])

filename = "day10/test-input.txt"
filename = "day10/input.txt"
map = parse_map(filename)
zeros = find_zeros(map)
part1 = sum([get_peaks(map, z, set()) for z in find_zeros(map)])
print(part1)
part2 = sum([get_paths(map, z) for z in zeros])
print(part2)