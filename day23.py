from __future__ import annotations
from rich.console import Console
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set
from enum import Enum
from frozendict import frozendict
import heapq
from itertools import count

console = Console()


@dataclass(order=True, frozen=True)
class Coords:
    x: int
    y: int

    def get_neighbours(self) -> List[Coords]:
        return [
            Coords(self.x - 1, self.y),
            Coords(self.x, self.y - 1),
            Coords(self.x + 1, self.y),
            Coords(self.x, self.y + 1),
        ]


class SpaceType(Enum):
    HALLWAY = 0
    DOORWAY = 1
    A_HOME = 2
    B_HOME = 3
    C_HOME = 4
    D_HOME = 5

    def __add__(self, other):
        if isinstance(other, int):
            val = (self.value + other) % 6
            for type in SpaceType:
                if type.value == val:
                    return type

    def is_home(self):
        return self != SpaceType.HALLWAY and self != SpaceType.DOORWAY

    def is_home_for(self, amphipod: str):
        return (
            (self == SpaceType.A_HOME and amphipod == "A")
            or (self == SpaceType.B_HOME and amphipod == "B")
            or (self == SpaceType.C_HOME and amphipod == "C")
            or (self == SpaceType.D_HOME and amphipod == "D")
        )

    @staticmethod
    def get_home_column_for(amphipod: str):
        lookup: Dict[str, int] = {
            "A": 3,
            "B": 5,
            "C": 7,
            "D": 9,
        }
        return lookup[amphipod]

    def get_energy_for_step(amphipod: str):
        energyUse: Dict[str, int] = {
            "A": 1,
            "B": 10,
            "C": 100,
            "D": 1000,
        }
        return energyUse[amphipod]


@dataclass(frozen=True, eq=True)
class GameState:
    map: Dict[Coords, SpaceType]
    amphipods: Dict[Coords, str]

    def gen_moves_for_pod(
        self, amphipod: str, starting_loc: Coords
    ) -> List[Tuple[GameState, int]]:
        moves = []
        queue = [(starting_loc, 0)]
        explored = set()
        home_move = False
        while len(queue) > 0:
            current_loc, num_moves = queue.pop()
            explored.add(current_loc)
            for neighbour in current_loc.get_neighbours():
                if neighbour in explored:
                    continue
                if neighbour not in self.map:
                    continue  # skip non-map locs
                if neighbour in self.amphipods:
                    continue  # can't walk through other amphipods
                map_type: SpaceType = self.map[neighbour]
                starting_type: SpaceType = self.map[starting_loc]
                if (
                    map_type.is_home()
                    and not map_type.is_home_for(amphipod)
                    and starting_type != map_type
                ):
                    continue  # this amphipod can't move into other homes, but can move out of starting home

                queue.append(
                    (neighbour, num_moves + 1)
                )  # we can at least move through this space
                valid_move = False
                if map_type == SpaceType.HALLWAY and starting_type != SpaceType.HALLWAY:
                    valid_move = True
                elif map_type.is_home_for(amphipod):
                    # only valid if no other amphipods in this spot
                    # and if moving to the deepest spot
                    deeper = Coords(neighbour.x, neighbour.y + 1)
                    while deeper in self.map:
                        if (
                            not deeper in self.amphipods
                            or self.amphipods[deeper] != amphipod
                        ):
                            break
                        deeper = Coords(neighbour.x, deeper.y + 1)
                    if not deeper in self.map:
                        valid_move = True
                        home_move = True

                if valid_move:
                    new_amphipods = dict(self.amphipods)
                    del new_amphipods[starting_loc]
                    new_amphipods[neighbour] = amphipod
                    if home_move:
                        moves.clear()
                    moves.append(
                        (
                            GameState(self.map, frozendict(new_amphipods)),
                            (num_moves + 1) * SpaceType.get_energy_for_step(amphipod),
                        )
                    )
                    if home_move:
                        return moves

        return moves

    def is_completed(self) -> bool:
        for loc, amphipod in self.amphipods.items():
            if not self.map[loc].is_home_for(amphipod):
                return False
        return True

    def heuristic_distance_to_goal(self) -> int:
        heuristic = 0
        for loc, amphipod in self.amphipods.items():
            if self.map[loc].is_home_for(amphipod):
                continue
            goal_col = SpaceType.get_home_column_for(amphipod)
            distance = abs(loc.x - goal_col) + (abs(loc.y - 1) + 1)
            heuristic += distance * SpaceType.get_energy_for_step(amphipod)
        return heuristic

    def __repr__(self) -> str:
        result = "\n"
        for y in range(0, 7):
            for x in range(0, 14):
                coords = Coords(x, y)
                if coords in self.amphipods:
                    result += self.amphipods[coords]
                elif coords in self.map:
                    result += "."
                else:
                    result += "#"
            result += f"\n"
        result += f"{self.heuristic_distance_to_goal()}\n"
        return result

    def gen_moves(self) -> Tuple[List[GameState], int]:
        moves = []
        for amphipods_loc, amphipod in self.amphipods.items():
            moves.extend(self.gen_moves_for_pod(amphipod, amphipods_loc))
        return moves


def read_input(input: List[str]) -> GameState:
    map = {}
    locs = {}
    for y, line in enumerate(input):
        next_home = SpaceType.A_HOME
        for x, char in enumerate(line):
            if char == ".":
                map[Coords(x, y)] = SpaceType.HALLWAY
            elif char in "ABCD":
                map[Coords(x, y)] = next_home
                locs[Coords(x, y)] = char
                next_home = next_home + 1
                if map[Coords(x, y - 1)] == SpaceType.HALLWAY:
                    map[Coords(x, y - 1)] = SpaceType.DOORWAY
    return GameState(frozendict(map), frozendict(locs))


def reconstruct_path(came_from, current) -> List[GameState]:
    path = [current]
    state = current
    while state in came_from:
        state = came_from[state]
        path.insert(0, state)
    return path


def a_star_search(start: GameState) -> int:
    open_set: List[Tuple[int, GameState]] = []
    counter = count()
    next_num = next(counter)
    heapq.heappush(open_set, (0, next_num, start))

    gScore: Dict[GameState, int] = {}
    gScore[start] = 0
    fScore: Dict[GameState, int] = {}
    fScore[start] = start.heuristic_distance_to_goal()
    explored: Set[GameState] = set()

    came_from = {}

    while len(open_set) > 0:
        _, _, current = heapq.heappop(open_set)

        if current in explored:
            continue
        if current.is_completed():
            return gScore[current], reconstruct_path(came_from, current)

        explored.add(current)

        moves = current.gen_moves()
        for move, cost in moves:
            new_gscore = gScore[current] + cost
            if move not in gScore or new_gscore < gScore[move]:
                came_from[move] = current
                gScore[move] = new_gscore
                fScore[move] = new_gscore + move.heuristic_distance_to_goal()
                next_num = next(counter)
                heapq.heappush(open_set, (fScore[move], next_num, move))

    return None


with open("day23.txt", "r") as file:
    hall = read_input(file.readlines())
    console.print("[b yellow]Day 23 - part 1[/b yellow]")
    score, path = a_star_search(hall)
    console.print(path)
    console.print(score)

with open("day23.txt", "r") as file:
    lines = file.readlines()
    lines.insert(3, "  #D#C#B#A#")
    lines.insert(4, "  #D#B#A#C#")
    hall = read_input(lines)
    console.print("[b yellow]Day 23 - part 2[/b yellow]")
    score, path = a_star_search(hall)
    console.print(path)
    console.print(score)
