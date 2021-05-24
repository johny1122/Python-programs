import tkinter as tki
from game_board import GameBoard
from widget_name_consts import *

GAME_NAME = "Boggle"

WIN_HEIGHT = 600
WIN_WIDTH = 600

LOGO_PIC_PATH = "boggle_logo.png"

MAIN_COLOR = "blanched almond"
BORDER_COLOR = "black"

MAIN_BORDER_WIDTH = 5
BORDER_THICKNESS = 1

# Sections placing
##########################
MAIN_FRAME_REL_H = 1
MAIN_FRAME_REL_W = 1

HEADER_FRAME_REL_H = 0.2
HEADER_FRAME_REL_W = 1
HEADER_FRAME_REL_Y = 0

GAME_FRAME_REL_H = 0.8
GAME_FRAME_REL_W = 1
GAME_FRAME_REL_Y = 0.2

BOARD_FRAME_REL_H = 1
BOARD_FRAME_REL_W = 0.7

WORDS_FRAME_REL_H = 1
WORDS_FRAME_REL_W = 0.3
WORDS_FRAME_REL_X = 0.7
##########################

START_BUTTON_TEXT = "Start!"
START_BUTTON_WIDTH = 10
START_BUTTON_HEIGHT = 2
START_BUTTON_REL_X = 0.9
START_BUTTON_REL_Y = 0.5

ANCHOR_CENTER = "center"

TIMER_REL_X = 0.1
TIMER_REL_Y = 0.3

INIT_SCORE = "SCORE: 0"

SCORE_REL_X = 0.1
SCORE_REL_Y = 0.6

BUTTONS_FRAME_REL_X = 0.5
BUTTONS_FRAME_REL_Y = 0.5

GUESS_LABEL_H = 2
GUESS_LABEL_W = 20
GUESS_LABEL_REL_X = 0.5
GUESS_LABEL_REL_Y = 0.95
GUESS_LABEL_RELIEF = "ridge"

WORD_LB_REL_H = 1
WORD_LB_REL_X = 0.5
WORD_LB_REL_Y = 0.5


class BoggleGUI:
    """
    This class is responsible on the GUI and starting the game.
    it has the attributes of all the frames on the screen, the image logo
    and the game board object
    """
    def __init__(self, root):
        self.root = root
        self.root.title(GAME_NAME)

        self.main_frame = tki.Frame(self.root)
        self.header_frame = tki.Frame(self.main_frame)
        self.game_frame = tki.Frame(self.main_frame)
        self.words_frame = tki.Frame(self.game_frame)
        self.board_frame = tki.Frame(self.game_frame)
        self.logo_image = tki.PhotoImage(file=LOGO_PIC_PATH)
        self.game_board = GameBoard(self.board_frame, self)

        self.center_win()
        self._init_sections()
        self._style_frames()
        self._init_header()
        self._init_board_frame()
        self._init_word_frame()

    def _style_frames(self):
        """
        The function changes the style of the frames
        """
        self.main_frame.config(borderwidth=MAIN_BORDER_WIDTH,
                               highlightbackground=BORDER_COLOR,
                               highlightthickness=BORDER_THICKNESS)
        self.header_frame.config(borderwidth=MAIN_BORDER_WIDTH,
                                 highlightbackground=BORDER_COLOR,
                                 highlightthickness=BORDER_THICKNESS,
                                 background=MAIN_COLOR)
        self.game_frame.config(borderwidth=MAIN_BORDER_WIDTH,
                               highlightbackground=BORDER_COLOR,
                               highlightthickness=BORDER_THICKNESS,
                               background=MAIN_COLOR)
        self.words_frame.config(borderwidth=MAIN_BORDER_WIDTH,
                                highlightbackground=BORDER_COLOR,
                                highlightthickness=BORDER_THICKNESS,
                                background=MAIN_COLOR)
        self.board_frame.config(borderwidth=MAIN_BORDER_WIDTH,
                                highlightbackground=BORDER_COLOR,
                                highlightthickness=BORDER_THICKNESS,
                                background=MAIN_COLOR)

    def _init_sections(self):
        """
        The function places all the frames in the right places on the screen
        """
        self.main_frame.place(relheight=MAIN_FRAME_REL_H,
                              relwidth=MAIN_FRAME_REL_W)
        self.header_frame.place(rely=HEADER_FRAME_REL_Y,
                                relheight=HEADER_FRAME_REL_H,
                                relwidth=HEADER_FRAME_REL_W)
        self.game_frame.place(rely=GAME_FRAME_REL_Y,
                              relheight=GAME_FRAME_REL_H,
                              relwidth=GAME_FRAME_REL_W)
        self.board_frame.place(relheight=BOARD_FRAME_REL_H,
                               relwidth=BOARD_FRAME_REL_W)
        self.words_frame.place(relheight=WORDS_FRAME_REL_H,
                               relwidth=WORDS_FRAME_REL_W,
                               relx=WORDS_FRAME_REL_X)

    def _init_header(self):
        """
        The function initiates the header frame. it place the start button,
        timer, score and image logo.
        """
        logo_label = tki.Label(self.header_frame,
                               image=self.logo_image,
                               background=MAIN_COLOR)
        logo_label.pack()

        start_button = tki.Button(self.header_frame,
                                  text=START_BUTTON_TEXT,
                                  command=self._start_game,
                                  width=START_BUTTON_WIDTH,
                                  height=START_BUTTON_HEIGHT,
                                  name=START_BUTTON_NAME,
                                  background=MAIN_COLOR)
        start_button.place(relx=START_BUTTON_REL_X, rely=START_BUTTON_REL_Y,
                           anchor=ANCHOR_CENTER)

        timer = tki.Label(self.header_frame, name=TIMER_LABEL_NAME,
                          background=MAIN_COLOR)
        timer.place(relx=TIMER_REL_X, rely=TIMER_REL_Y, anchor=ANCHOR_CENTER)

        score = tki.Label(self.header_frame, name=SCORE_LABEL_NAME,
                          background=MAIN_COLOR)
        score.config(text=INIT_SCORE)
        score.place(relx=SCORE_REL_X, rely=SCORE_REL_Y, anchor=ANCHOR_CENTER)

    def _init_board_frame(self):
        """
        The function initiates the board frame and place the buttons frame
        and guess label
        """
        buttons_frame = tki.Frame(self.board_frame,
                                  name=BUTTONS_FRAME_NAME,
                                  background=MAIN_COLOR)
        buttons_frame.place(relx=BUTTONS_FRAME_REL_X,
                            rely=BUTTONS_FRAME_REL_Y,
                            anchor=ANCHOR_CENTER)

        guess_label = tki.Label(self.board_frame,
                                name=GUESS_LABEL_NAME,
                                height=GUESS_LABEL_H,
                                width=GUESS_LABEL_W,
                                background=MAIN_COLOR)
        guess_label.place(relx=GUESS_LABEL_REL_X, rely=GUESS_LABEL_REL_Y,
                          anchor=ANCHOR_CENTER)
        guess_label.config(relief=GUESS_LABEL_RELIEF)

    def _start_game(self):
        """
        The function starts the game by call th function start_game in
        game_board
        """
        self.header_frame.nametowidget(START_BUTTON_NAME).destroy()
        self.game_board.start_game()

    def _init_word_frame(self):
        """
        The function initiates the list box frame that shows all the found
        words.
        """
        word_listbox = tki.Listbox(self.words_frame,
                                   name=WORD_LISTBOX_NAME,
                                   background=MAIN_COLOR)
        word_listbox.place(relheight=WORD_LB_REL_H, rely=WORD_LB_REL_Y,
                           relx=WORD_LB_REL_X,
                           anchor=ANCHOR_CENTER)

    def center_win(self):
        """
        The function will place the window of the game in the center of the
        screen for any screen size
        """
        self.root.update_idletasks()
        width = WIN_WIDTH
        height = WIN_HEIGHT
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))


boggle = tki.Tk()
b_gui = BoggleGUI(boggle)
boggle.mainloop()
