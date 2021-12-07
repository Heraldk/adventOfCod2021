import functools
from rich.console import Console
from typing import Callable, List


def calc_cost_linear(numbers: List[int], offset: int) -> int:
    cost = 0
    for number in numbers:
        cost += abs(number - offset)
    return cost


def calc_cost_nonlinear(numbers: List[int], offset: int) -> int:
    cost = 0
    for number in numbers:
        distance = abs(number - offset)
        # arithemtic sequence formula: number of terms (distance) multiplied by first term and the last term added together. Then divide by 2.
        cost += distance * (distance + 1) // 2
    return cost


def minimize_fuel(numbers: List[int], cost_func: Callable[[int], int]) -> int:
    min_index = None
    for x in range(min(numbers), max(numbers)):
        cost = cost_func(numbers, x)
        if not min_index or cost < min_cost:
            min_index = x
            min_cost = cost
    return min_cost


console = Console()
with open("day07.txt", "r") as file:
    numbers = [int(x) for x in file.readline().strip().split(",")]
    console.print("[b yellow]Day 07 - part 1[/b yellow]")
    console.print(minimize_fuel(numbers, calc_cost_linear))
    console.print("[b yellow]Day 07 - part 2[/b yellow]")
    console.print(minimize_fuel(numbers, calc_cost_nonlinear))
