from rich.console import Console
from typing import List, Tuple, Optional, Dict


def read_program(lines: List[str]) -> List[List[str]]:
    program = []
    for line in lines:
        program.append(line.strip().split())
    return program


def read_val(registers: Dict[str, int], num_or_register: str) -> int:
    if (num := registers.get(num_or_register)) is not None:
        return num
    return int(num_or_register)


def write_val(registers: Dict[str, int], register: str, num: int):
    registers[register] = num


def validate_solution(
    program: List[List[str]],
    registers: Dict[str, int],
    input: str,
) -> Optional[str]:

    inputs = list(input)
    pc = 0
    while pc < len(program):
        if pc == len(program):
            if read_val(registers, "z") == 0:
                return f"{input}"
            else:
                return None
        instr = program[pc][0]
        if instr == "inp":
            dest = program[pc][1]
            input_val = inputs.pop(0)
            write_val(registers, dest, int(input_val))
        else:
            op1 = program[pc][1]
            op2 = program[pc][2]
            if instr == "add":
                write_val(
                    registers,
                    op1,
                    read_val(registers, op1) + read_val(registers, op2),
                )
            elif instr == "mul":
                write_val(
                    registers,
                    op1,
                    read_val(registers, op1) * read_val(registers, op2),
                )
            elif instr == "div":
                write_val(
                    registers,
                    op1,
                    read_val(registers, op1) // read_val(registers, op2),
                )
            elif instr == "mod":
                write_val(
                    registers,
                    op1,
                    read_val(registers, op1) % read_val(registers, op2),
                )
            elif instr == "eql":
                write_val(
                    registers,
                    op1,
                    1 if read_val(registers, op1) == read_val(registers, op2) else 0,
                )
        pc += 1
    return registers["z"] == 0


console = Console()
with open("day24.txt", "r") as file:
    program = read_program(file.readlines())
    console.print("[b yellow]Day 24[/b yellow]")
    registers = {"x": 0, "y": 0, "w": 0, "z": 0}
    result = validate_solution(program, registers, "99999795919456")
    console.print(result)
    result = validate_solution(program, registers, "45311191516111")
    console.print(result)


# did this by hand to find those solutions, then the program is just a way to verify that it succeeds
# input has to abide by these constraints:
# input[4] = input[3]
# input[5] = input[2] - 2
# input[8] = input[7] + 4
# input[9] = input[6] - 8
# input[11] = input[10] - 5
# input[12] = input[1] - 4
# input[13] = input[0] - 3
