from ball import Ball
from my_event import Event
from paddle import Paddle
from player import Player
import turtle
import random
import heapq

class BouncingSimulator:
    def __init__(self, num_balls):
        self.num_balls = num_balls
        self.ball_list = []
        self.t = 0.0
        self.pq = []
        self.HZ = 4
        turtle.speed(0)
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)
        self.canvas_width = turtle.screensize()[0] + 100
        self.canvas_height = turtle.screensize()[1]
        print(self.canvas_width, self.canvas_height)

        ball_radius = 0.05 * self.canvas_width
        for i in range(self.num_balls):
            x = -self.canvas_width + (i+1)*(2*self.canvas_width/(self.num_balls+1))
            y = 0.0
            vx = 10*random.uniform(-1.0, 1.0)
            vy = 10*random.uniform(-1.0, 1.0)
            ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.ball_list.append(Ball(ball_radius, x, y, vx, vy, ball_color, i))

        # self.my_paddle = Paddle(200, 50, (255, 0, 0))
        # self.my_paddle.set_location([0, -50])

        self.player1 = Player(id=1, color="red", width=10, height=150, pos=[-400, 0], canvas_height=self.canvas_height)
        self.player2 = Player(id=2, color="blue", width=10, height=150, pos=[400, 0], canvas_height=self.canvas_height)
        self.screen = turtle.Screen()

    # updates priority queue with all new events for a_ball
    def __predict(self, a_ball):
        if a_ball is None:
            return

        # particle-particle collisions
        for i in range(len(self.ball_list)):
            dt = a_ball.time_to_hit(self.ball_list[i])
            # insert this event into pq
            heapq.heappush(self.pq, Event(self.t + dt, a_ball, self.ball_list[i], None))
        
        # particle-wall collisions
        dtX = a_ball.time_to_hit_vertical_wall()
        dtY = a_ball.time_to_hit_horizontal_wall()
        heapq.heappush(self.pq, Event(self.t + dtX, a_ball, None, None))
        heapq.heappush(self.pq, Event(self.t + dtY, None, a_ball, None))
    
    def __draw_border(self):
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(10)
        turtle.setheading(0)
        turtle.pendown()
        turtle.color((0, 0, 0))
        for i in range(2):
            turtle.forward(2*self.canvas_width)
            turtle.left(90)
            turtle.forward(2*self.canvas_height)
            turtle.left(90)
        turtle.penup()

    def __redraw(self):
        turtle.clear()
        self.player1.clear()
        self.player2.clear()
        self.__draw_border()
        self.player1.draw()
        self.player2.draw()
        for i in range(len(self.ball_list)):
            self.ball_list[i].draw()
        turtle.update()
        heapq.heappush(self.pq, Event(self.t + 1.0/self.HZ, None, None, None))

    def __paddle_predict(self):
        for i in range(len(self.ball_list)):
            a_ball = self.ball_list[i]
            dtP = a_ball.time_to_hit_paddle(self.player1)
            heapq.heappush(self.pq, Event(self.t + dtP, a_ball, None, self.player1))

    # move_left and move_right handlers update paddle positions
    # def move_left(self):
    #     if (self.my_paddle.x - self.my_paddle.width/2 - 40) >= -self.canvas_width:
    #         self.my_paddle.set_location([self.my_paddle.x - 40, self.my_paddle.y])

    # # move_left and move_right handlers update paddle positions
    # def move_right(self):
    #     if (self.my_paddle.x + self.my_paddle.width/2 + 40) <= self.canvas_width:
    #         self.my_paddle.set_location([self.my_paddle.x + 40, self.my_paddle.y])

    def run(self):
        # initialize pq with collision events and redraw event
        for i in range(len(self.ball_list)):
            self.__predict(self.ball_list[i])
        heapq.heappush(self.pq, Event(0, None, None, None))

        # listen to keyboard events and activate move_left and move_right handlers accordingly
        self.player1.get_input(self.screen)
        self.player2.get_input(self.screen)
        # self.screen.listen()
        # self.screen.onkey(self.move_left, "Left")
        # self.screen.onkey(self.move_right, "Right")

        while (True):
            e = heapq.heappop(self.pq)
            if not e.is_valid():
                continue

            ball_a = e.a
            ball_b = e.b
            paddle_a = e.paddle

            # update positions, and then simulation clock
            for i in range(len(self.ball_list)):
                self.ball_list[i].move(e.time - self.t)
            self.t = e.time

            if (ball_a is not None) and (ball_b is not None) and (paddle_a is None):
                ball_a.bounce_off(ball_b)
            elif (ball_a is not None) and (ball_b is None) and (paddle_a is None):
                ball_a.bounce_off_vertical_wall()
            elif (ball_a is None) and (ball_b is not None) and (paddle_a is None):
                ball_b.bounce_off_horizontal_wall()
            elif (ball_a is None) and (ball_b is None) and (paddle_a is None):
                self.__redraw()
            elif (ball_a is not None) and (ball_b is None) and (paddle_a is not None):
                ball_a.bounce_off_paddle()

            self.__predict(ball_a)
            self.__predict(ball_b)

            # regularly update the prediction for the paddle as its position may always be changing due to keyboard events
            self.__paddle_predict()


        # hold the window; close it by clicking the window close 'x' mark
        turtle.done()

# num_balls = int(input("Number of balls to simulate: "))
num_balls = 2
my_simulator = BouncingSimulator(num_balls)
my_simulator.run()
