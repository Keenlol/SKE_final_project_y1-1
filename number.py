import copy
from char import Char

class Text:
    def __init__(self, pos, char_size, color, thickness, spacing) -> None:
        self.text = 0
        self.spacing = spacing
        self.x = pos[0]
        self.y = pos[1]
        self.char_width = char_size[0]
        self.char_height = char_size[1]
        self.char_list = [Char(pos, self.char_width, self.char_height, color, thickness)]

    def __update_number_of_char(self):
        diff = len(self.char_list) - len(self.text)
        if diff < 0:
            for _ in range(-diff):
                more_char = copy.deepcopy(self.char_list[0])
                self.char_list.append(more_char)
        elif diff > 0:
            for _ in range(diff):
                self.char_list.pop()

    def __update_char_positions(self):
        center_diff = self.spacing + self.char_width
        n_char = len(self.char_list)

        if n_char % 2 == 1:
            starting_x = self.x + (n_char)/2 * center_diff
            for i in range(len(self.char_list)):
                self.char_list[i].pos = [starting_x - (center_diff * i), self.y]
        else:
            starting_x = self.x + (((n_char)/2) - 0.5) * center_diff
            for i in range(len(self.char_list)):
                self.char_list[i].pos = [starting_x - (center_diff * i), self.y]

    def __draw_the_text(self):
        for i in range(len(self.char_list)):
            self.char_list[i].draw(self.text[i])

    def draw(self, text):
        self.text = text
        self.__update_number_of_char()
        self.__update_char_positions()
        self.__draw_the_text()
