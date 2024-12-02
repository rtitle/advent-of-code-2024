def parse_reports(filename: str) -> list[list[int]]:
    reports = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            levels = []
            sp = line.split()
            for s in sp:
                levels.append(int(s))
            reports.append(levels)
        return reports

def part1(reports: list[list[int]]) -> int:
    count = 0
    for report in reports:
        safe = True
        prev = None
        increasing = None
        has_skip = True
        for cur in report:
            if not prev:
                prev = cur
                continue
            diff = cur - prev
            # prev = cur
            if increasing == None:
                increasing = diff > 0
            if increasing and diff >= 1 and diff <= 3:
                prev = cur
                continue
            if not increasing and diff <= -1 and diff >= -3:
                prev = cur
                continue
            if has_skip:
                has_skip = False
                continue
            safe = False
            break
        if safe:
            count += 1
    return count


filename = 'test-input.txt'
filename = 'input.txt'
reports = parse_reports(filename)
print(part1(reports))
