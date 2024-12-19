from typing import Optional

def parse_input(filename: str) -> tuple[dict[str, int], list[int]]:
    with open(filename, 'r') as file:
        lines = file.read()
    [registers, program] = lines.split("\n\n")

    regs_dict = {}
    for register in registers.split("\n"):
        [k, v] = register.replace("Register", "").replace(" ", "").split(":")
        regs_dict[k] = int(v)

    prog = [int(x) for x in program.replace("Program: ", "").split(",")]

    return regs_dict, prog

def get_combo_operand(operand: int, registers: dict[str, int]) -> int:
    if 0 <= operand <= 3:
        return operand
    if operand == 4:
        return registers["A"]
    if operand == 5:
        return registers["B"]
    if operand == 6:
        return registers["C"]
    return 0
    
def apply_instruction(opcode: int, operand: int, registers: dict[str, int], pointer) -> tuple[Optional[int], int]:
    match opcode:
        case 0:
            numerator = registers["A"]
            denominator = pow(2, get_combo_operand(operand, registers))
            result = numerator // denominator
            registers["A"] = result
            return None, pointer + 2
        case 1:
            reg_b = registers["B"]
            result = reg_b ^ operand
            registers["B"] = result
            return None, pointer + 2
        case 2:
            op_value = get_combo_operand(operand, registers)
            result = op_value % 8
            registers["B"] = result
            return None, pointer + 2
        case 3:
            a_reg = registers["A"]
            if a_reg == 0:
                return None, pointer + 2
            return None, operand
        case 4:
            b_reg = registers["B"]
            c_reg = registers["C"]
            result = b_reg ^ c_reg
            registers["B"] = result
            return None, pointer + 2
        case 5:
            op_value = get_combo_operand(operand, registers)
            result = op_value % 8
            return result, pointer + 2
        case 6:
            numerator = registers["A"]
            denominator = pow(2, get_combo_operand(operand, registers))
            result = numerator // denominator
            registers["B"] = result
            return None, pointer + 2
        case 7:
            numerator = registers["A"]
            denominator = pow(2, get_combo_operand(operand, registers))
            result = numerator // denominator
            registers["C"] = result
            return None, pointer + 2

def do_part_1(program: list[int], registers: dict[str, int]) -> Optional[str]:
    pointer = 0
    output = []
    short_circuited = False
    while pointer < len(program):
        out, pointer = apply_instruction(program[pointer], program[pointer+1], registers, pointer)
        if out is not None:
            output.append(out)
    return ",".join(map(str, output)) if not short_circuited else None

def do_part_2(program: list[int]) -> int:
    res = []
    do_part_2_rec(program, len(program)-1, 0, res)
    return min(res)

def do_part_2_rec(program: list[int], index: int, n: int, results: list[int]) -> None:
    program_trunc = ",".join(map(str, program[index:]))
    for i in range(n, n+8):
        registers = {"A": i, "B": 0, "C": 0}
        res = do_part_1(program, registers)
        if res == program_trunc:
            if index == 0:
                results.append(i)
            else:
                do_part_2_rec(program, index-1, i*8, results)

filename = "day17/input.txt"
registers, program = parse_input(filename)
part1 = do_part_1(program, registers)
print(part1)
part2 = do_part_2(program)
print(part2)