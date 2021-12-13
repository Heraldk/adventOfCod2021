from rich.console import Console
from typing import List, Tuple, Set
from dataclasses import dataclass

console = Console()


@dataclass(frozen=True)
class Coords:
    x: int
    y: int


def read_input(lines: List[str]) -> Tuple[Set[Coords], List[Tuple[str, int]]]:
    coords: Set[Coords] = set()
    folds: List[Tuple[str, int]] = []
    for line in lines:
        line = line.strip()
        if line.startswith("fold"):
            vals = line.split()
            vals = vals[-1].split("=")
            folds.append((vals[-2], int(vals[-1])))
        elif line != "":
            vals = line.split(",")
            coords.add(Coords(x=int(vals[0]), y=int(vals[1])))
    return coords, folds


def output_coords(coords: Set[Coords]):
    maxX = max([coord.x for coord in coords]) + 1
    maxY = max([coord.y for coord in coords]) + 1
    for y in range(0, maxY):
        for x in range(0, maxX):
            char = "#" if Coords(x, y) in coords else "."
            console.print(f"{char}", end="")
        console.print()
    console.print()


def perform_fold(coords: Set[Coords], fold: Tuple[str, int]) -> Set[Coords]:
    new_coords: Set[Coords] = set()
    dimension, value = fold
    for coord in coords:
        if dimension == "x":
            if coord.x < value:
                new_coords.add(coord)
            else:
                new_coords.add(Coords(value - (coord.x - value), coord.y))
        else:
            if coord.y < value:
                new_coords.add(coord)
            else:
                new_coords.add(Coords(coord.x, value - (coord.y - value)))
    return new_coords


with open("day13.txt", "r") as file:
    coords, folds = read_input(file.readlines())
    console.print("[b yellow]Day 13[/b yellow]")

    for fold in folds:
        coords = perform_fold(coords, fold)
        console.print(len(coords))

    output_coords(coords)
