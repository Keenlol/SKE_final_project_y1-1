import turtle


class Paddle:
    def __init__(self, size, color, thickness=10, x=0, y=0):
        self._width = size[0]
        self._height = size[1]
        self._x = x
        self._y = y
        self._angle_deg = 0
        self._color = color
        self.__thickness = thickness
        turtle.penup()
        turtle.setheading(0)
        turtle.hideturtle()

    @property
    def pos(self):
        return self._x, self._y

    @pos.setter
    def pos(self, pos):
        self._x = pos[0]
        self._y = pos[1]
        turtle.goto(self._x, self._y)

    def draw(self):
        turtle.color(self._color)
        turtle.pensize(self.__thickness)
        turtle.goto(self._x, self._y)
        turtle.setheading(self._angle_deg)
        turtle.forward(self._width/2)
        turtle.pendown()
        turtle.begin_fill()
        turtle.left(90)
        for _ in range(2):
            turtle.forward(self._height/2)
            turtle.left(90)
            turtle.forward(self._width)
            turtle.left(90)
            turtle.forward(self._height/2)
        turtle.end_fill()
        turtle.penup()
        turtle.goto(self._x, self._y)

    def __str__(self):
        return f"paddle ({self._x:.2f}, {self._y:.2f}) a: {self._angle_deg}*"
