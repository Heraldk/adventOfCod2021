from rich.console import Console
from typing import List
from dataclasses import dataclass


@dataclass
class Timer:
    timer: int
    num: int


# strategy: since the newly added fish all have timers that start at the same time we can use a very basic compression algorithm
# to count how many fish are added on each iteration. That saves a ton of list space so when the number of iterations goes higher
# we don't have an exponential explosion of list size: we only grow the list size by one on each pass.
def iterate_days(timers: List[int], num_days: int):
    timers = [Timer(timer=x, num=1) for x in timers]
    for _ in range(0, num_days):
        new_num_counter = 0
        for index, _ in enumerate(timers):
            timers[index].timer -= 1
            if timers[index].timer < 0:
                timers[index].timer = 6
                new_num_counter += timers[index].num
        timers.append(Timer(timer=8, num=new_num_counter))
        new_num_counter = 0
    return sum(x.num for x in timers)


console = Console()
with open("day06.txt", "r") as file:
    numbers = [int(x) for x in file.readline().strip().split(",")]
    console.print("[b yellow]Day 06 - part 1[/b yellow]")
    console.print(iterate_days(numbers, 80))
    console.print("[b yellow]Day 06 - part 2[/b yellow]")
    console.print(iterate_days(numbers, 256))
