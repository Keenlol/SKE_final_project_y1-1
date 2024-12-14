import copy
from char import Char

class Text:
    def __init__(self ,text ,pos, char_size, color, thickness, spacing) -> None:
        self.text = text
        self.spacing = spacing
        self.x = pos[0]
        self.y = pos[1]
        self.char_width = char_size[0]
        self.char_height = char_size[1]
        self.thickness = thickness
        self.color = color
        self.__update_char_style()

    def __update_char_style(self):
        self.char_list = [Char([self.x, self.y], self.char_width, self.char_height, self.color, self.thickness)]

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

        starting_x = self.x - (((n_char)/2) - 0.5) * center_diff

        for i in range(len(self.char_list)):
            self.char_list[i].pos = [starting_x + (center_diff * i), self.y]

    def __draw_the_text(self):
        for i in range(len(self.char_list)):
            self.char_list[i].draw(self.text[i])

    def draw(self):
        self.__update_char_style()
        self.__update_number_of_char()
        self.__update_char_positions()
        self.__draw_the_text()
