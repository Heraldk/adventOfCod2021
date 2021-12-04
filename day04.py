from rich.console import Console
from typing import List, Tuple, Optional


class BingoCard:
    def __init__(self, numbers: List[int]):
        assert len(numbers) == 25
        self.map = {}
        for index, number in enumerate(numbers):
            self.map[number] = (index // 5, index % 5)
        self.marked_row_count = [0 for _ in range(0, 5)]
        self.marked_col_count = [0 for _ in range(0, 5)]
        self.winner_num = -1

    def mark_number(self, number: int) -> bool:
        if coords := self.map.get(number):
            del self.map[number]
            self.last_marked_num = number

            row, col = coords
            self.marked_row_count[row] += 1
            self.marked_col_count[col] += 1

            if self.marked_row_count[row] == 5 or self.marked_col_count[col] == 5:
                self.winner_num = number
                return True

        return False

    def score_card(self) -> int:
        if self.winner_num >= 0:
            return sum(self.map.keys()) * self.last_marked_num
        else:
            return -1


def play_bingo_game(
    numbers: List[int], bingo_cards: List[BingoCard]
) -> Tuple[Optional[BingoCard], Optional[BingoCard]]:
    cards = bingo_cards
    next_cards = []
    first_winner = None
    last_winner = None

    for number in numbers:
        for card in cards:
            if card.mark_number(number):
                if not first_winner:
                    first_winner = card
                last_winner = card
            else:
                next_cards.append(card)

        cards = list(next_cards)
        next_cards.clear()

    return (first_winner, last_winner)


def read_bingo_cards(file) -> List[BingoCard]:
    current_numbers = []
    bingo_cards = []
    for line in file.readlines():
        current_numbers.extend([int(x) for x in line.strip().split()])
        if len(current_numbers) == 25:
            bingo_cards.append(BingoCard(current_numbers))
            current_numbers.clear()

    return bingo_cards


console = Console()
with open("day04.txt", "r") as file:
    console.print("[b yellow]Day 04[/b yellow]")
    numbers_to_call = [int(x) for x in file.readline().strip().split(",")]
    bingo_cards = read_bingo_cards(file)
    first_winner, last_winner = play_bingo_game(numbers_to_call, bingo_cards)
    print(first_winner.score_card())
    print(last_winner.score_card())
