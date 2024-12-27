from collections import defaultdict
from itertools import product

def parse_input(filename: str) -> tuple[list[dict[int, int]]]:
    with open(filename, 'r') as file:
        data = file.read()
    groups = data.split("\n\n")
    locks = []
    keys = []
    for group in groups:
        lines = group.split("\n")
        key = True if "." in lines[0] else False
        col_count = defaultdict(int)
        for line in lines:
            for i, c in enumerate(line):
                if c == "#":
                    col_count[i] += 1
        if key:
            keys.append(col_count)
        else:
            locks.append(col_count)
    return locks, keys

def key_fits_lock(lock: dict[int, int], key: dict[int, int]) -> bool:
    for i in range(0, 5):
        if lock[i] + key[i] > _height:
            return False
    return True

def do_part_1(locks: list[dict[int, int]], keys: list[dict[int, int]]) -> int:
    return len([x for x in product(locks, keys) if key_fits_lock(*x)])

_height = 7
filename = "day25/input.txt"
locks, keys = parse_input(filename)
part1 = do_part_1(locks, keys)
print(part1)