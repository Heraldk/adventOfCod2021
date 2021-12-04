from rich.console import Console
from typing import List, Tuple


def count_bit_freq(bin_numbers: List[int]) -> Tuple[int, int]:
    counts = {}
    for number in bin_numbers:
        index = 0
        while number > 0:
            if number & 1:
                counts[index] = counts.get(index, 0) + 1
            index += 1
            number >>= 1

    most_freq_number = 0
    least_freq_number = 0
    for index in sorted(counts, reverse=True):
        most_freq_number <<= 1
        least_freq_number <<= 1
        if counts[index] * 2 >= len(bin_numbers):
            most_freq_number |= 1
        elif counts[index] * 2 < len(bin_numbers):
            least_freq_number |= 1

    return most_freq_number, least_freq_number


def filter_and_repeat(bin_numbers: List[int], num_bits: int, use_most: bool) -> int:
    bit_position = 1 << (num_bits - 1)

    nums = bin_numbers
    while len(nums) > 1:
        most_freq_number, least_freq_number = count_bit_freq(nums)
        comparison = most_freq_number if use_most else least_freq_number
        nums = [x for x in nums if (comparison & bit_position) == (x & bit_position)]
        bit_position >>= 1

    return nums[0]


console = Console()

# hacky way to get the number of bits we're dealing with
bit_str_len = 0
with open("day03.txt", "r") as file:
    first_line = file.readline()
    bit_str_len = len(first_line.strip())

with open("day03.txt", "r") as file:
    lines = [int(x, 2) for x in file.readlines()]

    console.print("[b yellow]Day 03 - part 1[/b yellow]")
    result = count_bit_freq(lines)
    console.print(f"{result} = {result[0] * result[1]}")

    console.print("[b yellow]Day 03 - part 2[/b yellow]")
    result_oxygen = filter_and_repeat(lines, bit_str_len, True)
    result_co2 = filter_and_repeat(lines, bit_str_len, False)
    console.print(f"{result_oxygen} {result_co2} = {result_oxygen * result_co2}")
