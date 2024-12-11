import turtle
import copy
from digit import Digit

class Number:
    def __init__(self, pos, digit_size, color, thickness, spacing) -> None:
        self.number = 0
        self.offset = spacing
        self.x = pos[0]
        self.y = pos[1]
        self.digit_width = digit_size[0]
        self.digit_height = digit_size[1]
        self.digit_list = [Digit(pos, self.digit_width, self.digit_height, color, thickness)]

    def __update_number_of_digit(self):
        n_digit = 0
        tmp = self.number
        while tmp >= 0:
            tmp %= 10
            n_digit += 1
        
        diff = len(self.digit_list) - n_digit
        if diff < 0:
            for _ in range(-diff):
                more_digit = copy.deepcopy(self.digit_list[0])
                self.digit_list.append(more_digit)
        elif diff > 0:
            for _ in range(diff):
                self.digit_list.pop()

    def __update_digit_positions(self):
        center_diff = self.offset + self.digit_width/2
        n_digit = len(self.digit_list)


        if n_digit % 2 == 1:
            starting_x = (self.x - (n_digit)/2 * center_diff )
            for i in range(len(self.digit_list)):
                self.digit_list[i].x = starting_x + (center_diff * i)
        else:
            starting_x = self.x - ((((n_digit)/2) - 0.5) * center_diff ) 
            for i in range(len(self.digit_list)):
                self.digit_list[i].x = starting_x + (center_diff * i)

    def __update_the_digit(self):

    def update(self):
        self.__update_number_of_digit()
        