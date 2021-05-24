BOARD_SIZE = 4


class LetterButton:
    """
    This class defines a button of a letter in the board game.
    each letter button has the attributes:
    - row / column
    - color of background
    - button content - the letter
    - button widget of the specific button
    - list of all the legal possible moves around the specific button
    """
    def __init__(self, row, col, button_widget, letter):
        self.row = row
        self.col = col
        self.color = button_widget["bg"]
        self.letter = letter.upper()
        self.button_widget = button_widget
        self.possible_moves = []

        self._init_possible_moves()

    def _init_possible_moves(self):
        """
        The function creates the possible moves list of the current button
        and saves it in the attribute self.possible_moves
        """
        for row_index in range(self.row - 1, self.row + 2):
            for col_index in range(self.col - 1, self.col + 2):
                if self.is_coord_in_board(row_index, col_index) and \
                        (row_index != self.row or col_index != self.col):
                    self.possible_moves.append((row_index, col_index))

    @staticmethod
    def is_coord_in_board(row, col):
        """
        The function returns True if a given coordinate is in the board and
        False otherwise
        """
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color
        self.button_widget["bg"] = color
