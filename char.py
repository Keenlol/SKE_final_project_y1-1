import turtle


class Char:
    def __init__(self, pos, width, height, color, thickness) -> None:
        self._color = color
        self._thickness = thickness
        self._width = width
        self._height = height
        self.pos = pos
        self.__draw_seq = {"0": [6, 0, 2, 8, 6],
                           "1": [3, 1, 7],
                           "2": [3, 0, 2, 5, 6, 8],
                           "3": [0, 2, 4, 5, 8, 6],
                           "4": [1, 3, 5, 2, 8],
                           "5": [2, 0, 3, 5, 8, 6],
                           "6": [2, 0, 6, 8, 5, 3],
                           "7": [0, 2, 7],
                           "8": [6, 0, 2, 8, 6, 3, 5],
                           "9": [5, 3, 0, 2, 8, 6],
                           "A": [6, 3, 1, 5, 8, 5, 3],
                           "B": [0, 6, 8, 5, 4, 2, 0],
                           "C": [2, 0, 6, 8],
                           "D": [0, 6, 7, 5, 1, 0],
                           "E": [2, 0, 3, 5, 3, 6, 8],
                           "F": [2, 0, 3, 4, 3, 6],
                           "G": [2, 0, 6, 8, 5, 4],
                           "H": [0, 6, 3, 5, 8, 2],
                           "I": [0, 2, 1, 7, 6, 8],
                           "J": [0, 2, 1, 7, 6, 3],
                           "K": [0, 6, 3, 2, 3, 8],
                           "L": [0, 6, 8],
                           "M": [6, 0, 4, 2, 8],
                           "N": [6, 0, 8, 2],
                           "O": [0, 2, 8, 6, 0],
                           "P": [6, 0, 2, 5, 3],
                           "Q": [8, 4, 5, 2, 0, 6, 7, 5],
                           "R": [6, 0, 2, 5, 3, 4, 8],
                           "S": [2, 1, 3, 5, 8, 6],
                           "T": [0, 2, 1, 7],
                           "U": [0, 6, 8, 2],
                           "V": [0, 7, 2],
                           "W": [0, 6, 4, 8, 2],
                           "X": [0, 8, 4, 2, 6],
                           "Y": [0, 4, 2, 4, 7],
                           "Z": [0, 2, 6, 8],
                           " ": [],
                           "_": [6, 8]}

    @property
    def pos(self):
        return self._x, self._y

    @pos.setter
    def pos(self, pos):
        self._x = pos[0]
        self._y = pos[1]

        dx = self._width/2
        dy = self._height/2

        self._grid_points = [[self._x-dx, self._y+dy], [self._x, self._y+dy], [self._x+dx, self._y+dy],
                             [self._x-dx, self._y], [self._x,
                                                     self._y], [self._x+dx, self._y],
                             [self._x-dx, self._y-dy], [self._x, self._y-dy], [self._x+dx, self._y-dy]]

    def draw(self, char):
        turtle.penup()
        turtle.color(self._color)
        turtle.pensize(self._thickness)
        turtle.goto(self._x, self._y)
        turtle.setheading(0)

        sequence = self.__draw_seq[char]
        if not sequence == []:
            turtle.goto(self._grid_points[sequence[0]]
                        [0], self._grid_points[sequence[0]][1])
            turtle.pendown()
            for i in range(1, len(sequence)):
                turtle.goto(
                    self._grid_points[sequence[i]][0], self._grid_points[sequence[i]][1])
            turtle.penup()

    def __str__(self) -> str:
        return f"digit pos=({self._x:.2f}, {self._y:.2f})"
