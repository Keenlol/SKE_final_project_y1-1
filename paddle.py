""" Module providing paddle class"""

from turtle import Turtle


class Paddle:
    """
    Represents a paddle in the game that can be positioned and rotated.
    
    This class handles the basic paddle functionality including drawing
    and positioning. It serves as the base class for the Player class.

    Attributes:
        _width (float): Width of the paddle
        _height (float): Height of the paddle
        _x (float): X position of paddle center
        _y (float): Y position of paddle center
        _angle_deg (float): Rotation angle in degrees
        _color (tuple): RGB color of the paddle
        __thickness (int): Line thickness for drawing
    """

    def __init__(self, my_turtle: Turtle,
                 color: tuple,
                 size: list,
                 thickness: float=10,
                 pos: list=None):
        """
        Initialize paddle with given parameters.

        Args:
            size (list): [width, height] of the paddle
            color (tuple): RGB color for drawing
            thickness (int, optional): Line thickness. Defaults to 10.
            pos (list, optional): [x, y] position. Defaults to [0, 0]
        """
        if pos is None:
            pos = [0, 0]

        self._width = size[0]
        self._height = size[1]
        self.pos = pos
        self._angle_deg = 0
        self._color = color
        self.__thickness = thickness
        self._my_turtle = my_turtle
        self._my_turtle.penup()
        self._my_turtle.setheading(0)

    @property
    def pos(self):
        """ Position getter, quicker way to get the position"""
        return self._x, self._y

    @pos.setter
    def pos(self, pos):
        """
        Position setter

        Args:
            pos (list): [x, y] new position
        """
        self._x = pos[0]
        self._y = pos[1]
        self._my_turtle.goto(self._x, self._y)

    @property
    def x(self):
        """X position setter"""
        return self._x

    @x.setter
    def x(self, x):
        """X position setter"""
        self._x = x

    @property
    def y(self):
        """Y position getter"""
        return self._y

    @y.setter
    def y(self, y):
        """Y position setter"""
        self._y = y

    @property
    def angle_deg(self):
        """Paddle's angle getter, in degrees."""
        return self._angle_deg

    @angle_deg.setter
    def angle_deg(self, angle):
        """Paddle's angle setter, in degrees."""
        self._angle_deg = angle

    @property
    def width(self):
        """Paddle's width getter."""
        return self._width

    @property
    def height(self):
        """Paddle's height getter."""
        return self._height

    @property
    def color(self):
        """ Getter for color"""
        return self._color

    def draw(self):
        """
        Draw the paddle using turtle graphics.
        
        Draws a rectangular paddle centered at its position with the current
        rotation angle. The paddle is filled with its color.
        """
        self._my_turtle.color(self._color)
        self._my_turtle.pensize(self.__thickness)
        self._my_turtle.goto(self._x, self._y)
        self._my_turtle.setheading(self._angle_deg)

        # Move to starting position
        self._my_turtle.forward(self._width/2)
        self._my_turtle.pendown()
        self._my_turtle.begin_fill()

        # Draw rectangle
        self._my_turtle.left(90)
        for _ in range(2):
            self._my_turtle.forward(self._height/2)
            self._my_turtle.left(90)
            self._my_turtle.forward(self._width)
            self._my_turtle.left(90)
            self._my_turtle.forward(self._height/2)

        self._my_turtle.end_fill()
        self._my_turtle.penup()
        self._my_turtle.goto(self._x, self._y)

    def __str__(self):
        return f"paddle ({self._x:.2f}, {self._y:.2f}) a: {self._angle_deg}*"
