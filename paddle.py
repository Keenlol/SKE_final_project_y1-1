import turtle


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

    def __init__(self, size, color, thickness=10, x=0, y=0):
        """
        Initialize paddle with given parameters.

        Args:
            size (list): [width, height] of the paddle
            color (tuple): RGB color for drawing
            thickness (int, optional): Line thickness. Defaults to 10.
            x (float, optional): Initial x position. Defaults to 0.
            y (float, optional): Initial y position. Defaults to 0.
        """
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
        """
        Get the current position of the paddle.

        Returns:
            tuple: (x, y) coordinates of paddle center
        """
        return self._x, self._y

    @pos.setter
    def pos(self, pos):
        """
        Set the position of the paddle.

        Args:
            pos (list): [x, y] new position
        """
        self._x = pos[0]
        self._y = pos[1]
        turtle.goto(self._x, self._y)

    def draw(self):
        """
        Draw the paddle using turtle graphics.
        
        Draws a rectangular paddle centered at its position with the current
        rotation angle. The paddle is filled with its color.
        """
        turtle.color(self._color)
        turtle.pensize(self.__thickness)
        turtle.goto(self._x, self._y)
        turtle.setheading(self._angle_deg)
        
        # Move to starting position
        turtle.forward(self._width/2)
        turtle.pendown()
        turtle.begin_fill()
        
        # Draw rectangle
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
