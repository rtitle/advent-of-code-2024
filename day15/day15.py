from typing import Optional

def parse_input(filename: str) -> tuple[list[str], str]:
    with open(filename, 'r') as file:
        data = file.read()
    [map_data, move_data] = data.split("\n\n")
    return map_data.split("\n"), move_data.replace("\n", "")

def get_move(coord: tuple[int], move: str) -> tuple[int]:
    x, y = coord
    if move == "<":
        return x-1, y
    if move == ">":
        return x+1, y
    if move == "^":
        return x, y-1
    if move == "v":
        return x, y+1
    
def in_bounds(map: list[str], coord: tuple[int]) -> bool:
    xlen = len(map[0])
    ylen = len(map)
    x, y = coord
    return x >= 0 and x < xlen and y >= 0 and y < ylen

def get_robot_pos(map: list[str]) -> tuple[int]:
    robot_pos = None
    for y, row in enumerate(map):
        for x, s in enumerate(row):
            if s == '@':
                robot_pos = x, y
                break
    return robot_pos


def make_move(map: list[str], robot: tuple[int], move: str) -> Optional[tuple[int]]:
    initial_move = get_move(robot, move)
    if not in_bounds(map, initial_move):
        return None
    
    move_possible = True
    new_coord = initial_move
    while in_bounds(map, new_coord):
        nx, ny = new_coord
        if map[ny][nx] == '.':
            break
        if map[ny][nx] == '#':
            move_possible = False
            break

        new_coord = get_move(new_coord, move)

    if move_possible:
        x, y = initial_move
        rx, ry = robot
        map[y] = map[y][:x] + "@" + map[y][x+1:]
        map[ry] = map[ry][:rx] + "." + map[ry][rx+1:]
        if new_coord != initial_move:
            x, y = new_coord
            map[y] = map[y][:x] + "O" + map[y][x+1:]
        return initial_move
    
    return None

def do_part_1(map: list[str], moves: str) -> int:
    map2 = map.copy()
    robot_pos = get_robot_pos(map2)
    for move in moves:
        new_pos = make_move(map2, robot_pos, move)
        if new_pos != None:
            robot_pos = new_pos
        
    res = 0
    for y, row in enumerate(map2):
        for x, s in enumerate(row):
            if s == 'O':
                res += x + 100 * y

    return res

def scale_up_map(map: list[str]) -> list[str]:
    new_map = []
    for row in map:
        new_row = ""
        for s in row:
            if s == '#':
                new_row += "##"
            elif s == '.':
                new_row += ".."
            elif s == 'O':
                new_row += "[]"
            elif s == '@':
                new_row += "@."
        new_map.append(new_row)
    return new_map

def make_block_move(map: list[str], block: tuple[int], move: str) -> bool:
    x, y = block
    xi, yi = get_move(block, move)
    if not in_bounds(map, (xi, yi) or not in_bounds(map, (xi+1, yi))):
        return False
    
    if move == ">":
        if map[y][x+2] == '#':
            return False
        
        if map[y][x+2] == '.':
            map[y] = map[y][:x] + ".[]" + map[y][x+3:]
            return True
        
        if map[y][x+2] == "[":
            if make_block_move(map, (x+2, y), move):
                map[y] = map[y][:x] + ".[]" + map[y][x+3:]
                return True
            else:
                return False
        
    if move == "<":
        if map[y][x-1] == '#':
            return False
        
        if map[y][x-1] == '.':
            map[y] = map[y][:x-1] + "[]." + map[y][x+2:]
            return True
        
        if map[y][x-1] == "]":
            if make_block_move(map, (x-2, y), move):
                map[y] = map[y][:x-1] + "[]." + map[y][x+2:]
                return True
            else:
                return False
        
    if move == "^" or move == "v":
        if map[yi][xi] == '#' or map[yi][xi+1] == '#':
            return False
        
        if map[yi][xi] == '.' and map[yi][xi+1] == '.':
            x, y = block
            map[y] = map[y][:x] + ".." + map[y][x+2:]
            map[yi] = map[yi][:xi] + "[]" + map[yi][xi+2:]
            return True
        
        if map[yi][xi] == '[' and map[yi][xi+1] == ']':
            if make_block_move(map, (xi, yi), move):
                map[y] = map[y][:x] + ".." + map[y][x+2:]
                map[yi] = map[yi][:xi] + "[]" + map[yi][xi+2:]
                return True
            else:
                return False
        
        if map[yi][xi] == "]" and map[yi][xi+1] == ".":
            if make_block_move(map, (xi-1, yi), move):
                map[y] = map[y][:x] + ".." + map[y][x+2:]
                map[yi] = map[yi][:xi] + "[]" + map[yi][xi+2:]
                return True
            else: 
                return False

        if map[yi][xi] == "." and map[yi][xi+1] == "[":
            if make_block_move(map, (xi+1, yi), move):
                map[y] = map[y][:x] + ".." + map[y][x+2:]
                map[yi] = map[yi][:xi] + "[]" + map[yi][xi+2:]
                return True
            else:
                return False

        if map[yi][xi] == "]" and map[yi][xi+1] == "[":
            map2 = map.copy()
            if make_block_move(map2, (xi-1, yi), move) and make_block_move(map2, (xi+1, yi), move):
                for i in range(0, len(map2)):
                    map[i] = map2[i]
                map[y] = map[y][:x] + ".." + map[y][x+2:]
                map[yi] = map[yi][:xi] + "[]" + map[yi][xi+2:]
                return True
            else:
                return False

    return False

def make_move_part2(map: list[str], robot: tuple[int], move: str) -> Optional[tuple[int]]:
    initial_move = get_move(robot, move)
    x, y = robot
    xi, yi = initial_move
    if not in_bounds(map, initial_move):
        return None
    
    if map[yi][xi] == '#':
        return None
    
    if map[yi][xi] == '.':
        map[y] = map[y][:x] + "." + map[y][x+1:]
        map[yi] = map[yi][:xi] + "@" + map[yi][xi+1:]
        return xi, yi

    if map[yi][xi] == '[':
        if make_block_move(map, (xi, yi), move):
            map[y] = map[y][:x] + "." + map[y][x+1:]
            map[yi] = map[yi][:xi] + "@" + map[yi][xi+1:]
            return xi, yi
        else: 
            return None

    if map[yi][xi] == "]":
        if make_block_move(map, (xi-1, yi), move):
            map[y] = map[y][:x] + "." + map[y][x+1:]
            map[yi] = map[yi][:xi] + "@" + map[yi][xi+1:]
            return xi, yi
        else:
            return None

    return None
    
def do_part_2(map: list[str], moves: str) -> int:
    map2 = map.copy()
    robot_pos = get_robot_pos(map2)
    for move in moves:
        new_pos = make_move_part2(map2, robot_pos, move)
        if new_pos != None:
            robot_pos = new_pos
 
    res = 0
    for y, row in enumerate(map2):
        for x, s in enumerate(row):
            if s == '[':
                res += x + 100 * y

    return res

# filename = "day15/test-input.txt"
filename = "day15/input.txt"
map, moves = parse_input(filename)
part1 = do_part_1(map, moves)
print(part1)
new_map = scale_up_map(map)
part2 = do_part_2(new_map, moves)
print(part2)