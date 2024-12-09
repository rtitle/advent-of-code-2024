def read_file(filename: str) -> list[str]:
    with open(filename, 'r') as file:
        return file.read().rstrip()

def parse_disk_map(input: str) -> list[int | None]:
    res = []
    empty = False
    file = 0
    for c in input:
        for _ in range(0, int(c)):
            if empty:
                res.append(None)
            else:
                res.append(file)
        empty = not empty
        if not empty:
            file += 1
    return res

def get_checksum(disk_map: list[int | None]) -> int:
    res = 0
    for i in range(0, len(disk_map)):
        if disk_map[i] != None:
            res += i * disk_map[i]
    return res

def defrag_part_1(disk_map: list[int | None]) -> list[int | None]:
    disk_map_copy = disk_map.copy()
    l = 0
    r = len(disk_map_copy) - 1
    while l != r:
        if disk_map_copy[r] == None:
            r -= 1
            continue
        if disk_map_copy[l] == None:
            disk_map_copy[l] = disk_map[r]
            disk_map_copy[r] = None
            r -= 1
        l += 1
    return disk_map_copy

def get_chunks(disk_map: list[int | None]) -> list[tuple[int, int, int]]:
    prev = None
    prev_start_idx = None
    chunks = []
    for i in range(0, len(disk_map)):
        if prev != disk_map[i]:
            if prev_start_idx != None:
                chunks.append((prev_start_idx, i, prev))
            prev_start_idx = i
        prev = disk_map[i]
    chunks.append((prev_start_idx, len(disk_map), prev))
    return chunks

def defrag_part_2(disk_map: list[int | None]) -> list[int | None]:
    disk_map_copy = disk_map.copy()
    chunks = get_chunks(disk_map_copy)
    for start2, end2, id2 in filter(lambda x: x[2] != None, reversed(chunks)):
        for start, end, _ in filter(lambda x: x[2] == None, get_chunks(disk_map_copy)):
            if start > start2:
                break
            if (end2 - start2) <= (end - start):
                disk_map_copy[start:(start+end2-start2)] = [id2] * (end2-start2)
                disk_map_copy[start2:end2] = [None] * (end2-start2)
                break
    return disk_map_copy

filename = "day9/test-input.txt"
filename = "day9/input.txt"
disk_map = parse_disk_map(read_file(filename))
part1 = get_checksum(defrag_part_1(disk_map))
print(part1)
part2 = get_checksum(defrag_part_2(disk_map))
print(part2)