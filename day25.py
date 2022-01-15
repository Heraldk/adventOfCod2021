from __future__ import annotations
from rich.console import Console
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass


@dataclass(order=True, frozen=True)
class Coords:
    x: int
    y: int

    def get_neighbours(self) -> List[Coords]:
        return [
            Coords(self.x - 1, self.y),
            Coords(self.x, self.y - 1),
            Coords(self.x + 1, self.y),
            Coords(self.x, self.y + 1),
        ]


def read_map(lines: List[str]) -> Tuple[Dict[Coords, str], Dict[Coords, str], int, int]:
    east_map = {}
    south_map = {}
    maxY = len(lines)
    for y, line in enumerate(lines):
        maxX = len(line.strip())
        for x, char in enumerate(line.strip()):
            if char == ">":
                east_map[Coords(x, y)] = char
            elif char == "v":
                south_map[Coords(x, y)] = char
    return east_map, south_map, maxX, maxY


def print_map(map: Tuple[Dict[Coords, str], Dict[Coords, str], int, int]):
    east_map, south_map, maxX, maxY = map
    for y in range(0, maxY):
        for x in range(0, maxX):
            coords = Coords(x, y)
            if coords in east_map:
                print(">", end="")
            elif coords in south_map:
                print("v", end="")
            else:
                print(".", end="")
        print("")
    print("")


def simulate_steps(map: Tuple[Dict[Coords, str], Dict[Coords, str], int, int]) -> int:
    num_moved = 1
    east_map, south_map, maxX, maxY = map
    num_steps = 0

    while num_moved > 0:
        # print(num_steps)
        # print_map((east_map, south_map, maxX, maxY))
        num_moved = 0
        new_east_map, new_south_map = {}, {}
        for coord in east_map:
            check_coord = Coords((coord.x + 1) % maxX, coord.y)
            if check_coord not in east_map and check_coord not in south_map:
                new_east_map[check_coord] = ">"
                num_moved += 1
            else:
                new_east_map[coord] = ">"

        for coord in south_map:
            check_coord = Coords(coord.x, (coord.y + 1) % maxY)
            if check_coord not in south_map and check_coord not in new_east_map:
                new_south_map[check_coord] = "v"
                num_moved += 1
            else:
                new_south_map[coord] = "v"

        east_map = new_east_map
        south_map = new_south_map
        num_steps += 1

    return num_steps


console = Console()
with open("day25.txt", "r") as file:
    map = read_map(file.readlines())
    console.print("[b yellow]Day 24[/b yellow]")
    num_steps = simulate_steps(map)
    console.print(num_steps)
