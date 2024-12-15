def parse_line(line: str) -> tuple[tuple[int]]:
    [s1, s2] = line.split(" ")
    p = s1.split("=")[1]
    v = s2.split("=")[1]
    [px, py] = [int(x) for x in p.split(",")]
    [vx, vy] = [int(x) for x in v.split(",")]
    return ((px, py), (vx, vy))

def parse_file(filename: str) -> list[tuple[tuple[int]]]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [parse_line(line.strip()) for line in lines]

def simulate(pos: int, vel: int, len: int, steps: int) -> int:
    return (pos + vel * steps) % len

def do_part1(input: list[tuple[tuple[int]]]) -> int:
    lenx = 101 # 11
    leny = 103 # 7
    midx = 50 # 5
    midy = 51 # 3
    positions = []
    for ((x, y), (vx, vy)) in input:
        newx = simulate(x, vx, lenx, 100)
        newy = simulate(y, vy, leny, 100)
        positions.append((newx, newy))

    q1 = len(list(filter(lambda a: a[0] < midx and a[1] < midy, positions)))
    q2 = len(list(filter(lambda a: a[0] > midx and a[1] < midy, positions)))
    q3 = len(list(filter(lambda a: a[0] < midx and a[1] > midy, positions)))
    q4 = len(list(filter(lambda a: a[0] > midx and a[1] > midy, positions)))
    return q1 * q2 * q3 * q4

def print_grid(positions: list[tuple[int]]) -> None:
    ps = [x[0] for x in positions]
    for i in range(0, 103):
        s = ""
        for j in range(0, 101):
            if (j, i) in ps:
                s += "X"
            else:
                s += "."
        print(s)

def do_part2(positions: list[tuple[tuple[int]]]) -> None:
    i = 0
    while i < 10000:
        lenx = 101
        leny = 103 
        new_positions = []
        for ((x, y), (vx, vy)) in positions:
            newx = simulate(x, vx, lenx, 1)
            newy = simulate(y, vy, leny, 1)
            new_positions.append(((newx, newy), (vx, vy)))
        i += 1
        positions = new_positions
        if i == 6493:
            print_grid(new_positions)
            break
    return i
    
filename = "day14/test-input.txt"
filename = "day14/input.txt"
data = parse_file(filename)
part1 = do_part1(data)
print(part1)
part2 = do_part2(data)
print(part2)