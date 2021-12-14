from rich.console import Console
from typing import List, Tuple, Dict
from collections import Counter


def read_mappings(lines: List[str]) -> Dict[str, str]:
    mapping = {}
    for line in lines:
        vals = line.strip().split(" -> ")
        mapping[vals[0]] = vals[1]
    return mapping


def simple_expansion(starting_str: str, iterations: int, mapping: Dict[str, str]):
    next_str = starting_str
    for _ in range(0, iterations):
        current_str = next_str
        next_str = ""
        for i, char in enumerate(current_str):
            if i + 1 < len(current_str):
                next_str += char
                next_str += mapping[f"{char}{current_str[i+1]}"]
            else:
                next_str += char
    return next_str


def recursive_memory(
    current_str: str,
    iterations: int,
    memory: Dict[str, Dict[int, Counter]],
    mapping: Dict[str, str],
) -> Counter:
    if iterations == 0:
        return Counter(current_str)

    current_counter = Counter()
    for i, char in enumerate(current_str):
        if i + 1 < len(current_str):
            pair = f"{char}{current_str[i+1]}"

            # check if we've done this pair already:
            if lookup := memory.get(pair):
                if counter := lookup.get(iterations - 1):
                    # print(f"found in map: {pair} -> {counter}")
                    current_counter.update(counter)
                    continue

            # we're still here, so descend:
            next_str = f"{char}{mapping[pair]}{current_str[i+1]}"
            counter = recursive_memory(next_str, iterations - 1, memory, mapping)
            counter.subtract(current_str[i + 1])

            if pair not in memory:
                memory[pair] = {}
            memory[pair][iterations - 1] = counter
            current_counter.update(counter)
        else:
            current_counter.update(char)

    return current_counter


console = Console()
with open("day14.txt", "r") as file:
    starting_string, _, *mapping_input = file.readlines()
    starting_string = starting_string.strip()
    console.print("[b yellow]Day 14[/b yellow]")
    mapping = read_mappings(mapping_input)

    result_str = simple_expansion(starting_string, 10, mapping)
    counter = Counter(result_str)
    print(counter.most_common()[0][1] - counter.most_common()[-1][1])

    counter_part2 = recursive_memory(starting_string, 40, {}, mapping)
    print(counter_part2)
    print(counter_part2.most_common()[0][1] - counter_part2.most_common()[-1][1])
