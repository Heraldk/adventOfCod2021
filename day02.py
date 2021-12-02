from re import split
from typing import List, Tuple
from rich.console import Console


def convert_input(lines: List[str]) -> List[Tuple[str, int]]:
    result = []
    for line in lines:
        vals = line.strip().split()
        result.append((vals[0], int(vals[1])))
    return result


def calculate_position(course: List[Tuple[str, int]]) -> Tuple[int, int]:
    depth = 0
    horizontal_pos = 0
    for direction, distance in course:
        if direction == "forward":
            horizontal_pos += distance
        elif direction == "down":
            depth += distance
        elif direction == "up":
            depth -= distance
    return horizontal_pos, depth


def calculate_position_with_aim(course: List[Tuple[str, int]]) -> Tuple[int, int]:
    depth = 0
    horizontal_pos = 0
    aim = 0
    for direction, amount in course:
        if direction == "forward":
            horizontal_pos += amount
            depth += aim * amount
        elif direction == "down":
            aim += amount
        elif direction == "up":
            aim -= amount
    return horizontal_pos, depth


console = Console()

with open("day02.txt", "r") as file:
    console.print("[b yellow]Day 02 - part 1[/b yellow]")
    course = convert_input(file.readlines())
    result = calculate_position(course)
    console.print(f"{result[0]}, {result[1]}: {result[0]*result[1]}")

    console.print("[b yellow]Day 02 - part 2[/b yellow]")
    result = calculate_position_with_aim(course)
    console.print(f"{result[0]}, {result[1]}: {result[0]*result[1]}")
