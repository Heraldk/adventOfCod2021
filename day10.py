from rich.console import Console
from typing import Tuple


def score_result(char: str) -> int:
    score_map = {")": 3, "]": 57, "}": 1197, ">": 25137}
    return score_map[char]


def score_valid(char: str) -> int:
    score_map = {")": 1, "]": 2, "}": 3, ">": 4}
    return score_map[char]


def score_string(line: str) -> Tuple[int, int]:
    validator = []
    open_to_close = {"[": "]", "{": "}", "<": ">", "(": ")"}
    for char in line.strip():
        if char in "[<{(":
            validator.append(char)
        elif len(validator) == 0:
            return score_result(char), 0
        else:
            last = validator.pop()
            if open_to_close[last] != char:
                return score_result(char), 0

    valid_score = 0
    while len(validator) > 0:
        last = validator.pop()
        valid_score *= 5
        valid_score += score_valid(open_to_close[last])

    return 0, valid_score


console = Console()
with open("day10.txt", "r") as file:
    lines = file.readlines()
    console.print("[b yellow]Day 10[/b yellow]")
    invalid_score_sum = 0
    valid_scores = []
    for line in lines:
        invalid_score, valid_score = score_string(line)
        if invalid_score:
            invalid_score_sum += invalid_score
        else:
            valid_scores.append(valid_score)
    console.print(invalid_score_sum)
    valid_scores = sorted(valid_scores)
    console.print(valid_scores[len(valid_scores) // 2])
