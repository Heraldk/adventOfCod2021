from __future__ import annotations
from rich.console import Console
from dataclasses import dataclass
from typing import List, Dict, Tuple

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
        ]


def read_input(lines: List[str]) -> Dict[Coords, int]:
    map = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            map[Coords(x, y)] = int(char)
    return map


def find_lowpoints(map: Dict[Coords, int]) -> Tuple(List[Coords], List[int]):
    low_heights = []
    low_coords = []
    for coords, height in map.items():
        is_lowest = True
        for neighbour in coords.get_neighbours():
            if (neighbour_height := map.get(neighbour)) is not None:
                if neighbour_height <= height:
                    is_lowest = False
        if is_lowest:
            low_heights.append(height)
            low_coords.append(coords)
    return low_coords, low_heights


def find_basins(
    low_coords: List[Coords], map: Dict[Coords, int]
) -> Tuple[List(int), Dict[Coords, int]]:
    mapped_basins = {}
    for basin_num, coord in enumerate(low_coords):
        mapped_basins[coord] = basin_num
        basin_num += 1

    basin_sizes = [1 for _ in range(0, basin_num)]

    explore_list = list(low_coords)
    while len(explore_list) > 0:
        coords = explore_list.pop(0)
        basin = mapped_basins[coords]
        for neighbour in coords.get_neighbours():
            if (neighbour_height := map.get(neighbour)) is not None:
                if neighbour_height < 9:
                    if neighbour not in mapped_basins:
                        mapped_basins[neighbour] = basin
                        basin_sizes[basin] += 1
                        explore_list.append(neighbour)

    return sorted(basin_sizes), mapped_basins


# randomly generated mostly blue and green hues but some random other things for a bit of flavour
blues = [
    "#a8b6ff",
    "#36679b",
    "#391cc9",
    "#4f63e2",
    "#4686f4",
    "#4434bc",
    "#494cf4",
    "#8ed2ff",
    "#0d6de2",
    "#0a6b70",
    "#63cccc",
    "#2eaccc",
    "#c4d2ff",
    "#5fcfe2",
    "#27077a",
    "#035996",
    "#0b7ce0",
    "#5e29e5",
    "#189cba",
    "#08e00c",
    "#86f4bb",
    "#cee283",
    "#02701b",
    "#82f961",
    "#d4ea72",
    "#adffc4",
    "#75f479",
    "#53ed55",
    "#7d91f2",
    "#254a82",
    "#011ebf",
    "#0d6282",
    "#e3c5f9",
    "#f9bbea",
    "#dbf274",
    "#f4d122",
    "#bf630d",
    "#e855b4",
]


def visualise_basins(map: Dict[Coords, int], mapped_basins: Dict[Coords, int]):
    x = 0
    y = 0
    done = False
    while not done:
        if (val := mapped_basins.get(Coords(x, y))) is not None:
            console.print(f"~", end="", style=blues[val % len(blues)])
            x += 1
        elif (val := map.get(Coords(x, y))) is not None:
            console.print(f"^", end="")
            x += 1
        elif x != 0:
            y += 1
            x = 0
            console.print()
        else:
            done = True
            console.print()


with open("day09.txt", "r") as file:
    map = read_input(file.readlines())
    console.print("[b yellow]Day 09[/b yellow]")
    low_coords, low_points = find_lowpoints(map)
    basin_sizes, mapped_basins = find_basins(low_coords, map)

    visualise_basins(map, mapped_basins)
    console.print(
        f"found {len(low_points)} low points. Total height: {sum(low_points)} for total risk of {sum(low_points) + len(low_points)}"
    )
    console.print(
        f" Largest 3 basins: {basin_sizes[-1]}, {basin_sizes[-2]}, {basin_sizes[-3]} for score of {basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]}"
    )
