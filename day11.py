from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, List, Tuple

from rich.console import Console
from rich.live import Live
from rich.table import Table

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


def render_flashed_map(
    map: Dict[Coords, int], just_flashed: List[Coords], iteration: int
) -> Table:
    table = Table(show_header=False)
    table.add_column()

    flashed_set = set(just_flashed)
    x = 0
    y = 0
    done = False
    currRow = ""
    while not done:
        if (val := map.get(Coords(x, y))) is not None:
            if Coords(x, y) in flashed_set:
                currRow += f"[yellow]{val}[/yellow]"
            else:
                currRow += f"[grey50]{val}[/grey50]"
            x += 1
        elif x != 0:
            y += 1
            x = 0
            table.add_row(currRow)
            currRow = ""
        else:
            done = True

    table.add_row(f"Iter: {iteration}")
    return table


def read_input(lines: List[str]) -> Dict[Coords, int]:
    map = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            map[Coords(x, y)] = int(char)
    return map


def run_flash_iteration(map: Dict[Coords, int]) -> Tuple[int, List[Coords]]:
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

    return len(flashed), flashed


with open("day11.txt", "r") as file:
    map = read_input(file.readlines())
    console.print("[b yellow]Day 01[/b yellow]")
    flashes = 0
    latest_flashcount = 0
    iteration = 0

    with Live(render_flashed_map(map, [], iteration), refresh_per_second=10) as live:
        while latest_flashcount < 100:
            latest_flashcount, just_flashed = run_flash_iteration(map)
            live.update(render_flashed_map(map, just_flashed, iteration))
            if iteration < 100:
                flashes += latest_flashcount
            iteration += 1
            time.sleep(0.1)

    console.print(
        f"{flashes} after 100 iterations. It took {iteration} iterations for all to flash"
    )
