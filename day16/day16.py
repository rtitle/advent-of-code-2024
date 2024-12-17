from enum import IntEnum
from typing import Optional
from dataclasses import dataclass
import heapq
import itertools
import math

class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

_all_directions = [d for d in Direction]

def rotate(dir: Direction) -> list[Direction]:
    if dir == Direction.NORTH:
        return [Direction.EAST, Direction.WEST]
    if dir == Direction.EAST:
        return [Direction.SOUTH, Direction.NORTH]
    if dir == Direction.SOUTH:
        return [Direction.EAST, Direction.WEST]
    if dir == Direction.WEST:
        return [Direction.SOUTH, Direction.NORTH]

@dataclass(frozen=True, order=True)
class Position:
    x: int
    y: int
    dir: Optional[Direction] = None

def parse_input(filename: str) -> tuple[list[str], Position, Position]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    start = None
    end = None
    for y, ln in enumerate(lines):
        for x, s in enumerate(ln):
            if s == "S":
                start = Position(x, y, Direction.EAST)
            elif s == "E":
                end = Position(x, y)
            if start and end:
                break
        if start and end:
            break
    return lines, start, end

def get_neighbors(map: list[str], pos: Position) -> dict[Position, float]:
    res = {}
    for d in rotate(pos.dir):
        res[Position(pos.x, pos.y, d)] = 1000

    move = None
    if pos.dir == Direction.EAST and map[pos.y][pos.x+1] != "#":
        move = Position(pos.x+1, pos.y, pos.dir)
    elif pos.dir == Direction.WEST and map[pos.y][pos.x-1] != "#":
        move = Position(pos.x-1, pos.y, pos.dir)
    elif pos.dir == Direction.NORTH and map[pos.y-1][pos.x] != "#":
        move = Position(pos.x, pos.y-1, pos.dir)
    elif pos.dir == Direction.SOUTH and map[pos.y+1][pos.x] != "#":
        move = Position(pos.x, pos.y+1, pos.dir)
        
    if move:
        res[move] = 1
    return res

def dijkstra(map: list[str], start: Position) -> dict[Position, float]:
    distances = {Position(*node): math.inf for node in itertools.product(range(0, len(map[0])), range(0, len(map)), _all_directions)}
    distances[start] = 0
    visited = set()
    pq = [(0, start)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor, weight in get_neighbors(map, current_node).items():
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(pq, (new_distance, neighbor))

    return distances

def do_part_1(distances: dict[Position, float], end: Position) -> int:
    min = math.inf
    for k, v in distances.items():
        if k.x == end.x and k.y == end.y and v < min:
            min = v

    return min

def find_all_paths(map: list[str], distances: dict[Position, float], 
                   start: Position, end: Position, 
                   cost: float = 0, path: list[Position] = []) -> list[list[Position]]:
    path = path + [start]
    if start.x == end.x and start.y == end.y:
        return [path]
    paths = []
    for node, c in get_neighbors(map, start).items():
        if cost + c == distances[node]:
            newpaths = find_all_paths(map, distances, node, end, cost + c, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def do_part_2(paths: list[list[Position]]) -> int:
    s = set()
    for path in paths:
        for pos in path:
            s.add((pos.x, pos.y))
    return len(s)

filename = "day16/test-input.txt"
filename = "day16/input.txt"
map, start, end = parse_input(filename)
distances = dijkstra(map, start)
part1 = do_part_1(distances, end)
print(part1)
paths = find_all_paths(map, distances, start, end)
part2 = do_part_2(paths)
print(part2)