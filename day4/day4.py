from typing import List

def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines
 
def count_xmas(line: str) -> int:
    xmas_count = line.count("XMAS")
    samx_count = line.count("SAMX")
    return xmas_count + samx_count

def vertical_lines(data: List[str]) -> List[str]:
    vlines = []
    for i in range(0, len(data[0])):
        vline = ""
        for j in range(0, len(data)):
            vline = vline + data[j][i]
        vlines.append(vline)
    return vlines

def diagnonal_lines_a(data: List[str]) -> List[str]:
    diags = []
    for i in range(0, len(data[0])):
        diag = ""
        jx = i
        jy = 0
        while jx < len(data[0]) and jy < len(data):
            diag = diag + data[jy][jx]
            jx += 1
            jy += 1
        diags.append(diag)
    for j in range(1, len(data)):
        diag = ""
        ix = 0
        iy = j
        while ix < len(data[0]) and iy < len(data):
            diag = diag + data[iy][ix]
            ix += 1
            iy += 1
        diags.append(diag)
    return diags

def diagonal_lines_b(data: List[str]) -> List[str]:
    diags = []
    for i in range(0, len(data[0])):
        diag = ""
        jx = i
        jy = 0
        while jx >= 0 and jy < len(data):
            diag = diag + data[jy][jx]
            jx -= 1
            jy += 1
        diags.append(diag)
    for j in range(1, len(data)):
        diag = ""
        ix = len(data[0]) - 1
        iy = j
        while ix >= 0 and iy < len(data):
            diag = diag + data[iy][ix]
            ix -= 1
            iy += 1
        diags.append(diag)
    return diags

def do_part2(lines: List[str]) -> int:
    count = 0
    for j in range(1, len(lines)-1):
        for i in range(1, len(lines[0])-1):
            if lines[j][i] != 'A':
                continue
            mas_a = (lines[j-1][i-1] == 'M' and lines[j+1][i+1] == 'S') or (lines[j-1][i-1] == 'S' and lines[j+1][i+1] == 'M')
            mas_b = (lines[j-1][i+1] == 'M' and lines[j+1][i-1] == 'S') or (lines[j-1][i+1] == 'S' and lines[j+1][i-1] == 'M')
            if mas_a and mas_b:
                count += 1
    return count

# filename = "day4/test-input.txt"
filename = "day4/input.txt"
hlines = read_file(filename)
vlines = vertical_lines(hlines)
diags_a = diagnonal_lines_a(hlines)
diags_b = diagonal_lines_b(hlines)
all_lines = hlines + vlines + diags_a + diags_b
part1 = sum([count_xmas(line) for line in all_lines])
print(part1)
part2 = do_part2(hlines)
print(part2)