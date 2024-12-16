""" Module providing the central class for PongPlus game"""

import heapq, turtle

# from turtle import Turtle, Screen
from ball import Ball
from my_event import Event
from player import Player
from text import Text
from button import Button

class PongPlus:
    """
    Main game class that handles the Pong game logic and rendering.
    
    Attributes:
        _num_balls (int): Number of balls in play
        _ball_list (list): List of Ball objects
        _player_list (list): List of Player objects
        _player_names (list): List of player names
        _player_colors (list): List of RGB colors for players
        _t (float): Current simulation time
        _pq (list): Priority queue for event handling
        _HZ (int): Update frequency
        _winning_score (int): Score needed to win
        _base_ball_speed (float): Initial ball speed
    """

    def __init__(self, num_balls: int,
                 player_names: list,
                 player_colors: list,
                 winning_score: int,
                 ball_speed: float=8):
        """
        Args:
            num_balls (int): Number of balls in play
            player_names (list): List of player names, ex. [name1, name2]
            player_colors (list): List of RGB colors for players, ex. [(0,0,255), (0,255,0)]
            winning_score (int): Score needed to win
            ball_speed (float, optional): Initial ball speed. Defaults to 8.
        """
        # Screen setup
        self._screen = turtle.Screen()
        self._screen.colormode(255)

        # Create and setup turtle
        self._game_turtle = turtle.Turtle()
        self._game_turtle.getscreen().colormode(255)
        self._game_turtle.speed(0)
        self._game_turtle.hideturtle()
        self._screen.tracer(0)
        self._screen.delay(0)

        # Initialize other attributes
        self._num_balls = num_balls
        self._ball_list = []
        self._player_list = []
        self._player_names = player_names
        self._player_colors = player_colors
        self._t = 0.0
        self._pq = []
        self._hz = 4
        self._winning_score = winning_score
        self._base_ball_speed = ball_speed

        # Setup screen dimensions
        self._screen.setup(width=1920, height=1080, startx=0, starty=0)
        self._border_width = self._screen.window_width()//2 + 100
        self._border_height = self._screen.window_height()//2

        self._rematch = False

        self._create_objects()

    def _create_objects(self):
        """Create game objects including balls, players, and UI elements."""
        # initialize balls
        for i in range(self._num_balls):
            self._ball_list.append(Ball(
                size_range=[20, 40],
                uid=i,
                border_size=[self._border_width, self._border_height],
                base_speed=self._base_ball_speed,
                my_turtle=self._game_turtle
                ))

        # initialize player's paddles
        player1 = Player(
            uid=1,
            name=self._player_names[0],
            color=self._player_colors[0],
            size=[10, 150],
            pos=[-420, 0],
            border_height=self._border_height,
            my_turtle=self._game_turtle
            )
        player2 = Player(
            uid=2,
            name=self._player_names[1],
            color=self._player_colors[1],
            size=[10, 150],
            pos=[420, 0],
            border_height=self._border_height,
            my_turtle=self._game_turtle
            )
        self._player_list = [player1, player2]

        # initailize player's score ui
        ui_score1 = Text(
            text=str(player1.score),
            pos=[-600, 0],
            char_size=[30, 70],
            color=self._player_colors[0],
            thickness=20,
            spacing=30,
            my_turtle=self._game_turtle
            )
        ui_score2 = Text(
            text=str(player2.score),
            pos=[600, 0],
            char_size=[30, 70],
            color=self._player_colors[1],
            thickness=20,
            spacing=30,
            my_turtle=self._game_turtle
            )
        self.ui_score_list = [ui_score1, ui_score2]

        # initialize player's name ui
        ui_name1 = Text(
            text=player1.name,
            pos=[-600, -65],
            char_size=[10, 15],
            color=self._player_colors[0],
            thickness=4,
            spacing=5,
            my_turtle=self._game_turtle
            )
        ui_name2 = Text(
            text=player2.name,
            pos=[600, -65],
            char_size=[10, 15],
            color=self._player_colors[1],
            thickness=4,
            spacing=5,
            my_turtle=self._game_turtle
            )
        self.ui_name_list = [ui_name1, ui_name2]

    def __ball_predict(self, a_ball: Ball):
        """
        Predict future collisions for a given ball.

        Args:
            a_ball (Ball): Ball object to predict collisions for
        """
        if a_ball is None:
            return

        # particle-particle collisions
        for i in range(len(self._ball_list)):
            dt = a_ball.time_to_hit_ball(self._ball_list[i])
            # insert this event into pq
            heapq.heappush(self._pq, Event(
                self._t + dt, a_ball, self._ball_list[i], None))

        # particle-wall collisions
        dt_x = a_ball.time_to_leave_border()
        dt_y = a_ball.time_to_hit_horizontal_wall()
        heapq.heappush(self._pq, Event(self._t + dt_x, a_ball, None, None))
        heapq.heappush(self._pq, Event(self._t + dt_y, None, a_ball, None))

    def __draw_border(self, line_thickness: float,
                      color_normal: tuple,
                      color_left: tuple,
                      color_right: tuple,
                      n_interval: int):
        """
        Draw the game border.

        Args:
            line_thickness (float): Border line thickness
            color_normal (tuple): RGB color for horizontal borders
            color_left (tuple): RGB color for left border
            color_right (tuple): RGB color for right border
            n_interval (int): Number of dashed line intervals
        """
        self._game_turtle.penup()
        self._game_turtle.goto(-self._border_width, -self._border_height)
        self._game_turtle.pensize(line_thickness)
        self._game_turtle.setheading(0)

        # write the top/bottom border
        for color_i in [color_right, color_left]:
            self._game_turtle.pendown()
            self._game_turtle.color(color_normal)
            self._game_turtle.forward(2*self._border_width)
            self._game_turtle.left(90)
            self._game_turtle.color(color_i)

            # write the left/right border with dashed line
            for i in range(1, n_interval+1):
                if i % 2 == 1:
                    self._game_turtle.pendown()
                    self._game_turtle.forward(2*self._border_height/n_interval)
                    self._game_turtle.penup()
                else:
                    self._game_turtle.forward(2*self._border_height/n_interval)

            self._game_turtle.left(90)
        self._game_turtle.penup()

    def __redraw(self):
        """ Redraw everything"""
        self._screen.clear()

        self.__draw_border(line_thickness=10,
                           color_normal="black",
                           color_left=self._player_colors[0],
                           color_right=self._player_colors[1],
                           n_interval=15)

        # draw players and also their name and score
        for i in enumerate(self._player_list):
            self._player_list[i].draw()
            self.ui_score_list[i].text = str(self._player_list[i].score)
            self.ui_score_list[i].draw()
            self.ui_name_list[i].draw()

        # draw the balls
        for a_ball in self._ball_list:
            a_ball.draw()

        self._screen.update()
        heapq.heappush(self._pq, Event(
            self._t + 1.0/self._hz, None, None, None))

    def __paddle_predict(self):
        """
        predict the collision between the balls and paddles
        both vertically and horizontally.
        """
        for a_player in self._player_list:
            for a_ball in self._ball_list:
                dt_px = a_ball.time_to_hit_paddle_vertical(a_player)
                dt_py = a_ball.time_to_hit_paddle_horizontal(a_player)
                heapq.heappush(self._pq, Event(
                    self._t + dt_px, a_ball, None, a_player))
                heapq.heappush(self._pq, Event(
                    self._t + dt_py, a_ball, None, a_player))

    def __winning_screen(self):
        """Display and run the ending screen"""
        # set the display colors and name to the winning player
        if self._player_list[0].score > self._player_list[1].score:
            color = self._player_list[0].color
            name = self._player_list[0].name
        else:
            color = self._player_list[1].color
            name = self._player_list[1].name

        # initialize the ui(s)
        ui_winning_text = Text(text=str(name+" WON"),
                               pos=[0, 40],
                               char_size=[40, 90],
                               color=color,
                               thickness=20,
                               spacing=30,
                               my_turtle=self._game_turtle)

        ui_retry = Button(text="REMATCH",
                          pos=[0, -70],
                          char_size=[30, 40],
                          idle_color=(100, 100, 100),
                          hover_color=(50, 200, 50),
                          thickness=15,
                          spacing=20,
                          my_turtle=self._game_turtle,
                          my_screen=self._screen)

        self._rematch = False

        # reset the values and re-run the game if the "REMATCH" button is pressed
        def on_click(x, y):
            """ 
            a function for turtle to redirect to when the mouse is clicked.
            if the cursor overlap with the button when clicked then it restarts the game.
            """
            if ui_retry.is_hovered(x, y):
                self._rematch = True
                self._pq.clear()
                self._t = 0
                for a_ball in self._ball_list:
                    a_ball.respawn()
                for a_player in self._player_list:
                    a_player.score = 0
                self.play()

        # go to the function above if the mouse is clicked
        self._screen.onscreenclick(on_click)

        # keep drawing the ui if the rematch button hasn't been pressed
        while self._rematch is False:
            self._game_turtle.clear()
            ui_retry.active()
            ui_winning_text.draw()
            self._screen.update()

    def __adjust_hz(self):
        """
        Adjust the HZ based on the amount of character (mostly from player names) 
        on the screen to account for the lag it will cause.
        """
        total_char = 0

        for a_player in self._player_list:
            total_char += len(a_player.name)

        self._hz = 5 + total_char * (-0.1)

    def __playing_loop(self):
        """
        Main loop of the game, run all the interaction between objects.
        """
        while True:
            current_event = heapq.heappop(self._pq)
            if not current_event.is_valid():
                continue

            ball_a = current_event.ball_a
            ball_b = current_event.ball_b
            paddle_a = current_event.paddle
            player_1 = self._player_list[0]
            player_2 = self._player_list[1]
            # update positions, and then simulation clock
            for ball in self._ball_list:
                ball.move(current_event.time - self._t)

            for a_player in self._player_list:
                a_player.update_position()
                a_player.update_angle()

            self._t = current_event.time

            if (ball_a is not None) and (ball_b is not None) and (paddle_a is None):
                ball_a.bounce_off_ball(ball_b)
            elif (ball_a is not None) and (ball_b is None) and (paddle_a is None):
                # Detecting which side gain the score
                if ball_a.x < 0:
                    player_2.score += 1
                elif ball_a.x > 0:
                    player_1.score += 1
                # break and go to the winning screen if a player wins
                if player_1.score >= self._winning_score or player_2.score >= self._winning_score:
                    break
                ball_a.respawn()
            elif (ball_a is None) and (ball_b is not None) and (paddle_a is None):
                ball_b.bounce_off_horizontal_wall()
            elif (ball_a is None) and (ball_b is None) and (paddle_a is None):
                self.__redraw()
            elif (ball_a is not None) and (ball_b is None) and (paddle_a is not None):
                ball_a.bounce_off_paddle(paddle_a)

            # preedict the next collisions of the objects
            self.__ball_predict(ball_a)
            self.__ball_predict(ball_b)
            self.__paddle_predict()

    def play(self):
        """ Play PongPlus, setup and run the game"""
        self.__adjust_hz()
        # initialize pq with collision events and redraw event
        for i in range(len(self._ball_list)):
            self.__ball_predict(self._ball_list[i])
        heapq.heappush(self._pq, Event(0, None, None, None))

        # listen to keyboard events and make player moves
        for a_player in self._player_list:
            a_player.get_input(self._screen)

        # different phase of the game
        self.__playing_loop()
        self.__winning_screen()
        self._screen.bye()

        # hold the window; close it by clicking the window close 'x' mark
        self._screen.done()

# num_balls = int(input("Number of balls to simulate: "))
