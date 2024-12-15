from ball import Ball
from my_event import Event
from player import Player
from text import Text
from button import Button
import turtle
import heapq


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

    def __init__(self, num_balls, player_names, player_colors, winning_score, ball_speed=8):
        """
        Initialize the game with specified parameters.

        Args:
            num_balls (int): Number of balls in play
            player_names (list): List of player names
            player_colors (list): List of RGB colors for players
            winning_score (int): Score needed to win
            ball_speed (float, optional): Initial ball speed. Defaults to 8.
        """
        self._num_balls = num_balls
        self._ball_list = []
        self._player_list = []
        self._player_names = player_names
        self._player_colors = player_colors
        self._t = 0.0
        self._pq = []
        self._HZ = 4
        self._winning_score = winning_score
        self._base_ball_speed = ball_speed
        turtle.speed(0)
        turtle.tracer(0)
        turtle.delay(0)
        turtle.hideturtle()
        turtle.colormode(255)
        turtle.setup(width=1920, height=1080, startx=0, starty=0)
        self._border_width = turtle.screensize()[0] + 100
        self._border_height = turtle.screensize()[1]
        self._screen = turtle.Screen()

        self.__create_objects()

    def __create_objects(self):
        """Create game objects including balls, players, and UI elements."""
        # initialize balls
        for i in range(self._num_balls):
            self._ball_list.append(Ball(size_range=[20, 40], id=i, 
                                        border_size=[self._border_width, self._border_height], 
                                        base_speed=self._base_ball_speed))

        # initialize player's paddles
        player1 = Player(name=self._player_names[0], id=1, color=self._player_colors[0], 
                        size=[10, 150], pos=[-420, 0], border_height=self._border_height)
        player2 = Player(name=self._player_names[1], id=2, color=self._player_colors[1], 
                        size=[10, 150], pos=[420, 0], border_height=self._border_height)
        self._player_list = [player1, player2]

        # initailize player's score ui
        ui_score1 = Text(text=str(player1._score), pos=[-600, 0], char_size=[30, 70], 
                        color=self._player_colors[0], thickness=20, spacing=30)
        ui_score2 = Text(text=str(player2._score), pos=[600, 0], char_size=[30, 70], 
                        color=self._player_colors[1], thickness=20, spacing=30)
        self.ui_score_list = [ui_score1, ui_score2]

        # initialize player's name ui
        ui_name1 = Text(text=player1._name, pos=[-600, -65], char_size=[10, 15], 
                        color=self._player_colors[0], thickness=4, spacing=5)
        ui_name2 = Text(text=player2._name, pos=[600, -65], char_size=[10, 15], 
                        color=self._player_colors[1], thickness=4, spacing=5)
        self.ui_name_list = [ui_name1, ui_name2]

    def __ball_predict(self, a_ball):
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
        dtX = a_ball.time_to_leave_border()
        dtY = a_ball.time_to_hit_horizontal_wall()
        heapq.heappush(self._pq, Event(self._t + dtX, a_ball, None, None))
        heapq.heappush(self._pq, Event(self._t + dtY, None, a_ball, None))

    def __draw_border(self, line_thickness, color_normal, color_left, color_right, n_interval):
        """
        Draw the game border with specified parameters.

        Args:
            line_thickness (int): Border line thickness
            color_normal (tuple): RGB color for horizontal borders
            color_left (tuple): RGB color for left border
            color_right (tuple): RGB color for right border
            n_interval (int): Number of dashed line intervals
        """
        turtle.penup()
        turtle.goto(-self._border_width, -self._border_height)
        turtle.pensize(line_thickness)
        turtle.setheading(0)

        # write the top/bottom border
        for color_i in [color_right, color_left]:
            turtle.pendown()
            turtle.color(color_normal)
            turtle.forward(2*self._border_width)
            turtle.left(90)
            turtle.color(color_i)

            # write the left/right border with dashed line
            for i in range(1, n_interval+1):
                if i % 2 == 1:
                    turtle.pendown()
                    turtle.forward(2*self._border_height/n_interval)
                    turtle.penup()
                else:
                    turtle.forward(2*self._border_height/n_interval)

            turtle.left(90)
        turtle.penup()

    def __redraw(self):
        """ Redraw everything"""
        turtle.clear()

        self.__draw_border(line_thickness=10,
                           color_normal="black",
                           color_left=self._player_colors[0],
                           color_right=self._player_colors[1],
                           n_interval=15)

        # draw players and also their name and score
        for i in range(len(self._player_list)):
            self._player_list[i].draw()
            self.ui_score_list[i]._text = str(self._player_list[i]._score)
            self.ui_score_list[i].draw()
            self.ui_name_list[i].draw()

        # draw the balls
        for a_ball in self._ball_list:
            a_ball.draw()

        turtle.update()
        heapq.heappush(self._pq, Event(
            self._t + 1.0/self._HZ, None, None, None))

    def __paddle_predict(self):
        """
        predict the collision between the balls and paddles
        both vertically and horizontally.
        """
        for a_player in self._player_list:
            for a_ball in self._ball_list:
                dtPX = a_ball.time_to_hit_paddle_vertical(a_player)
                dtPY = a_ball.time_to_hit_paddle_horizontal(a_player)
                heapq.heappush(self._pq, Event(
                    self._t + dtPX, a_ball, None, a_player))
                heapq.heappush(self._pq, Event(
                    self._t + dtPY, a_ball, None, a_player))

    def __winning_screen(self):
        """Display and run the ending screen"""
        # set the display colors and name to the winning player
        if self._player_list[0]._score > self._player_list[1]._score:
            color = self._player_list[0]._color
            name = self._player_list[0]._name
        else:
            color = self._player_list[1]._color
            name = self._player_list[1]._name

        # initialize the ui(s)
        ui_winning_text = Text(text=str(name+" WON"), pos=[0, 40], 
                               char_size=[40, 90], color=color, 
                               thickness=20, spacing=30)
        ui_retry = Button(text="REMATCH", pos=[0, -70], char_size=[30, 40], 
                          idle_color=(100, 100, 100), hover_color=(50, 200, 50), 
                          thickness=15, spacing=20)

        self.__rematch = False

        # reset the values and re-run the game if the "REMATCH" button is pressed
        def on_click(x, y):
            """ 
            a function for turtle to redirect to when mouse is clicked.
            if the cursor overlap with the button when clicked then restart the game.
            """
            if ui_retry.is_hovered(x, y):
                self.__rematch = True
                self._pq.clear()
                self._t = 0
                for a_ball in self._ball_list:
                    a_ball.respawn()
                for a_player in self._player_list:
                    a_player._score = 0
                self.play()

        # go to the function above if the mouse is clicked
        turtle.onscreenclick(on_click)

        # keep drawing the ui if the rematch button hasn't been pressed
        while self.__rematch == False:
            turtle.clear()
            ui_retry.active()
            ui_winning_text.draw()
            turtle.update()

    def __adjust_hz(self):
        """
        Adjust the HZ based on the amount of character on the screen
        to account for the lag it will cause.
        """
        total_char = 0

        for a_player in self._player_list:
            total_char += len(a_player._name)

        self._HZ = 5 + total_char * (-0.1)

    def __playing_loop(self):
        """
        Main loop of the game, run all the interaction between objects.
        """
        while (True):
            current_event = heapq.heappop(self._pq)
            if not current_event.is_valid():
                continue

            ball_a = current_event._ball_a
            ball_b = current_event._ball_b
            paddle_a = current_event._paddle
            player_1 = self._player_list[0]
            player_2 = self._player_list[1]
            # update positions, and then simulation clock
            for i in range(len(self._ball_list)):
                self._ball_list[i].move(current_event._time - self._t)

            for a_player in self._player_list:
                a_player.update_position()
                a_player.update_angle()

            self._t = current_event._time

            if (ball_a is not None) and (ball_b is not None) and (paddle_a is None):
                ball_a.bounce_off_ball(ball_b)
            elif (ball_a is not None) and (ball_b is None) and (paddle_a is None):
                # Detecting which side gain the score
                if ball_a._x < 0:
                    player_2._score += 1
                elif ball_a._x > 0:
                    player_1._score += 1
                # break and go to the winning screen if a player wins
                if player_1._score >= self._winning_score or player_2._score >= self._winning_score:
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
        turtle.bye()

        # hold the window; close it by clicking the window close 'x' mark
        turtle.done()

# num_balls = int(input("Number of balls to simulate: "))
