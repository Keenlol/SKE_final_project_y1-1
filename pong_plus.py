from ball import Ball
from my_event import Event
from player import Player
from text import Text
from button import Button
import turtle, random, heapq

class PongPlus:
    def __init__(self, num_balls, player_names, player_colors, winning_score):
        self.num_balls = num_balls
        self.ball_list = []
        self.player_list = []
        self.player_names = player_names
        self.player_colors = player_colors
        self.t = 0.0
        self.pq = []
        self.HZ = 4
        self.winning_score = winning_score
        turtle.speed(0)
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)
        turtle.setup(width=1920, height=1080, startx=0, starty=0)
        self.canvas_width = turtle.screensize()[0] + 100
        self.canvas_height = turtle.screensize()[1]
        self.screen = turtle.Screen()

        self.__create_objects()


    def __create_objects(self):
        ball_radius = [20, 40]
        for i in range(self.num_balls):
            ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.ball_list.append(Ball(ball_radius, ball_color, i, self.canvas_width, self.canvas_height, 8))

        player1 = Player(name=self.player_names[0],id=1, color=self.player_colors[0], width=10, height=150, pos=[-420, 0], canvas_info=[self.canvas_width, self.canvas_height])
        player2 = Player(name=self.player_names[1], id=2, color=self.player_colors[1], width=10, height=150, pos=[420, 0], canvas_info=[self.canvas_width, self.canvas_height])
        self.player_list = [player1, player2]

        ui_score1 = Text(text=str(player1.score) ,pos=[-600,0], char_size=[30,70], color=self.player_colors[0], thickness=20, spacing=30)
        ui_score2 = Text(text=str(player1.score) ,pos=[600,0], char_size=[30,70], color=self.player_colors[1], thickness=20, spacing=30)
        self.ui_score_list = [ui_score1, ui_score2]


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

        for color_i in [color_right, color_left]:
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

        self.__draw_border(line_thickness=10, 
                           color_normal="black", 
                           color_left=self.player_colors[0], 
                           color_right=self.player_colors[1],
                           n_interval=15)
                        

        for i in range(len(self.player_list)):
            self.player_list[i].draw()
            self.ui_score_list[i].text = str(self.player_list[i].score)
            self.ui_score_list[i].draw()
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

    def __winning_screen(self):
        if self.player_list[0].score > self.player_list[1].score:
            color = self.player_list[0].color
            name = self.player_list[0].name
        else:
            color = self.player_list[1].color
            name = self.player_list[1].name

        ui_winning_text = Text(text=str(name+" WON") ,pos=[0,40], char_size=[40,90], color=color, thickness=20, spacing=30)
        ui_retry = Button(text="REMATCH",pos=[0,-70], char_size=[30,40], idle_color=(100,100,100), hover_color=(50,200,50), thickness=15, spacing=20)
        self.rematch = False

        def on_click(x, y):
            if ui_retry.is_hovered(x, y):
                self.rematch = True
                self.pq.clear()
                self.t = 0
                for a_ball in self.ball_list:
                    a_ball.respawn()
                for a_player in self.player_list:
                    a_player.score = 0
                self.play()

        turtle.onscreenclick(on_click)

        while self.rematch == False:
            turtle.clear()
            ui_retry.active()
            ui_winning_text.draw()
            turtle.update()

    def play(self):

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

            ball_a = current_event.a
            ball_b = current_event.b
            paddle_a = current_event.paddle
            paddle_a_pos_snapshot = current_event.paddle_pos_snapshot

            # update positions, and then simulation clock
            for i in range(len(self.ball_list)):
                self.ball_list[i].move(current_event.time - self.t)

            for a_player in self.player_list:
                a_player.update_position()
                a_player.update_angle()

            self.t = current_event.time    
        
            if (ball_a is not None) and (ball_b is not None) and (paddle_a is None):
                ball_a.bounce_off(ball_b)
            elif (ball_a is not None) and (ball_b is None) and (paddle_a is None):
                if ball_a.x < 0:
                    self.player_list[1].score += 1
                elif ball_a.x > 0:
                    self.player_list[0].score += 1
                if self.player_list[0].score >= self.winning_score or self.player_list[1].score >= self.winning_score:
                    break
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
        self.__winning_screen()
        turtle.bye()

        # hold the window; close it by clicking the window close 'x' mark
        turtle.done()

# num_balls = int(input("Number of balls to simulate: "))

