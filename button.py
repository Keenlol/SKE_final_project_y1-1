""" Module providing the Button class for handling clickable buttons"""


import turtle
from text import Text


class Button(Text):
    """
    Represents a clickable button with text and hover effects.
    Inherits from Text class to handle text rendering.

    Attributes:
        _hover_color (tuple): RGB color when mouse hovers over button
        _idle_color (tuple): RGB color when button is not hovered
        _extra_size (float): Additional size for hit detection area
    """

    def __init__(self, text: str,
                 pos: list,
                 char_size: list,
                 idle_color: tuple,
                 thickness: int,
                 spacing: float,
                 hover_color: tuple) -> None:
        """
        Initialize button with given parameters.

        Args:
            text (str): Text to display on button
            pos (list): [x, y] position of button center
            char_size (list): [width, height] of each character
            idle_color (tuple): RGB color when not hovered
            thickness (int): Line thickness for drawing
            spacing (float): Space between characters
            hover_color (tuple): RGB color when hovered
        """
        super().__init__(text, pos, char_size, idle_color, thickness, spacing)
        self._hover_color = hover_color
        self._idle_color = idle_color
        self._color = self._idle_color

    def __get_cursor_pos(self):
        """
        Get the current cursor position relative to the game window.

        Returns:
            tuple: (x, y) coordinates of cursor position
        """
        screen = turtle.Screen()
        # Get cursor position relative to window
        cursor_x = screen.getcanvas().winfo_pointerx() - screen.getcanvas().winfo_rootx()
        cursor_y = screen.getcanvas().winfo_pointery() - screen.getcanvas().winfo_rooty()

        # Convert to turtle coordinates (centered at origin)
        cursor_x = cursor_x - screen.window_width() // 2
        cursor_y = screen.window_height() // 2 - cursor_y

        return cursor_x, cursor_y

    def is_hovered(self, x: float, y: float):
        """
        Check if given coordinates are within button's bounds.

        Args:
            x (float): X coordinate to check
            y (float): Y coordinate to check

        Returns:
            bool: True if coordinates are within button bounds, False otherwise
        """
        # Calculate button boundaries using first and last characters
        bottom_right = [self._char_list[0].grid_points[8][0],
                       self._char_list[0].grid_points[8][1]]
        top_left = [self._char_list[-1].grid_points[0][0],
                   self._char_list[-1].grid_points[0][1]]

        return bottom_right[0] <= x <= top_left[0] and bottom_right[1] <= y <= top_left[1]

    def active(self):
        """
        Update button state based on cursor position and redraw.
        Changes color when hovered over.
        """
        cursor_x, cursor_y = self.__get_cursor_pos()

        # Update color based on hover state
        if self.is_hovered(cursor_x, cursor_y):
            self._color = self._hover_color
        else:
            self._color = self._idle_color

        self.draw()
