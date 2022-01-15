from __future__ import annotations
from rich.console import Console
from dataclasses import dataclass
from typing import List, Dict
from copy import deepcopy

console = Console()


@dataclass(order=True, frozen=True)
class Coords:
    x: int
    y: int
    z: int

    def __repr__(self) -> str:
        return f"<{self.x},{self.y}>"


def init_procedure(instructions) -> int:
    map: Dict[Coords, int] = {}
    for instruct in instructions:
        is_turn_on, xRange, yRange, zRange = instruct
        if (
            xRange[0] < -50
            or xRange[1] > 50
            or yRange[0] < -50
            or yRange[1] > 50
            or zRange[0] < -50
            or zRange[1] > 50
        ):
            continue
        for x in range(xRange[0], xRange[1] + 1):
            for y in range(yRange[0], yRange[1] + 1):
                for z in range(zRange[0], zRange[1] + 1):
                    if is_turn_on:
                        map[Coords(x, y, z)] = 1
                    else:
                        map.pop(Coords(x, y, z), None)

        # for x in range(xRange[0], xRange[1] + 1):
        # for y in range(yRange[0], yRange[1] + 1):
        #     for z in range(zRange[0], zRange[1] + 1):
        #         if is_turn_on:
        #             map[Coords(0, y, z)] = 1
        #         else:
        #             map.pop(Coords(0, y, z), None)
        # print(len(map))
    return len(map)


def read_ranges(input: str):
    commaSplit = input.split(",")
    xRange = commaSplit[0].removeprefix("x=").split("..")
    yRange = commaSplit[1].removeprefix("y=").split("..")
    zRange = commaSplit[2].removeprefix("z=").split("..")
    return (
        (int(xRange[0]), int(xRange[1])),
        (int(yRange[0]), int(yRange[1])),
        (int(zRange[0]), int(zRange[1])),
    )


def read_input(lines: List[str]):
    results = []
    for line in lines:
        spaceSplit = line.strip().split()
        is_on = spaceSplit[0] == "on"
        ranges = read_ranges(spaceSplit[1])
        results.append((is_on, *ranges))
    return results


class Range:
    def __init__(self, start: int, end: int, split: SplitMap):
        self.start = start
        self.end = end
        self.split = split

    def count_lit(self) -> int:
        count = self.end - self.start + 1
        if self.split is not None:
            count *= self.split.count_lit()
        return count

    def __repr__(self):
        map_str = "" if self.split is None else f":{self.split.map}"
        return f"<{self.start},{self.end}>{map_str}"


class SplitMap:
    def __init__(self):
        self.map: List[Range] = []

    def count_lit(self) -> int:
        return sum([a.count_lit() for a in self.map])

    def split_range(self, turn_on: bool, cuts):
        # console.print(self.map)
        # console.print(cuts)
        (cutMin, cutMax) = cuts.pop(0)

        newmap = []
        while len(self.map) > 0:
            interval = self.map[0]
            if cutMin is None:
                newmap.append(interval)
                self.map.pop(0)
            elif interval.end < cutMin:
                newmap.append(interval)
                self.map.pop(0)
            elif interval.start > cutMax:
                if turn_on:
                    newRange = Range(
                        cutMin, cutMax, None if len(cuts) == 0 else SplitMap()
                    )
                    if len(cuts) > 0:
                        newRange.split.split_range(turn_on, list(cuts))
                    newmap.append(newRange)
                cutMin = None
            else:
                if cutMin < interval.start:
                    if turn_on:
                        newRange = Range(
                            cutMin,
                            interval.start - 1,
                            None if len(cuts) == 0 else SplitMap(),
                        )
                        if len(cuts) > 0:
                            newRange.split.split_range(turn_on, list(cuts))
                        newmap.append(newRange)
                    cutMin = interval.start
                elif cutMin > interval.start:
                    newRange = Range(
                        interval.start, cutMin - 1, deepcopy(interval.split)
                    )
                    newmap.append(newRange)
                    interval.start = cutMin
                assert interval.start == cutMin
                if cutMax < interval.end:
                    newRange = Range(interval.start, cutMax, deepcopy(interval.split))
                    if len(cuts) > 0:
                        newRange.split.split_range(turn_on, list(cuts))
                        newmap.append(newRange)
                    elif turn_on:
                        newmap.append(newRange)
                    interval.start = cutMax + 1
                    newmap.append(interval)
                    self.map.pop(0)
                    cutMin = None
                else:
                    if cutMax > interval.end:
                        cutMin = interval.end + 1
                    else:
                        cutMin = None
                    if len(cuts) > 0:
                        interval.split.split_range(turn_on, list(cuts))
                        newmap.append(interval)
                    elif turn_on:
                        newmap.append(interval)
                    self.map.pop(0)

        if cutMin is not None and turn_on:
            newRange = Range(cutMin, cutMax, None if len(cuts) == 0 else SplitMap())
            if len(cuts) > 0:
                newRange.split.split_range(turn_on, list(cuts))
            newmap.append(newRange)

        self.map = newmap
        # console.print(self.map)


def range_splitter(instructions) -> int:
    map = SplitMap()
    for instruct in instructions:
        is_turn_on, xRange, yRange, zRange = instruct
        map.split_range(is_turn_on, [xRange, yRange, zRange])
        # console.print(map.map)
        # console.print(map.count_lit())
    console.print(map.count_lit())


with open("day22.txt", "r") as file:
    input = read_input(file.readlines())
    console.print("[b yellow]Day 22[/b yellow]")
    console.print(init_procedure(input))

    # map = SplitMap()
    # map.split_range(True, [(6, 10)])
    # console.print(map.map)
    # map.split_range(True, [(11, 20)])
    # console.print(map.map)
    # map.split_range(False, [(8, 17)])
    # console.print(map.map)

    range_splitter(input)
