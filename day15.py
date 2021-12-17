from __future__ import annotations
from rich.console import Console
from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass(frozen=True, order=True)
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


class Map:
    def __init__(self, lines: List[str]):
        self.map = {}
        self.maxX = 0
        self.maxY = 0
        for yCoord, line in enumerate(lines):
            for index, char in enumerate(line.strip()):
                self.map[Coords(index, yCoord)] = int(char)
                self.maxX = max(self.maxX, index)
            self.maxY = max(self.maxY, yCoord)

    def expand(self, dimension=5):
        newmap = {}
        newMaxX, newMaxY = 0, 0
        for yDim in range(dimension):
            for xDim in range(dimension):
                for y in range(self.maxY + 1):
                    for x in range(self.maxX + 1):
                        val = self.map[Coords(x, y)]
                        val = (val + yDim + xDim - 1) % 9 + 1
                        xCoord = xDim * (self.maxX + 1) + x
                        yCoord = yDim * (self.maxY + 1) + y
                        newmap[Coords(xCoord, yCoord)] = val
                        newMaxX = max(newMaxX, xCoord)
                        newMaxY = max(newMaxY, yCoord)
        self.map = newmap
        self.maxX = newMaxX
        self.maxY = newMaxY

    def print(self):
        for y in range(self.maxY + 1):
            for x in range(self.maxX + 1):
                print(self.map[Coords(x, y)], end="")
            print()


def find_shortest_path(start: Coords, end: Coords, map: Map) -> Optional[int]:
    explored = {}
    explore_set: Dict[Coords, int] = {start: 0}
    while len(explore_set) > 0:
        current_loc = min(
            explore_set,
            key=lambda k: abs(end.x - k.x) + abs(end.y - k.y) + explore_set[k],
        )
        print(explore_set)
        print(current_loc)
        risk = explore_set[current_loc]
        del explore_set[current_loc]
        if current_loc == end:
            print(len(explored))
            return risk
        explored[current_loc] = risk
        for neighbour in current_loc.get_neighbours():
            if (
                neighbour not in explored
                and (neighbour_risk := map.map.get(neighbour)) is not None
            ):
                if neighbour not in explore_set:
                    explore_set[neighbour] = risk + neighbour_risk
                else:
                    explore_set[neighbour] = min(
                        explore_set[neighbour], risk + neighbour_risk
                    )

    return None


console = Console()
with open("day15.txt", "r") as file:
    map = Map(file.readlines())
    console.print("[b yellow]Day 15[/b yellow]")
    console.print(find_shortest_path(Coords(0, 0), Coords(map.maxX, map.maxY), map))
    map.expand(5)
    console.print(find_shortest_path(Coords(0, 0), Coords(map.maxX, map.maxY), map))
