from __future__ import annotations
from rich.console import Console
from typing import List, Tuple, Dict
from dataclasses import dataclass


def day01():
    pass


def starting_pos(input: List[str]) -> List[int]:
    startings = []
    for line in input:
        vals = line.strip().split()
        startings.append(int(vals[4]) - 1)  # do zero based locations
    return startings


def simple_play_game(starting_pos: List[int]) -> Tuple[int, int]:
    done = False
    turn = 0
    die_rolls = 0
    prev_die = 0
    current_pos = list(starting_pos)
    scores = [0 for _ in starting_pos]
    while not done:
        roll = prev_die * 3 + 6
        current_pos[turn] = (current_pos[turn] + roll) % 10
        scores[turn] += current_pos[turn] + 1
        die_rolls += 3
        if scores[turn] >= 1000:
            done = True

        prev_die += 3
        turn = (turn + 1) % len(starting_pos)

    return die_rolls, scores[turn]


@dataclass(frozen=True)
class GameState:
    player1_loc: int
    player1_score: int

    player2_loc: int
    player2_score: int

    turn: int

    def __repr__(self) -> str:
        return f"p1{self.player1_loc} ({self.player1_score}) - p2{self.player2_loc} ({self.player2_score}) - {self.turn}"

    def play_turn(self, die_roll: int) -> GameState:
        if self.turn == 0:
            player1_newloc = (self.player1_loc + die_roll) % 10
            return GameState(
                player1_newloc,
                self.player1_score + player1_newloc + 1,
                self.player2_loc,
                self.player2_score,
                1 - self.turn,
            )
        else:
            player2_newloc = (self.player2_loc + die_roll) % 10
            return GameState(
                self.player1_loc,
                self.player1_score,
                player2_newloc,
                self.player2_score + player2_newloc + 1,
                1 - self.turn,
            )


roll_result_freq = ((3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1))


def play_quantum_game(
    game_state: GameState, cache: Dict[GameState, Tuple[int, int]]
) -> Tuple[int, int]:
    if game_state.player1_score >= 21:
        return 1, 0
    elif game_state.player2_score >= 21:
        return 0, 1

    if game_state in cache:
        return cache[game_state]

    wins1, wins2 = 0, 0
    for die_roll, freq in roll_result_freq:
        sub_wins1, sub_wins2 = play_quantum_game(game_state.play_turn(die_roll), cache)
        wins1 += sub_wins1 * freq
        wins2 += sub_wins2 * freq

    cache[game_state] = wins1, wins2

    return wins1, wins2


console = Console()
with open("day21.txt", "r") as file:
    starting = starting_pos(file.readlines())
    console.print("[b yellow]Day 21[/b yellow]")
    die_rolls, losing_score = simple_play_game(starting)
    console.print(f"{die_rolls} * {losing_score} = {die_rolls * losing_score}")

    wins1, wins2 = play_quantum_game(GameState(starting[0], 0, starting[1], 0, 0), {})
    console.print(wins1, wins2)
