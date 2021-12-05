from __future__ import annotations
from rich.console import Console
from dataclasses import dataclass
from typing import Tuple, List


@dataclass(frozen=True)
class Coords:
    x: int
    y: int

    @classmethod
    def from_string(cls, input: str) -> Coords:
        vals = input.split(",")
        return Coords(x=int(vals[0]), y=int(vals[1]))

    def __add__(self, o: Coords) -> Coords:
        return Coords(self.x + o.x, self.y + o.y)


def read_input(lines: list[str]) -> List[Tuple[Coords, Coords]]:
    result = []
    for line in lines:
        vals = line.strip().split()
        result.append((Coords.from_string(vals[0]), Coords.from_string(vals[2])))

    return result


def find_intersections(
    lines: list[Tuple[Coords, Coords]], include_diagonals: bool
) -> int:
    map = {}
    for start, end in lines:
        if start.x == end.x:
            step = Coords(0, 1) if start.y < end.y else Coords(0, -1)
        elif start.y == end.y:
            step = Coords(1, 0) if start.x < end.x else Coords(-1, 0)
        elif include_diagonals:
            step = Coords(1 if start.x < end.x else -1, 1 if start.y < end.y else -1)
        else:
            continue

        current = start
        map[current] = map.get(current, 0) + 1
        while current != end:
            current += step
            map[current] = map.get(current, 0) + 1

    intersects = {key: value for (key, value) in map.items() if value > 1}
    return len(intersects)


console = Console()
with open("day05.txt", "r") as file:
    lines = read_input(file.readlines())
    console.print("[b yellow]Day 01 - part 1[/b yellow]")
    print(find_intersections(lines, include_diagonals=False))
    console.print("[b yellow]Day 01 - part 2[/b yellow]")
    print(find_intersections(lines, include_diagonals=True))
