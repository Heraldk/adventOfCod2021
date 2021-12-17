from enum import Enum
from rich.console import Console
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class Coords:
    x: int
    y: int


class Indicator(Enum):
    HIGHER = 1
    THROUGH = 2
    LOWER = 3


def read_target_area(input: str) -> Tuple[Coords, Coords]:
    spaced = input.strip().split()
    x = spaced[2][2:-1].split(".")
    y = spaced[3][2:].split(".")

    start = Coords(int(x[0]), int(y[0]))
    end = Coords(int(x[2]), int(y[2]))
    return start, end


def fire_probe(
    startVelocityX: int, startVelocityY: int, target: Tuple[Coords, Coords]
) -> Tuple[bool, Indicator, Coords]:
    """returns tuple with three values:
    bool is true if it hits the target
    indicator indicates if the shot goes above or below the target
    coords indicates the highest point the shot reaches
    """

    position = Coords(0, 0)
    velX = startVelocityX
    velY = startVelocityY
    highest = Coords(0, 0)
    while position.x < max(target[0].x, target[1].x) and position.y > min(
        target[0].y, target[1].y
    ):
        position.x += velX
        position.y += velY
        if position.y > highest.y:
            highest = Coords(position.x, position.y)
        velX = max(0, velX - 1)
        velY -= 1
        if (
            position.x >= min(target[0].x, target[1].x)
            and position.x <= max(target[0].x, target[1].x)
            and position.y >= min(target[0].y, target[1].y)
            and position.y <= max(target[0].y, target[1].y)
        ):
            return True, Indicator.THROUGH, highest

    return False, Indicator.HIGHER, highest


console = Console()
with open("day17.txt", "r") as file:
    target_area = read_target_area(file.readline())
    console.print("[b yellow]Day 17[/b yellow]")
    print(target_area)

    best: Optional[Coords] = None
    hit_count = 0
    for x in range(10, 500):
        print(x, hit_count)
        for y in range(-800, 2500):
            hit, _, highest = fire_probe(x, y, target_area)
            if hit:
                if not best or highest.y > best.y:
                    best = highest
                    print(best)
                hit_count += 1
    print(hit_count)
