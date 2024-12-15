import copy
from char import Char

class Text:
    def __init__(self ,text ,pos, char_size, color, thickness, spacing) -> None:
        self._text = text.upper()
        self._spacing = spacing
        self._x = pos[0]
        self._y = pos[1]
        self._char_width = char_size[0]
        self._char_height = char_size[1]
        self._thickness = thickness
        self._color = color
        self.__update_char_style()

    def __update_char_style(self):
        self._char_list = [Char([self._x, self._y], self._char_width, self._char_height, self._color, self._thickness)]

    def __update_number_of_char(self):
        diff = len(self._char_list) - len(self._text)
        if diff < 0:
            for _ in range(-diff):
                more_char = copy.deepcopy(self._char_list[0])
                self._char_list.append(more_char)
        elif diff > 0:
            for _ in range(diff):
                self._char_list.pop()

    def __update_char_positions(self):
        center_diff = self._spacing + self._char_width
        n_char = len(self._char_list)

        starting_x = self._x - (((n_char)/2) - 0.5) * center_diff

        for i in range(len(self._char_list)):
            self._char_list[i].pos = [starting_x + (center_diff * i), self._y]

    def __draw_the_text(self):
        for i in range(len(self._char_list)):
            self._char_list[i].draw(self._text[i])

    def draw(self):
        self.__update_char_style()
        self.__update_number_of_char()
        self.__update_char_positions()
        self.__draw_the_text()
