import boggle_board_randomizer
import tkinter as tki
from tkinter import messagebox
from letter_button import LetterButton
from timer import Timer
from widget_name_consts import *

BOARD_SIZE = 4

QU_LETTER = "QU"

UNMARKED_COLOR = "white"
MARKED_COLOR = "red"
POSS_MOVE_COLOR = "coral"

INIT_SCORE = "SCORE: 0"
SCORE_PREFIX = "SCORE: "

NO_TIME_LEFT = "00:00"

DICT_FILE_PATH = "boggle_dict.txt"

GAME_OVER_TITLE = "Game Over"
GAME_OVER_MSG_1 = "Time's up! your score: "
GAME_OVER_MSG_2 = "\nDo you want to play again?"

MSG_BOX_TITLE = "Get Ready!"
MSG_BOX_MSG = "You will now start a new game"
MSG_BOX_ICON = "question"
MSG_BOX_NO = "no"

BUTTON_WID_RELIEF_RAISED = "raised"
BUTTON_WID_RELIEF_SOLID = "solid"

BUTTON_WIDTH = 10
BUTTON_HEIGHT = 4


class GameBoard:
    """
    This class is responsible on the game and the rules
    it has the attributes:
    - parent = the root of the board game
    - board = a list of lists of the board's letters
    - letter_buttons = a dict of letter_buttons objects
    - letters_path = a list coordinates of the path the player chose to click
    - guess_label = the widget of the label showing the current player's path
    - timer = timer object
    - words_set = set of all the possible words in the game
    """

    def __init__(self, parent, master):
        self.master = master
        self.parent = parent
        self.board = None
        self.letter_buttons = {}
        self.letters_path = []
        self.guess_label = None
        self.timer = None
        self.words_set = set()
        self._import_words()

    def _init_board(self):
        """
        The function initiates the board with a randomize board. it creates
        the letter_buttons and place them on the board frame
        """
        self.board = boggle_board_randomizer.randomize_board()
        self.guess_label = \
            self.master.board_frame.nametowidget(GUESS_LABEL_NAME)
        buttons_frame = self.master.board_frame.nametowidget(
            BUTTONS_FRAME_NAME)
        for row_index in range(len(self.board)):
            for col_index in range(len(self.board[row_index])):
                curr_button = \
                    tki.Button(buttons_frame,
                               text=self.board[row_index][
                                   col_index],
                               command=lambda row=row_index, col=col_index:
                               self.button_click(row, col),
                               width=BUTTON_WIDTH,
                               height=BUTTON_HEIGHT)
                curr_button.config(bg=UNMARKED_COLOR)
                curr_button.grid(row=row_index, column=col_index)
                self.letter_buttons[(row_index, col_index)] = \
                    LetterButton(row_index,
                                 col_index,
                                 curr_button,
                                 self.board[row_index][col_index])

    def button_click(self, row, col):
        """
        The function gets a coordinate of a button and defines what happen
        when the button was clicked for each situation in the game.
        """
        # If empty or not white
        if self.letter_buttons[(row, col)].get_color() != UNMARKED_COLOR or \
                not self.letters_path:
            # path board is empty
            if not self.letters_path:
                self.letter_buttons[(row, col)].set_color(MARKED_COLOR)
                self.letters_path.append((row, col))
                self.mark_possible_moves()
                self.guess_label["text"] += self.letter_buttons[
                    self.letters_path[-1]].letter
            # We clicked the last button in path to unmark
            elif (row, col) == self.letters_path[-1]:
                self.unmark_possible_moves()
                self.letters_path.pop()
                self.letter_buttons[(row, col)].set_color(UNMARKED_COLOR)
                if self.letters_path:
                    self.mark_possible_moves()
                self.guess_label["text"] = self.guess_label["text"][:-1]
                if self.letter_buttons[(row, col)].letter == QU_LETTER:
                    self.guess_label["text"] = self.guess_label["text"][:-1]
            # Marking the next possible letter to choose
            elif self.letter_buttons[
                (row, col)].get_color() == POSS_MOVE_COLOR:
                self.unmark_possible_moves()
                self.letter_buttons[(row, col)].set_color(MARKED_COLOR)
                self.letters_path.append((row, col))
                self.mark_possible_moves()
                self.guess_label["text"] += self.letter_buttons[
                    self.letters_path[-1]].letter

            self.search_word()

    def mark_possible_moves(self):
        """
        The function marks the possible moves of the current clicked button
        according to the current board state.
        it also marks the clicked button with a different border
        """
        last_letter_button = self.letter_buttons[self.letters_path[-1]]
        last_letter_button.button_widget["relief"] = BUTTON_WID_RELIEF_SOLID
        for coords in last_letter_button.possible_moves:
            if self.letter_buttons[coords].get_color() != MARKED_COLOR:
                self.letter_buttons[coords].set_color(POSS_MOVE_COLOR)

    def unmark_possible_moves(self):
        """
        The function unmark the current possible moves and the last clicked
        button
        """
        last_letter_button = self.letter_buttons[self.letters_path[-1]]
        last_letter_button.button_widget["relief"] = BUTTON_WID_RELIEF_RAISED
        if not self.letters_path:
            self.letter_buttons[self.letters_path[-1]].button_widget[
                "relief"] = BUTTON_WID_RELIEF_SOLID
        for coord in last_letter_button.possible_moves:
            if self.letter_buttons[coord].get_color() == POSS_MOVE_COLOR:
                self.letter_buttons[coord].set_color(UNMARKED_COLOR)

    def search_word(self):
        """
        The function searched if the current path the player did is in the
        list of possible words.
        if so, it will stop the path, add the word to the found word list
        and start a new player turn
        """
        guess_str = self.guess_label["text"]

        if guess_str in self.words_set:
            self.add_word(guess_str)
            self.clear_board()

    def clear_board(self):
        """
        The function clears the board from marked buttons after finding a good
        word
        """
        self.guess_label["text"] = ""
        self.letters_path = []

        for button in self.letter_buttons.values():
            button.button_widget["relief"] = BUTTON_WID_RELIEF_RAISED
            button.set_color(UNMARKED_COLOR)

    def start_game(self):
        """
        The function starts the game. it initiates the board and start the
        timer
        """
        self._init_board()
        self.timer = Timer()
        self._update_time()

    def restart_game(self):
        """
        The function restart the game after the timer finished and the
        player wanted to play again
        """
        self.master.header_frame.nametowidget(SCORE_LABEL_NAME)[
            "text"] = INIT_SCORE
        self.master.words_frame.nametowidget(WORD_LISTBOX_NAME).delete(0,
                                                                       tki.END)
        self.guess_label["text"] = ""
        self.letters_path = []
        self._import_words()
        self.start_game()

    def _update_time(self):
        """
        The function updates the time on the time with root.after
        If the timer finished the function will call the game_over function
        to finish the game.
        """
        curr_time = self.timer.get_time()
        self.master.header_frame.nametowidget(TIMER_LABEL_NAME).config(
            text=curr_time)

        if curr_time == NO_TIME_LEFT:
            self.game_over()
            return

        self.master.root.after(1000, self._update_time)

    def _import_words(self):
        """
        The function imports the possible words from a file and saves them
        in the attribute self.words_set
        """
        words_file = open(DICT_FILE_PATH, "r")
        self.words_set = set([word.replace("\n", "") for word in
                              words_file.readlines()])

    def add_word(self, word):
        """
        The function adds a word to the found words list after the player
        found a good word in the board. it also removes the word from the
        possible words list so the player will not find it again and calls
        the function update_score to update the score
        """
        self.master.words_frame.nametowidget(WORD_LISTBOX_NAME).insert(tki.END,
                                                                       word)
        self.words_set.remove(word)
        self.update_score(word)

    def update_score(self, word=None):
        """
        The function updates the player score after finding a good word and
        showing it on the on the screen
        """
        score = \
            int(self.master.header_frame.nametowidget(SCORE_LABEL_NAME)[
                "text"].replace(
                SCORE_PREFIX, ""))
        if word:
            score += int(len(word) ** 2)
        else:
            score = 0

        self.master.header_frame.nametowidget(SCORE_LABEL_NAME)["text"] = \
            SCORE_PREFIX + str(score)

    def game_over(self):
        """
        The function open a message box and asks the player after the timer
        was finished if he would like to play again or exit. if the player
        chose to play again it will call the function restart_game. if not
        it will terminate the program
        """
        msg_box = \
            tki.messagebox.askquestion(GAME_OVER_TITLE,
                                       GAME_OVER_MSG_1 +
                                       self.master.header_frame.nametowidget(
                                           SCORE_LABEL_NAME)["text"].replace(
                                           SCORE_PREFIX, "") +
                                       GAME_OVER_MSG_2,
                                       icon=MSG_BOX_ICON)
        if msg_box == MSG_BOX_NO:
            self.master.root.destroy()
        else:
            tki.messagebox.showinfo(MSG_BOX_TITLE,
                                    MSG_BOX_MSG)
            self.restart_game()
