from __future__ import annotations
from rich.console import Console
from typing import List, Optional
from itertools import permutations
from copy import deepcopy


class SnailfishNum:
    def __init__(self, left, right):
        self.parent = None
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"[{self.left},{self.right}]"

    def reduce(self):
        done = False
        while not done:
            done = True
            # look for a pair to "explode"
            if self.find_explosion(depth=4):
                done = False
            elif self.split():
                done = False

    def magnitude(self) -> int:
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def find_explosion(self, depth: int) -> bool:
        if depth == 1:
            if isinstance(self.left, SnailfishNum):
                self.left.explode()
                self.left = SnailfishLeaf(0)
                return True
            elif isinstance(self.right, SnailfishNum):
                self.right.explode()
                self.right = SnailfishLeaf(0)
                return True

        return self.left.find_explosion(depth - 1) or self.right.find_explosion(
            depth - 1
        )

    def find_left_leaf(self) -> Optional[SnailfishLeaf]:
        prev = self
        current = self.parent
        # go up until there's a path left
        while (current is not None) and (current.left is prev):
            prev = current
            current = current.parent
        # go left
        if current is not None:
            current = current.left
        # go right until we get to a leaf
        while current is not None:
            if isinstance(current, SnailfishLeaf):
                return current
            current = current.right

        return None

    def find_right_leaf(self) -> Optional[SnailfishLeaf]:
        prev = self
        current = self.parent
        # go up until there's a path right
        while (current is not None) and (current.right is prev):
            prev = current
            current = current.parent
        # go right
        if current is not None:
            current = current.right
        # go left until we get to a leaf
        while current is not None:
            if isinstance(current, SnailfishLeaf):
                return current
            current = current.left

        return None

    def explode(self):
        assert isinstance(self.left, SnailfishLeaf)
        assert isinstance(self.right, SnailfishLeaf)
        if left := self.find_left_leaf():
            left.value += self.left.value
        if right := self.find_right_leaf():
            right.value += self.right.value

    def split(self) -> bool:
        if isinstance(self.left, SnailfishLeaf):
            if self.left.value > 9:
                self.left = self.left.split()
                self.left.parent = self
                return True
        elif self.left.split():
            return True

        if isinstance(self.right, SnailfishLeaf):
            if self.right.value > 9:
                self.right = self.right.split()
                self.right.parent = self
                return True
        else:
            return self.right.split()

        return False

    def __add__(self, other) -> SnailfishNum:
        assert isinstance(other, SnailfishNum)
        result = SnailfishNum(deepcopy(self), deepcopy(other))
        result.left.parent = result
        result.right.parent = result
        result.reduce()
        return result


class SnailfishLeaf:
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.value}"

    def find_explosion(self, depth: int) -> bool:
        return False

    def split(self) -> SnailfishNum:
        return SnailfishNum(
            SnailfishLeaf(self.value // 2),
            SnailfishLeaf(self.value - (self.value // 2)),
        )

    def magnitude(self) -> int:
        return self.value


def read_input(line: List[str]) -> SnailfishNum:
    assert line.pop(0) == "["
    if line[0].isdigit():
        left = SnailfishLeaf(int(line.pop(0)))
    elif line[0] == "[":
        left = read_input(line)
    assert line.pop(0) == ","
    if line[0].isdigit():
        right = SnailfishLeaf(int(line.pop(0)))
    elif line[0] == "[":
        right = read_input(line)
    assert line.pop(0) == "]"

    result = SnailfishNum(left, right)
    left.parent = result
    right.parent = result
    return result


console = Console()
with open("day18.txt", "r") as file:
    orig_numbers = [read_input(list(x.strip())) for x in file.readlines()]
    console.print("[b yellow]Day 18[/b yellow]")
    numbers = list(orig_numbers)
    total = numbers.pop(0)
    for num in numbers:
        total += num
    console.print(total, total.magnitude())

    maxMagnitude = 0
    for num1, num2 in permutations(orig_numbers, 2):
        # print(f"{num1} + {num2}, {(num1 + num2).magnitude()}")
        maxMagnitude = max((num1 + num2).magnitude(), maxMagnitude)
    console.print(maxMagnitude)
