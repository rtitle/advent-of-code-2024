
import heapq
from itertools import product
import math

type Coord = tuple[int, int]

def parse_input(filename: str) -> list[Coord]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    res = []
    for line in lines:
        [x, y] = line.split(",")
        res.append((int(x), int(y)))
    return res

def in_bounds(coord: Coord) -> bool:
    x, y = coord
    return x >= 0 and x < _xlen and y >= 0 and y < _ylen

def get_neighbors(bytes: set[Coord], cur: Coord) -> list[Coord]:
    x, y = cur
    res = []
    possible = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    for p in possible:
        if in_bounds(p) and p not in bytes:
            res.append(p)
    return res

def dijkstra(bytes: set[Coord], start: Coord = (0, 0)) -> dict[Coord, float]:
    distances = {(x, y): math.inf for x, y in product(range(0, _xlen), range(0, _ylen))}
    distances[start] = 0
    visited = set()
    pq = [(0, start)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor in get_neighbors(bytes, current_node):
            new_distance = current_distance + 1
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(pq, (new_distance, neighbor))

    return distances

def do_part_1(bytes: set[Coord]) -> int:
    distances = dijkstra(bytes)
    return int(distances[(_xlen-1, _ylen-1)])

def do_part_2(bytes: list[Coord]) -> Coord:
    for i in range(_max_bytes, len(bytes)):
        trunc_bytes = bytes[:i]
        distances = dijkstra(set(trunc_bytes))
        if distances[(_xlen-1, _ylen-1)] == math.inf:
            return bytes[i-1]
    return (0, 0)

# _xlen = 7
# _ylen = 7
# _max_bytes = 12
# filename = "day18/test-input.txt"

_xlen = 71
_ylen = 71
_max_bytes = 1024
filename = "day18/input.txt"

bytes = parse_input(filename)
trunc_bytes = bytes[:_max_bytes+1]
part1 = do_part_1(set(trunc_bytes))
print(part1)
x,y = do_part_2(bytes)
part2 = f"{x},{y}"
print(part2)