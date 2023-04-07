class Note:
    def __init__(self, date, time, text):
        self.__date = date
        self.__time = time
        self.__text = text


class Schedule:
    def __init__(self, days, pairs, state):
        self.__days = days
        self.__pairs = pairs
        self.__state = state
