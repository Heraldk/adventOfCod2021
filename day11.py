from __future__ import annotations
from typing import List, Dict
from dataclasses import dataclass
from rich.console import Console

console = Console()


@dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def get_neighbours(self) -> List[Coords]:
        return [
            Coords(self.x - 1, self.y),
            Coords(self.x, self.y - 1),
            Coords(self.x + 1, self.y),
            Coords(self.x, self.y + 1),
            Coords(self.x - 1, self.y - 1),
            Coords(self.x - 1, self.y + 1),
            Coords(self.x + 1, self.y + 1),
            Coords(self.x + 1, self.y - 1),
        ]


def print_map(map: Dict[Coords, int]):
    x = 0
    y = 0
    done = False
    while not done:
        if (val := map.get(Coords(x, y))) is not None:
            console.print(f"{val}", end="")
            x += 1
        elif x != 0:
            y += 1
            x = 0
            console.print()
        else:
            done = True
            console.print()


def read_input(lines: List[str]) -> Dict[Coords, int]:
    map = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            map[Coords(x, y)] = int(char)
    return map


def run_flash_iteration(map: Dict[Coords, int]) -> int:
    flashed: List[Coords] = []
    increase_energy: List[Coords] = map.keys()
    while len(increase_energy) > 0:
        next_increase_energy: List[Coords] = []
        for coords in increase_energy:
            map[coords] += 1
            if map[coords] == 10:
                flashed.append(coords)
                for neighbour in coords.get_neighbours():
                    if neighbour in map:
                        next_increase_energy.append(neighbour)
        increase_energy = next_increase_energy

    for flashed_coords in flashed:
        map[flashed_coords] = 0

    return len(flashed)


with open("day11.txt", "r") as file:
    map = read_input(file.readlines())
    console.print("[b yellow]Day 01[/b yellow]")
    flashes = 0
    latest_flashcount = 0
    iteration = 0
    while latest_flashcount < 100:
        latest_flashcount = run_flash_iteration(map)
        if iteration < 100:
            flashes += latest_flashcount
        iteration += 1
        
    console.print(f"{flashes} after 100 iterations. It took {iteration} iterations for all to flash")
