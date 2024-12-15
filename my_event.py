class Event:
    def __init__(self, time, ball_a, ball_b, paddle):
        self._time = time
        self._ball_a = ball_a
        self._ball_b = ball_b
        self._paddle = paddle

        if ball_a is not None:
            self._count_a = ball_a._count
        else:
            self._count_a = -1
        if ball_b is not None:
            self._count_b = ball_b._count
        else:
            self._count_b = -1

    def __lt__(self, that):
        return self._time < that._time

    def is_valid(self):
        if (self._ball_a is not None) and (self._ball_a._count != self._count_a):
            return False
        if (self._ball_b is not None) and (self._ball_b._count != self._count_b):
            return False
        return True
    
    def __str__(self) -> str:
        return f"time={self._time} | {self._ball_a} | {self._ball_b} | {self._paddle} |"
