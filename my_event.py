class Event:
    """
    A game event with timing information and involved objects.

    Attributes:
        _time (float): Time when the event occurs
        _ball_a (Ball): First ball involved in the event (or None)
        _ball_b (Ball): Second ball involved in the event (or None)
        _paddle (Paddle): Paddle involved in the event (or None)
        _count_a (int): Collision count of ball_a at event creation
        _count_b (int): Collision count of ball_b at event creation
    """

    def __init__(self, time, ball_a, ball_b, paddle):
        """
        Initialize an event with given parameters.

        Args:
            time (float): Time when the event occurs
            ball_a (Ball): First ball involved (or None)
            ball_b (Ball): Second ball involved (or None)
            paddle (Paddle): Paddle involved (or None)
        """
        self._time = time
        self._ball_a = ball_a
        self._ball_b = ball_b
        self._paddle = paddle

        # Store collision counts at event creation for validity checking
        if ball_a is not None:
            self._count_a = ball_a._count
        else:
            self._count_a = -1
        if ball_b is not None:
            self._count_b = ball_b._count
        else:
            self._count_b = -1

    def is_valid(self):
        """
        Check if the event is still valid.
        
        An event becomes invalid if either ball has experienced the predicted
        event since the event was created.

        Returns:
            bool: True if event is still valid, False otherwise
        """
        if (self._ball_a is not None) and (self._ball_a._count != self._count_a):
            return False
        if (self._ball_b is not None) and (self._ball_b._count != self._count_b):
            return False
        return True

    def __str__(self) -> str:
        """
        String representation of the event.

        Returns:
            str: Event details including time and involved objects
        """
        return f"time={self._time} | {self._ball_a} | {self._ball_b} | {self._paddle} |"

    def __lt__(self, that):
        """
        Compare events based on their time.
        Used for priority queue ordering of events.

        Args:
            that (Event): Another event to compare with

        Returns:
            bool: True if this event occurs before that event
        """
        return self._time < that._time
