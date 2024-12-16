""" Module providing a ball class"""

import math
import random
from turtle import Turtle
from paddle import Paddle

class Ball:
    """
    Represents a ball in the game with physics properties and collision detection.

    Attributes:
        _size (float): Radius of the ball
        _x (float): X position
        _y (float): Y position
        _vx (float): X velocity
        _vy (float): Y velocity
        _color (tuple): RGB color
        _count (int): Collision counter
    """

    def __init__(self, size_range: list,
                 my_turtle: Turtle,
                 uid: int,
                 base_speed: float,
                 border_size: list,
                 color_gradient: list=None):
        """
        Initialize a ball with given parameters.

        Args:
            size_range (list): [min_size, max_size] for random size selection
            id (int): Unique identifier for the ball
            base_speed (float): Initial speed
            border_size (list): [width, height] of game border
            color_gradient (list): List of RGB colors for gradient (2 colors)
        """
        if color_gradient is None:
            color_gradient = [(200, 230, 255), (230, 20, 20)]

        self.__size_range = size_range
        self._base_speed = base_speed
        self._count = 0
        self._uid = uid
        self.__border_width = border_size[0]
        self.__border_height = border_size[1]
        self.__color_gradient = color_gradient
        self._color = self.__color_gradient[0]
        self.__my_turle = my_turtle

        self.respawn()

    @property
    def x(self):
        """X position getter"""
        return self._x

    @x.setter
    def x(self, x):
        """X position setter"""
        self._x = x

    @property
    def y(self):
        """Y position getter"""
        return self._y

    @y.setter
    def y(self, y):
        """Y position setter"""
        self._y = y

    @property
    def vx(self):
        """X signed velocity getter"""
        return self._vx

    @vx.setter
    def vx(self, vx):
        """X signed velocity setter"""
        self._vx = vx

    @property
    def vy(self):
        """Y signed velocity getter"""
        return self._vy

    @vy.setter
    def vy(self, vy):
        """Y signed velocity setter"""
        self._vy = vy

    @property
    def mass(self):
        """ Ball's mass getter"""
        return self._mass

    @property
    def size(self):
        """ Ball's size getter"""
        return self._size

    @property
    def count(self):
        """ Ball's number of finished event getter"""
        return self._count

    def draw(self):
        """Draw the ball at its position and current color"""
        self.__my_turle.penup()
        self.__my_turle.pensize(0)
        self.__my_turle.color(self._color)
        self.__my_turle.fillcolor(self._color)
        self.__my_turle.goto(self.x, self.y-self.size)
        self.__my_turle.setheading(0)
        self.__my_turle.pendown()
        self.__my_turle.begin_fill()
        self.__my_turle.circle(self.size)
        self.__my_turle.end_fill()

    def move(self, dt: float):
        """Update the ball position based on its velocities."""
        self.x += self.vx*dt
        self.y += self.vy*dt

    def bounce_off_horizontal_wall(self):
        """Invert the y velocity, use when hitting the top or bottom of the border."""
        self.vy = -self.vy
        self._count += 1
        self.update_color()

    def bounce_off_ball(self, that):
        """
        Handle collision physics between two balls.

        Args:
            that (Ball): The other ball involved in collision
        """
        dx = that.x - self.x
        dy = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx*dvx + dy*dvy  # dv dot dr
        dist = self.size + that.size   # distance between particle centers at collison

        # magnitude of normal force
        magnitude = 2 * self.mass * that.mass * dvdr / ((self.mass + that.mass) * dist)

        # normal force, and in x and y directions
        fx = magnitude * dx / dist
        fy = magnitude * dy / dist

        # update velocities according to normal force
        self.vx += fx / self.mass
        self.vy += fy / self.mass
        that.vx -= fx / that.mass
        that.vy -= fy / that.mass

        # update collision counts
        self._count += 1
        that._count += 1
        self.update_color()
        that.update_color()

    def bounce_off_paddle(self, paddle: Paddle):
        """
        Handle the collision physics between the ball and a paddle.

        Args:
            that (Paddle): The paddle involved in collision
        """
        magic_x, magic_y = self.__rotate_xy_around_pivot(
            [self.x, self.y], [paddle.x, paddle.y], -paddle.angle_deg)
        magic_vx, magic_vy = self.__rotate_xy_around_pivot(
            [self.vx, self.vy], [0, 0], -paddle.angle_deg)

        dx = abs(magic_x - paddle.x) - self.size - paddle.width/2
        dy = abs(magic_y - paddle.y) - self.size - paddle.height/2

        if dx > dy:
            magic_vx = -magic_vx
        else:
            magic_vy = -magic_vy

        # Convert velocity back to world coordinates
        self.vx, self.vy = self.__rotate_xy_around_pivot(
            [magic_vx, magic_vy], [0, 0], paddle.angle_deg)

        # Add some randomization to make it more interesting
        current_angle_rad = math.atan2(self.vy, self.vx)
        self.vx += self._base_speed * math.cos(current_angle_rad) * 0.1
        self.vy += self._base_speed * math.sin(current_angle_rad) * 0.1
        self._count += 1

        self.update_color()

    def time_to_hit_ball(self, that):
        """ Returns the predicted time the ball will collide with another ball.
        
        Args:
            that (Ball): The other ball involved in collision
        """
        if self is that:
            return math.inf
        dx = that.x - self.x
        dy = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx*dvx + dy*dvy
        if dvdr > 0:
            return math.inf
        dvdv = dvx*dvx + dvy*dvy
        if dvdv == 0:
            return math.inf
        drdr = dx*dx + dy*dy
        sigma = self.size + that.size
        d = (dvdr*dvdr) - dvdv * (drdr - sigma*sigma)

        if d < 0:
            return math.inf
        t = -(dvdr + math.sqrt(d)) / dvdv

        # should't happen, but seems to be needed for some extreme inputs
        # (floating-point precision when dvdv is close to 0, I think)
        if t <= 0:
            return math.inf

        return t

    def time_to_leave_border(self):
        """ Returns the predicted time the ball will leave the border (left/right)."""
        if self.vx > 0:
            return (self.__border_width - self.x + self.size) / self.vx
        elif self.vx < 0:
            return (self.__border_width + self.x + self.size) / (-self.vx)
        else:
            return math.inf

    def time_to_hit_horizontal_wall(self):
        """ Returns the predicted time the ball will hit the border (top/bottom)."""
        if self.vy > 0:
            return (self.__border_height - self.y - self.size) / self.vy
        elif self.vy < 0:
            return (self.__border_height + self.y - self.size) / (-self.vy)
        else:
            return math.inf

    def __rotate_xy_around_pivot(self, xy: list, pivot: list, angle_add: float):
        """
        Rotate the (x,y) coordinate around a pivot with a given amount of angle
        
        Args:
            x (float): X coordinate before rotation
            y (float): Y coordinate before rotation
            pivot_x (float): X coordinate of the pivot
            pivot_y (float): Y coordinate of the pivot
            angle_add (float): Amount of angle to rotate (anti-clockwise, in degrees)
        """
        x = xy[0]
        y = xy[1]
        pivot_x = pivot[0]
        pivot_y = pivot[1]

        angle_add = math.radians(angle_add)
        angle_origin = math.atan2((y - pivot_y), (x - pivot_x))

        radius = math.dist([x, y], [pivot_x, pivot_y])

        final_y = radius * math.sin(angle_origin + angle_add) + pivot_y
        final_x = radius * math.cos(angle_origin + angle_add) + pivot_x
        return final_x, final_y

    def time_to_hit_paddle_horizontal(self, paddle: Paddle):
        """ Returns the predicted time the ball will hit the left or right side of the paddle"""
        magic_x, magic_y = self.__rotate_xy_around_pivot(
            [self.x, self.y], [paddle.x, paddle.y], -paddle.angle_deg)
        magic_vx, magic_vy = self.__rotate_xy_around_pivot(
            [self.vx, self.vy], [0, 0], -paddle.angle_deg)

        if (magic_vx > 0) and ((magic_x + self.size) > (paddle.x - paddle.width/2)):
            return math.inf
        if (magic_vx < 0) and ((magic_x - self.size) < (paddle.x + paddle.width/2)):
            return math.inf

        dtx = (abs(paddle.x - magic_x) - self.size - paddle.width/2) / abs(magic_vx)

        paddle_bottom_edge = paddle.y - paddle.height/2
        paddle_top_edge = paddle.y + paddle.height/2

        if paddle_bottom_edge - self.size <= magic_y + (magic_vy*dtx) <= paddle_top_edge + self.size:
            return dtx
        else:
            return math.inf

    def time_to_hit_paddle_vertical(self, paddle: Paddle):
        """ Returns the predicted time the ball will hit the top or bottom side of the paddle"""
        magic_x, magic_y = self.__rotate_xy_around_pivot(
            [self.x, self.y], [paddle.x, paddle.y], -paddle.angle_deg)
        magic_vx, magic_vy = self.__rotate_xy_around_pivot(
            [self.vx, self.vy], [0, 0], -paddle.angle_deg)

        if (magic_vy > 0) and ((magic_y + self.size) > (paddle.y - paddle.height/2)):
            return math.inf
        if (magic_vy < 0) and ((magic_y - self.size) < (paddle.y + paddle.height/2)):
            return math.inf

        if magic_vy == 0:
            return math.inf
        dty = (abs(paddle.y - magic_y) - self.size - paddle.height/2) / abs(magic_vy)

        paddle_left_edge = paddle.x - paddle.width/2
        paddle_right_edge = paddle.x + paddle.width/2

        if paddle_left_edge - self.size <= magic_x + (magic_vx*dty) <= paddle_right_edge + self.size:
            return dty
        else:
            return math.inf

    def respawn(self):
        """ Reset the position, size and velocity of the ball"""
        angle_rad = math.radians(random.randint(0, 360))
        self._x = 0
        self._y = 0
        self._vx = self._base_speed * math.cos(angle_rad)
        self._vy = self._base_speed * math.sin(angle_rad)
        self._size = random.randint(self.__size_range[0], self.__size_range[1])
        self._mass = math.pi * self.size**2
        self._count += 1
        self.update_color()

    def update_color(self):
        """
        Linearly change the color of the ball based on its kenetic energy
        by using its gradient colors
        """
        current_speed = math.dist([0, 0], [self.vx, self.vy])
        current_energy = (1/2) * self.mass * current_speed**2
        min_energy = 8000
        max_energy = 1000000
        gradient_multiplier = (current_energy - min_energy) / \
            (max_energy - min_energy)

        dr = self.__color_gradient[1][0] - self.__color_gradient[0][0]
        dg = self.__color_gradient[1][1] - self.__color_gradient[0][1]
        db = self.__color_gradient[1][2] - self.__color_gradient[0][2]

        if gradient_multiplier > 1:
            gradient_multiplier = 1
        elif gradient_multiplier < 0:
            gradient_multiplier = 0

        red = int(self.__color_gradient[0][0] + dr*gradient_multiplier)
        green = int(self.__color_gradient[0][1] + dg*gradient_multiplier)
        blue = int(self.__color_gradient[0][2] + db*gradient_multiplier)

        self._color = (red, green, blue)

    def __str__(self):
        return f"ball id={self._uid} pos=({self.x:.2f}, {self.y:.2f}) v=({self.vx:.2f}, {self.vy:.2f}) count={self._count}"
