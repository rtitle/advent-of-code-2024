from typing import List, Tuple

def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

def parse_line(line: str) -> Tuple[int, List[int]]:
    s = line.split(":")
    target = int(s[0])
    o = s[1].split(" ")
    ops = [int(x.strip()) for x in o if x != '']
    return (target, ops)

def do_day(lines: List[Tuple[int, List[int]]], part2: bool) -> int:
    def inner(target: int, line: List[int]) -> bool:
        if len(line) == 1:
            return target == line[0]
        
        last = line[-1]        
        res = False
        if target - last > 0:
            res = res or inner(target - last, line[:-1])
        if target % last == 0:
            res = res or inner(int(target / last), line[:-1])
        
        if part2:
            last_str = str(last)
            target_str = str(target)
            if target_str.endswith(last_str) and not target == last:
                len_target = len(target_str)
                len_last = len(last_str)
                x = int(target_str[:(len_target - len_last)])
                res = res or inner(x, line[:-1])

        return res
        
    res = 0
    for target, line in lines:
        if inner(target, line):
            res += target
    return res

filename = "day7/test-input.txt"
filename = "day7/input.txt"
lines = [parse_line(x) for x in read_file(filename)]
part1 = do_day(lines, False)
print(part1)
part2 = do_day(lines, True)
print(part2)