""" Module providing a Char class for handling sigular alphanumeric character"""

import turtle

class Char:
    """
    Represents a single character that can be drawn using turtle graphics.
    
    This class handles the drawing of alphanumeric characters using a grid-based system
    where each character is drawn by connecting points on a 3x3 grid.

    The grid and its represnting number:
    0   1   2
    3   4   5
    6   7   8

    Attributes:
        + pos (list) <<GET, SET>>: [x, y] position in the form of list
        # _color (tuple): RGB color of the character
        # _thickness (int): Line thickness for drawing
        # _width (float) <<GET, SET>>: Width of the character
        # _height (float) <<GET, SET>>: Height of the character
        # _x (float): X position of character center
        # _y (float): Y position of character center
        # _grid_points (list) <<GET>>: a list containing position of each point of the grid
    """
    def __init__(self, pos: list,
                 size: list,
                 color: tuple,
                 thickness: float) -> None:
        """
        Initialize a charater with given parameters.

        Args:
            pos (list): [x ,y] Position of the character from the middle 
            size (list): [width, height] Size of the character
            color (tuple): color of the character
            thickness (float): thickness of the line used in drawing the character
        """
        self._color = color
        self._thickness = thickness
        self._width = size[0]
        self._height = size[1]
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
        """
        Get the position of the character.

        Returns:
            tuple: (x, y) coordinates of character center
        """
        return self._x, self._y

    @pos.setter
    def pos(self, pos: list):
        """
        Set the position of the character and update grid points.

        Args:
            pos (list): [x, y] new position
        """
        x = self._x = pos[0]
        y = self._y = pos[1]

        dx = self._width/2
        dy = self._height/2

        # Calculate 3x3 grid points relative to character center with the given width and height
        self._grid_points = [[x-dx, y+dy], [x, y+dy], [x+dx, y+dy],
                             [x-dx, y], [x, y], [x+dx, y],
                             [x-dx, y-dy], [x, y-dy], [x+dx, y-dy]]

    @property
    def width(self):
        """Getter for character's width"""
        return self._width

    @width.setter
    def width(self, width):
        """Setter for character's width"""
        self._width = width

    @property
    def height(self):
        """Getter for character's height"""
        return self._height

    @height.setter
    def height(self, height):
        """Setter for character's height"""
        self._width = height

    @property
    def grid_points(self):
        """ 
        Getter for grid points
        
        Return:
            list: a list containg 9 positions of all the point of the grid"""
        return self._grid_points

    def draw(self, char: str):
        """
        Draw the specified character using turtle graphics.

        Args:
            char (str): Single character to draw
        """
        turtle.penup()
        turtle.color(self._color)
        turtle.pensize(self._thickness)
        turtle.goto(self._x, self._y)
        turtle.setheading(0)


        sequence = self.__draw_seq[char]

        if not sequence == []:
            # Move to first point without drawing
            turtle.goto(self._grid_points[sequence[0]][0],
                        self._grid_points[sequence[0]][1])
            turtle.pendown()
            # Connect remaining points with lines
            for i in range(1, len(sequence)):
                turtle.goto(
                    self._grid_points[sequence[i]][0],
                    self._grid_points[sequence[i]][1])
            turtle.penup()

    def __str__(self) -> str:
        return f"digit pos=({self._x:.2f}, {self._y:.2f})"
