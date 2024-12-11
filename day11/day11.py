from functools import lru_cache

def parse_stones(filename: str) -> list[int]:
    with open(filename, 'r') as file:
        content = file.read()
    return [int(x) for x in content.split(" ")]

@lru_cache(maxsize=10000000)
def count_stones(n: int, depth: int, max_depth: int) -> int:
    if depth == max_depth:
        return 1
    
    if n == 0:
        return count_stones(1, depth+1, max_depth)
    
    ln = len(str(n))
    if ln % 2 == 0:
        l = int(str(n)[0:int(ln/2)])
        r = int(str(n)[int(ln/2):ln])
        return count_stones(l, depth+1, max_depth) + count_stones(r, depth+1, max_depth)
    
    return count_stones(n * 2024, depth+1, max_depth)

# filename = "day11/test-input.txt"
filename = "day11/input.txt"
stones = parse_stones(filename)
part1 = sum([count_stones(x, 0, 25) for x in stones])
print(part1)
part2 = sum([count_stones(x, 0, 75) for x in stones])
print(part2)