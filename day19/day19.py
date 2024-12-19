from functools import lru_cache

def parse_input(filename: str) -> tuple[set[str], list[str]]:
    with open(filename, 'r') as file:
        lines = file.read()
    [patterns, designs] = lines.split("\n\n")
    return set(patterns.split(", ")), designs.split("\n")

@lru_cache(maxsize=100000)
def count_pattern_combos(target_design: str) -> int:
    if target_design == "":
        return 1
    
    total = 0
    upper = min(len(target_design)+1, _max_pattern_len+1)
    for i in range(1, upper):
        s = target_design[:i]
        if s in _patterns:
            total += count_pattern_combos(target_design[len(s):])
    
    return total

def do_part_1(designs: list[str]) -> int:
    return len(list(filter(lambda x: x > 0, [count_pattern_combos(d) for d in designs])))

def do_part_2(designs: list[str]) -> int:
    return sum(count_pattern_combos(d) for d in designs)

filename = "day19/input.txt"
_patterns, designs = parse_input(filename)
_max_pattern_len = max(len(x) for x in _patterns)
part1 = do_part_1(designs)
print(part1)
part2 = do_part_2(designs)
print(part2)