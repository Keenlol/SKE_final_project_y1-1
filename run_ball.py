from ball import Ball
from my_event import Event
from player import Player
from number import Number
import turtle
import random
import heapq

class BouncingSimulator:
    def __init__(self, num_balls):
        self.num_balls = num_balls
        self.ball_list = []
        self.player_list = []
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

        ball_radius = [20, 40]
        for i in range(self.num_balls):
            ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.ball_list.append(Ball(ball_radius, ball_color, i, self.canvas_width, self.canvas_height))

        # self.my_paddle = Paddle(200, 50, (255, 0, 0))
        # self.my_paddle.set_location([0, -50])

        player1 = Player(id=1, color="red", width=10, height=150, pos=[-400, 0], canvas_info=[self.canvas_width, self.canvas_height])
        player2 = Player(id=2, color="blue", width=10, height=150, pos=[400, 0], canvas_info=[self.canvas_width, self.canvas_height])
        self.player_list = [player1, player2]

        thickness = 20
        digit_size = [30,70]
        spacing = 30
        ui_score1 = Number(pos=[-600,0], digit_size=digit_size, color=("red"), thickness=thickness, spacing=spacing)
        ui_score2 = Number(pos=[600,0], digit_size=digit_size, color=("blue"), thickness=thickness, spacing=spacing)
        self.ui_score_list = [ui_score1, ui_score2]
        self.screen = turtle.Screen()

    # updates priority queue with all new events for a_ball
    def __predict(self, a_ball):
        if a_ball is None:
            return

        # particle-particle collisions
        for i in range(len(self.ball_list)):
            dt = a_ball.time_to_hit(self.ball_list[i])
            # insert this event into pq
            heapq.heappush(self.pq, Event(self.t + dt, a_ball, self.ball_list[i], None, None))
        
        # particle-wall collisions
        dtX = a_ball.time_to_leave_border()
        dtY = a_ball.time_to_hit_horizontal_wall()
        heapq.heappush(self.pq, Event(self.t + dtX, a_ball, None, None, None))
        heapq.heappush(self.pq, Event(self.t + dtY, None, a_ball, None, None))
    
    def __draw_border(self, line_thickness ,color_normal, color_left, color_right, n_interval):
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(line_thickness)
        turtle.setheading(0)

        for color_i in [color_left, color_right]:
            turtle.pendown()
            turtle.color(color_normal)
            turtle.forward(2*self.canvas_width)
            turtle.left(90)
            turtle.color(color_i)
            for i in range(1, n_interval+1):
                if i % 2 == 1:
                    turtle.pendown()
                    turtle.forward(2*self.canvas_height/n_interval)
                    turtle.penup()
                else:
                    turtle.forward(2*self.canvas_height/n_interval)
            turtle.left(90)
        turtle.penup()

    def __redraw(self):
        turtle.clear()
        for a_player in self.player_list:
            a_player.clear()

        self.__draw_border(line_thickness=10, 
                           color_normal="black", 
                           color_left=(150, 150, 255), 
                           color_right=(255, 150, 150),
                           n_interval=15)
                        

        for i in range(len(self.player_list)):
            self.player_list[i].draw()
            self.ui_score_list[i].draw(self.player_list[i].score)
        for a_ball in self.ball_list:
            a_ball.draw()

        turtle.update()
        heapq.heappush(self.pq, Event(self.t + 1.0/self.HZ, None, None, None, None))

    def __paddle_predict(self):
        for a_player in self.player_list:
            for a_ball in self.ball_list:
                dtPX = a_ball.time_to_hit_paddle_vertical(a_player)
                dtPY = a_ball.time_to_hit_paddle_horizontal(a_player)
                heapq.heappush(self.pq, Event(self.t + dtPX, a_ball, None, a_player, [a_player.x, a_player.y]))
                heapq.heappush(self.pq, Event(self.t + dtPY, a_ball, None, a_player, [a_player.x, a_player.y]))

    def run(self):
        # initialize pq with collision events and redraw event
        for i in range(len(self.ball_list)):
            self.__predict(self.ball_list[i])
        heapq.heappush(self.pq, Event(0, None, None, None, None))

        # listen to keyboard events and activate move_left and move_right handlers accordingly
        for a_player in self.player_list:
            a_player.get_input(self.screen)

        while (True):
            current_event = heapq.heappop(self.pq)
            if not current_event.is_valid():
                continue
            print(current_event)

            ball_a = current_event.a
            ball_b = current_event.b
            paddle_a = current_event.paddle
            paddle_a_pos_snapshot = current_event.paddle_pos_snapshot

            # update positions, and then simulation clock
            for i in range(len(self.ball_list)):
                self.ball_list[i].move(current_event.time - self.t)
            self.t = current_event.time

            if (ball_a is not None) and (ball_b is not None) and (paddle_a is None):
                ball_a.bounce_off(ball_b)
            elif (ball_a is not None) and (ball_b is None) and (paddle_a is None):
                if ball_a.x < 0:
                    self.player_list[1].score += 1
                if ball_a.x > 0:
                    self.player_list[0].score += 1
                ball_a.respawn()
            elif (ball_a is None) and (ball_b is not None) and (paddle_a is None):
                ball_b.bounce_off_horizontal_wall()
            elif (ball_a is None) and (ball_b is None) and (paddle_a is None):
                self.__redraw()
            elif (ball_a is not None) and (ball_b is None) and (paddle_a is not None):
                ball_a.bounce_off_paddle(paddle_a, paddle_a_pos_snapshot)

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
