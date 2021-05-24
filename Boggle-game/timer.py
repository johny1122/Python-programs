GAME_TIME = 180
SEC_IN_MIN = 60
ZERO_STR = "0"
NO_TIME_LEFT = "00:00"


class Timer:
    """
    This class is responsible about the timer in the game.
    the class has an attribute of the current time left in the game
    """
    def __init__(self):
        self.game_time = GAME_TIME + 1

    def get_time(self):
        """
        The function calculates the time to show to the user according to
        the current time in the game
        :return: String of the current time
        """
        self.game_time -= 1
        if self.game_time > 0:
            minutes = int(self.game_time / SEC_IN_MIN)
            seconds = int(self.game_time % SEC_IN_MIN)

            minutes = str(minutes)
            seconds = str(seconds)

            if len(minutes) == 1:
                minutes = ZERO_STR + minutes
            if len(seconds) == 1:
                seconds = ZERO_STR + seconds

            return minutes + ":" + seconds
        else:
            return NO_TIME_LEFT
