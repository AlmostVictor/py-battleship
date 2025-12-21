class Deck:
    def __init__(self, row: int, column: int, is_alive: bool=True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned: bool=False) -> None:
        self.start = start
        self.end = end
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
        self.field = {}
        for coords in ships:
            ship = Ship(coords[0], coords[1])
            for deck in ship.decks:
                self.field[deck] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field.keys():
            return "Miss!"

        cell = self.field[location]
        cell.fire(location[0], location[1])
        if cell.is_drowned:
            return "Sunk!"
        return "Hit!"
