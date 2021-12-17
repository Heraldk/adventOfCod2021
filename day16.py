from rich.console import Console
from typing import List
from math import prod


class LiteralPacket:
    def __init__(self, version, type, value):
        self.version: int = version
        self.type: int = type
        self.value: int = value

    def version_sum(self):
        return self.version

    def evaluate(self):
        return self.value

    def __repr__(self):
        return f"{self.version} {self.type} {self.value}"


class OperatorPacket:
    def __init__(self, version, type, packets):
        self.version: int = version
        self.type: int = type
        self.packets = packets

    def version_sum(self):
        return sum([x.version_sum() for x in self.packets]) + self.version

    def evaluate(self):
        if self.type == 0:
            return sum([x.evaluate() for x in self.packets])
        elif self.type == 1:
            return prod([x.evaluate() for x in self.packets])
        elif self.type == 2:
            return min([x.evaluate() for x in self.packets])
        elif self.type == 3:
            return max([x.evaluate() for x in self.packets])
        elif self.type == 5:
            assert len(self.packets) == 2
            val1 = self.packets[0].evaluate()
            val2 = self.packets[1].evaluate()
            return 1 if val1 > val2 else 0
        elif self.type == 6:
            assert len(self.packets) == 2
            val1 = self.packets[0].evaluate()
            val2 = self.packets[1].evaluate()
            return 1 if val1 < val2 else 0
        elif self.type == 7:
            assert len(self.packets) == 2
            val1 = self.packets[0].evaluate()
            val2 = self.packets[1].evaluate()
            return 1 if val1 == val2 else 0

    def __repr__(self):
        return f"{self.version} {self.type} {self.packets}"


def read_input(hex_str: str) -> List[str]:
    result = []
    for char in hex_str:
        num = int(char, 16)
        for bindigit in f"{num:04b}":
            result.append(bindigit)
    return result


def parse_packet(bindigits: List[str]):
    version = int("".join(bindigits[:3]), 2)
    del bindigits[:3]
    type = int("".join(bindigits[:3]), 2)
    del bindigits[:3]

    if type == 4:  # literal
        binstr = ""
        done = False
        while not done:
            indicator = bindigits.pop(0)
            binstr += "".join(bindigits[:4])
            del bindigits[:4]
            if indicator == "0":
                done = True
        number = int(binstr, 2)
        return LiteralPacket(version, type, number)
    else:
        length_type = bindigits.pop(0)
        packets = []
        if length_type == "0":
            packets_length = int("".join(bindigits[:15]), 2)
            del bindigits[:15]
            next_bindigits = bindigits[:packets_length]
            del bindigits[:packets_length]
            while len(next_bindigits) > 0:
                packets.append(parse_packet(next_bindigits))
        else:
            num_packets = int("".join(bindigits[:11]), 2)
            del bindigits[:11]
            for _ in range(num_packets):
                packets.append(parse_packet(bindigits))
        return OperatorPacket(version, type, packets)


console = Console()
with open("day16.txt", "r") as file:
    input = file.readline().strip()
    console.print("[b yellow]Day 16[/b yellow]")
    binstr = read_input(input)
    packet = parse_packet(binstr)
    console.print(packet.version_sum())
    console.print(packet.evaluate())
