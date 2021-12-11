from dataclasses import dataclass
from rich.console import Console
from typing import List, Set


class Code:
    def __init__(self, unique_signals: List[str], output: List[str]):
        self.unique_signals = ["".join(sorted(x)) for x in unique_signals]
        self.output = ["".join(sorted(x)) for x in output]

    def __repr__(self) -> str:
        return f"{self.unique_signals} | {self.output}"

    @classmethod
    def read_input(cls, lines: List[str]):
        result = []
        for line in lines:
            vals = line.strip().split()
            bar = vals.index("|")
            result.append(Code(list(vals[0:bar]), list(vals[bar + 1 :])))

        return result


def count_unique_digit_codes(codes: List[Code]):
    count = 0
    for code in codes:
        for output in code.output:
            if len(output) in [2, 3, 4, 7]:
                count += 1
    return count


@dataclass
class Digit:
    number: int
    segments: Set[str]

    @classmethod
    def get_digits(cls):
        return {
            0: Digit(0, set("abcefg")),
            1: Digit(1, set("cf")),
            2: Digit(2, set("acdeg")),
            3: Digit(3, set("acdfg")),
            4: Digit(4, set("bcdf")),
            5: Digit(5, set("abdfg")),
            6: Digit(6, set("abdefg")),
            7: Digit(7, set("acf")),
            8: Digit(8, set("abcdefg")),
            9: Digit(9, set("abcdfg")),
        }


def decode_line(code: Code) -> int:
    possibles = {}
    digits = Digit.get_digits()
    signal_to_number_mapping = {}
    number_to_signal_set_mapping = {}

    for signal in code.unique_signals:
        possibles[signal] = [
            num for num, digit in digits.items() if len(digit.segments) == len(signal)
        ]
        if len(possibles[signal]) == 1:
            signal_to_number_mapping[signal] = possibles[signal][0]
            number_to_signal_set_mapping[possibles[signal][0]] = set(signal)
            del possibles[signal]

    # hacky hacky hack
    # look for the 3 (must contain the one)
    pattern = number_to_signal_set_mapping[1]
    for key, vals in possibles.items():
        if vals.count(3) > 0:
            if set(key).intersection(pattern) == pattern:
                signal_to_number_mapping[key] = 3
                number_to_signal_set_mapping[3] = set(key)
                del possibles[key]
                break

    # now look for the 0 using the 1 and 3
    pattern = number_to_signal_set_mapping[3] - number_to_signal_set_mapping[1]
    for key, vals in possibles.items():
        if vals.count(0) > 0:
            if set(key).intersection(pattern) != pattern:
                signal_to_number_mapping[key] = 0
                number_to_signal_set_mapping[0] = set(key)
                del possibles[key]
                break

    # now we can use the 1 to find the 9 and the 6
    pattern = number_to_signal_set_mapping[1]
    for key, vals in possibles.items():
        if vals.count(9) > 0:
            if set(key).intersection(pattern) == pattern:
                signal_to_number_mapping[key] = 9
                number_to_signal_set_mapping[9] = set(key)
            elif set(key).intersection(pattern) != pattern:
                signal_to_number_mapping[key] = 6
                number_to_signal_set_mapping[6] = set(key)

    # finally use 9 and 1 to find the 5 (and therefore the 2)
    pattern = number_to_signal_set_mapping[1]
    for key, vals in possibles.items():
        if vals.count(2) > 0:
            if (
                set(key).union(number_to_signal_set_mapping[1])
                == number_to_signal_set_mapping[9]
            ):
                signal_to_number_mapping[key] = 5
                number_to_signal_set_mapping[5] = set(key)
            else:
                signal_to_number_mapping[key] = 2
                number_to_signal_set_mapping[2] = set(key)

    # finally, use the mapping to return an integer
    num = 0
    for val in code.output:
        num = num * 10 + signal_to_number_mapping[val]
    return num


def decode_lines(codes: List[Code]) -> List[int]:
    result = [decode_line(code) for code in codes]
    return result


console = Console()
with open("day08.txt", "r") as file:
    input = Code.read_input(file.readlines())
    console.print("[b yellow]Day 08 - part 1[/b yellow]")
    console.print(count_unique_digit_codes(input))
    result = decode_lines(input)
    console.print("[b yellow]Day 08 - part 2[/b yellow]")
    console.print(sum(result))
