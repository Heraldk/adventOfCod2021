from __future__ import annotations
from dataclasses import dataclass
from rich.console import Console
from typing import List, Tuple, Dict


@dataclass(order=True, frozen=True)
class Coords:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"<{self.x},{self.y}>"

    def get_neighbours_in_order(self) -> List[Coords]:
        return [
            Coords(self.x - 1, self.y - 1),
            Coords(self.x, self.y - 1),
            Coords(self.x + 1, self.y - 1),
            Coords(self.x - 1, self.y),
            Coords(self.x, self.y),
            Coords(self.x + 1, self.y),
            Coords(self.x - 1, self.y + 1),
            Coords(self.x, self.y + 1),
            Coords(self.x + 1, self.y + 1),
        ]


def read_input(lines: List[str]) -> Tuple[str, Dict[Coords, int], Coords, Coords]:
    mapping = lines.pop(0)
    lines.pop(0)

    image = {}
    maxX = 0
    for yIndex, line in enumerate(lines):
        for xIndex, item in enumerate(line):
            if item == "#":
                image[Coords(xIndex, yIndex)] = 1
                maxX = max(maxX, xIndex)

    return mapping, image, Coords(0, 0), Coords(maxX, yIndex)


def output_coords(coords: Dict[Coords, int], min_val: Coords, max_val: Coords):
    for y in range(min_val.y, max_val.y + 1):
        for x in range(min_val.x, max_val.x + 1):
            char = "#" if Coords(x, y) in coords else "."
            console.print(f"{char}", end="")
        console.print()
    console.print()


def isPixelLit(
    pixel: Coords,
    mapping: str,
    image: Dict[Coords, int],
    minCoord: Coords,
    maxCoord: Coords,
    iteration: int,
) -> bool:
    num = 0
    for neighbour in pixel.get_neighbours_in_order():
        num <<= 1
        if image.get(neighbour) is not None:
            num |= 1
        elif mapping[0] == "#":
            if iteration % 2 == 0 and (
                neighbour.x < minCoord.x
                or neighbour.y < minCoord.y
                or neighbour.x > maxCoord.x
                or neighbour.y > maxCoord.y
            ):
                num |= 1
    return mapping[num] == "#"


def enhance(
    mapping: str,
    image: Dict[Coords, int],
    origin_min: Coords,
    origin_max: Coords,
    iteration: int,
) -> Tuple[Dict[Coords, int], Coords, Coords]:

    new_image = {}
    minX = 1
    maxX = 0
    minY = 1
    maxY = 0

    for y in range(origin_min.y - 1, origin_max.y + 2):
        for x in range(origin_min.x - 1, origin_max.x + 2):
            loc = Coords(x, y)
            if isPixelLit(loc, mapping, image, origin_min, origin_max, iteration):
                new_image[loc] = 1
                minX = min(minX, x)
                minY = min(minY, y)
                maxX = max(maxX, x)
                maxY = max(maxY, y)

    return new_image, Coords(minX, minY), Coords(maxX, maxY)


console = Console()
with open("day20.txt", "r") as file:
    mapping, image, minCoords, maxCoords = read_input(file.readlines())
    console.print("[b yellow]Day 20[/b yellow]")

    for iteration in range(1, 51):
        image, minCoords, maxCoords = enhance(
            mapping, image, minCoords, maxCoords, iteration
        )
        if iteration == 2:
            console.print(len(image))
    console.print(len(image))
