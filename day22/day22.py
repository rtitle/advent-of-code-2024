from collections import defaultdict

def parse_input(filename: str) -> list[int]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [int(line.strip()) for line in lines]

def mix_and_prune(a: int, b: int) -> int:
    return (a ^ b) % 16777216

def process_secret_number(n: int) -> int:
    step1 = mix_and_prune(n, n * 64)
    step2 = mix_and_prune(step1, step1 // 32)
    step3 = mix_and_prune(step2, step2 * 2048)
    return step3

def do_part_1(lines: list[int]) -> int:
    res = 0
    for line in lines:
        x = line
        for _ in range(0, 2000):
            x = process_secret_number(x)
        res += x
    return res

def get_secret_numbers(n: int) -> list[int]:
    res = []
    x = n
    for _ in range(0, 2000):
        x = process_secret_number(x)
        res.append(x)
    return res

def get_changes(lines: list[int]) -> dict[tuple[int], int]:
    res = defaultdict(int)
    for line in lines:
        secrets = [s % 10 for s in get_secret_numbers(line)]
        lineres = {}
        for i in range(4, len(secrets)):
            last = []
            for j in range(i-3, i+1):
                delta = secrets[j] - secrets[j-1]
                last.append(delta)
            if tuple(last) not in lineres:
                lineres[tuple(last)] = secrets[i]
        
        for k, v in lineres.items():
            res[k] = res[k] + v
    return res

def do_part_2(lines: list[str]) -> int:
    changes = get_changes(lines)
    return max(changes.values())

filename = "day22/input.txt"
lines = parse_input(filename)
part1 = do_part_1(lines)
print(part1)
part2 = do_part_2(lines)
print(part2)