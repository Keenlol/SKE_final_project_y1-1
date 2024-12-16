""" Module providing Text class for displaying muliple alphanumeric characters"""

import copy
from char import Char

class Text:
    """
    Represents a string of characters that can be drawn using the Char class.
    
    This class manages multiple Char objects to display text strings, handling
    positioning, spacing, and updates of the characters.

    Attributes:
        _text (str): The text string to display (converted to uppercase)
        _spacing (float): Space between characters
        _x (float): X position of text center
        _y (float): Y position of text center
        _char_width (float): Width of each character
        _char_height (float): Height of each character
        _thickness (int): Line thickness for drawing
        _color (tuple): RGB color of the text
        _char_list (list): List of Char objects making up the text
    """

    def __init__(self, text: str,
                 pos: list,
                 char_size: float,
                 color: tuple,
                 thickness: float,
                 spacing: float,
                 ) -> None:
        """
        Initialize text object with given parameters.

        Args:
            text (str): Text string to display
            pos (list): [x, y] position of text center
            char_size (list): [width, height] of each character
            color (tuple): RGB color for drawing
            thickness (int): Line thickness for drawing
            spacing (float): Space between characters
        """
        self._text = text.upper()
        self._spacing = spacing
        self._x = pos[0]
        self._y = pos[1]
        self._char_width = char_size[0]
        self._char_height = char_size[1]
        self._thickness = thickness
        self._color = color
        self.__update_char_style()

    @property
    def text(self):
        """ Getter for text"""
        return self._text

    @text.setter
    def text(self, text):
        """ Setter for text"""
        self._text = text

    def __update_char_style(self):
        """
        Initialize or update the character list with base character style.
        Creates first character with current style settings.
        """
        self._char_list = [Char(pos=[self._x, self._y],
                                size=[self._char_width, self._char_height],
                                color=self._color,
                                thickness=self._thickness)]

    def __update_number_of_char(self):
        """
        Adjust the number of Char objects to match the length of the text.
        Adds or removes characters as needed by copying the style of the first character.
        """
        diff = len(self._char_list) - len(self._text)
        if diff < 0:
            # Add more characters if needed
            for _ in range(-diff):
                more_char = copy.deepcopy(self._char_list[0])
                self._char_list.append(more_char)
        elif diff > 0:
            # Remove excess characters if needed
            for _ in range(diff):
                self._char_list.pop()

    def __update_char_positions(self):
        """
        Update the positions of all characters to maintain proper spacing.
        Centers the text around the initial position.
        """
        center_diff = self._spacing + self._char_width
        n_char = len(self._char_list)

        # Calculate starting x position to center the text
        starting_x = self._x - (((n_char)/2) - 0.5) * center_diff

        # Update position of each character
        for i, char in enumerate(self._char_list):
            char.pos = [starting_x + (center_diff * i), self._y]

    def __draw_the_text(self):
        """
        Draw each character in the text string using the corresponding Char object.
        """
        for i, char in enumerate(self._char_list):
            char.draw(self._text[i])

    def draw(self):
        """
        Main drawing method that updates and draws the complete text string.
        Handles character creation, positioning, and drawing in sequence.
        """
        self.__update_char_style()
        self.__update_number_of_char()
        self.__update_char_positions()
        self.__draw_the_text()
