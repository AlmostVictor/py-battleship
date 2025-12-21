from collections import Counter
from itertools import product


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple,
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        if start[0] == end[0]:
            self.decks = [Deck(start[0], y_coord) for y_coord
                          in range(start[1], end[1] + 1)]
        else:
            self.decks = [Deck(x_coord, start[1]) for x_coord
                          in range(start[0], end[0] + 1)]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False

            if not any(part.is_alive for part in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple[
        tuple[int, int], tuple[int, int]
    ]]) -> None:
        self.fleet = []
        self.field = {}
        for coords in ships:
            ship = Ship(coords[0], coords[1])
            self.fleet.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field.keys():
            return "Miss!"

        cell = self.field[location]
        cell.fire(location[0], location[1])
        if cell.is_drowned:
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        table = [["~" for _ in range(10)] for _ in range(10)]
        for cell, ship in self.field.items():
            if ship.is_drowned:
                table[cell[0]][cell[1]] = "x"
            elif not ship.get_deck(cell[0], cell[1]).is_alive:
                table[cell[0]][cell[1]] = "*"
            else:
                table[cell[0]][cell[1]] = u"\u25A1"

        for row in table:
            print(f"{'\t'.join(row)}")

    def _validate_field(self) -> bool:
        displacements = [coords for coords in product([-1, 0, 1], repeat=2)
                         if coords != (0, 0)]
        for cell in self.field:
            for change in displacements:
                deck = (cell[0] + change[0],
                        cell[1] + change[1])
                if self.field.get(deck) and self.field[deck] != self.field[cell]:
                    return False

        sizes = Counter([len(ship.decks) for ship in self.fleet])
        return all(
            [len(self.fleet) == 10,
             sizes[1] == 4,
             sizes[2] == 3,
             sizes[3] == 2,
             sizes[4] == 1]
        )
