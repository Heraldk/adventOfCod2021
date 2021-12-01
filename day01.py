from rich.console import Console
from typing import List


def count_increases_for_window(numbers: List[int], window_size: int) -> int:
    increases = 0
    window = []
    prevSum = None
    for number in numbers:
        if len(window) == window_size:
            window.pop(0)
        window.append(number)

        if prevSum and sum(window) > prevSum:
            increases += 1

        if len(window) == window_size:
            prevSum = sum(window)
    return increases


console = Console()
with open("day01.txt", "r") as file:
    console.print("[b yellow]Day 01 - part 1[/b yellow]")
    numbers = [int(x) for x in file.readlines()]
    print(count_increases_for_window(numbers, 1))
    console.print("[b yellow]Day 02 - part 2[/b yellow]")
    print(count_increases_for_window(numbers, 3))
