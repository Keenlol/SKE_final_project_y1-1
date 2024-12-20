""" Module providing player class"""

from paddle import Paddle

class Player(Paddle):
    """
    Represents a player in the game, extending the Paddle class with input handling
    and movement capabilities.
    
    This class adds player-specific functionality including keyboard input handling,
    movement, scoring, and paddle tilting mechanics.

    Attributes:
        # _name (str) <<GET>>: Player name
        # _uid (int) <<GET>>: Unique player identifier (1 or 2)
        # _score (int) <<GET, SET>>: Current player score
        # _max_tilt_angle_deg (float): Maximum tilt angle in degrees (unsigned)
        # _target_angle_deg (float): Target angle for smooth rotation (signed)
        # _target_y (float): Target Y position for smooth movement
        - __dist_per_move (float): Distance to move per key press
        - __border_height (float): Height of game border
        - __input_set (Dict): A dict containing cotrols for both players

    Methods:
        + get_input(Screen): Set up keyboard event listeners for player controls
        # _move_up(): Move paddle upward if within border limits
        # _move_down(): Move paddle downward if within border limits
        # _tilt_cw(): Set target angle for clockwise rotation
        # _tilt_ccw(): Set target angle for counter-clockwise rotation
        # _tilt_reset(): Reset target angle to zero
        + update_angle(): Update paddle angle with smooth rotation
        + update_position(): Update paddle position with smooth movement
        - __initailize_input_set(): Initialize keyboard controls based on player ID
    """

    def __init__(self, name: str,
                 uid: int,
                 color: tuple,
                 size: float,
                 pos: list,
                 border_height: float):
        """
        Initialize player with given parameters.

        Args:
            name (str): Player name
            id (int): Player identifier (1 or 2)
            color (tuple): RGB color for paddle
            size (list): [width, height] of paddle
            pos (list): [x, y] initial position
            border_height (float): Height of game border
        """
        super().__init__(color, size)
        self._name = name
        self._uid = uid
        self._score = 0
        self.__border_height = border_height
        self.__initailize_input_set()

        self._x = pos[0]
        self._y = pos[1]
        self._max_tilt_angle_deg = 40
        self._target_angle_deg = 0
        self.__dist_per_move = self._height*0.8
        self._target_y = self._y

    @property
    def name(self) -> str:
        """ Player's name Getter."""
        return self._name

    @property
    def uid(self) -> int:
        """ Player's unique identifier getter"""
        return self._uid

    @property
    def score(self) -> int:
        """ PLayer's score Getter"""
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        """ PLayer's score Setter"""
        self._score = value

    def __initailize_input_set(self):
        """
        Initialize keyboard controls based on player ID.
        Player 1 uses WASD, Player 2 uses arrow keys.
        """
        if self._uid == 1:
            self.__input_set = {"move_up": "w",
                              "move_down": "s",
                              "tilt_cw": "d",
                              "tilt_ccw": "a"}
        elif self._uid == 2:
            self.__input_set = {"move_up": "Up",
                              "move_down": "Down",
                              "tilt_cw": "Right",
                              "tilt_ccw": "Left"}

    def get_input(self, my_screen):
        """
        Set up keyboard event listeners for player controls.

        Args:
            screen (Screen): Game screen for input binding
        """
        my_screen.listen()
        my_screen.onkeypress(self._move_up, self.__input_set["move_up"])
        my_screen.onkeypress(self._move_down, self.__input_set["move_down"])
        my_screen.onkeypress(self._tilt_cw, self.__input_set["tilt_cw"])
        my_screen.onkeypress(self._tilt_ccw, self.__input_set["tilt_ccw"])

        my_screen.onkeyrelease(self._tilt_reset, self.__input_set["tilt_cw"])
        my_screen.onkeyrelease(self._tilt_reset, self.__input_set["tilt_ccw"])

    def _move_up(self):
        """
        Move paddle upward if within border limits.
        Updates target Y position for smooth movement.
        """
        if self._target_y < self.__border_height/2:
            self._target_y += self.__dist_per_move

    def _move_down(self):
        """
        Move paddle downward if within border limits.
        Updates target Y position for smooth movement.
        """
        if self._target_y > -self.__border_height/2:
            self._target_y -= self.__dist_per_move

    def _tilt_cw(self):
        """Set target angle for clockwise rotation."""
        self._target_angle_deg = -self._max_tilt_angle_deg

    def _tilt_ccw(self):
        """Set target angle for counter-clockwise rotation."""
        self._target_angle_deg = self._max_tilt_angle_deg

    def _tilt_reset(self):
        """Reset target angle to zero (vertical position)."""
        self._target_angle_deg = 0

    def update_position(self):
        """
        Update paddle position with smooth movement towards target position.
        Uses interpolation for smooth motion.
        """
        dy = self._target_y - self._y
        self.pos = [self._x, self._y + 0.3 * dy]

    def update_angle(self):
        """
        Update paddle angle with smooth rotation towards target angle.
        Uses interpolation for smooth rotation.
        """
        d_angle = self._target_angle_deg - self._angle_deg
        self._angle_deg = self._angle_deg + d_angle * 0.3
