import re

def read_file(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()

def compute(data: str) -> int:
    matches = re.findall(r'mul\((\d+),(\d+)\)', data)
    return sum([int(x) * int(y) for (x,y) in matches])

def process_part2(data: str) -> str:
    new_data = data
    while True:
        dont_idx = new_data.find("don't()")
        do_idx = new_data[dont_idx:].find("do()")

        if dont_idx == -1:
            break
        
        if do_idx == -1:
            new_data = new_data[:dont_idx]
        else:
            do_idx_adj = do_idx + dont_idx + 4
            new_data = new_data[:dont_idx] + new_data[do_idx_adj:]

    return new_data
    
# file = 'day3/test-input.txt'
# file = 'day3/test-input-part2.txt'
file = 'day3/input.txt'
data = read_file(file)

# part 1
print(compute(data))
# part 2
print(compute(process_part2(data)))