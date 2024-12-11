class Event:
    def __init__(self, time, ball_a, ball_b, paddle, paddle_pos_snapshot):
        self.time = time
        self.a = ball_a
        self.b = ball_b
        self.paddle = paddle
        self.paddle_pos_snapshot = paddle_pos_snapshot

        if ball_a is not None:
            self.count_a = ball_a.count
        else:
            self.count_a = -1
        if ball_b is not None:
            self.count_b = ball_b.count
        else:
            self.count_b = -1

    def __lt__(self, that):
        return self.time < that.time

    def is_valid(self):
        if (self.a is not None) and (self.a.count != self.count_a):
            return False
        if (self.b is not None) and (self.b.count != self.count_b):
            return False
        return True
    
    def __str__(self) -> str:
        return f"time={self.time} | {self.a} | {self.b} | {self.paddle} |"
