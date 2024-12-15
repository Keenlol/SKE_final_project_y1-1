import turtle
import math
import random

class Ball:
    def __init__(self, size_range, id, base_speed, border_size):
        self.__size_range = size_range
        self._base_speed = base_speed
        self._count = 0
        self._id = id
        self.__border_width = border_size[0]
        self.__border_height = border_size[1]

        self.respawn()
        

    def draw(self):
        turtle.penup()
        turtle.pensize(0)
        turtle.color(self._color)
        turtle.fillcolor(self._color)
        turtle.goto(self._x, self._y-self._size)
        turtle.setheading(0)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(self._size)
        turtle.end_fill()

    def bounce_off_vertical_wall(self):
        self._vx = -self._vx
        self._count += 1
        self.__update_color()

    def bounce_off_horizontal_wall(self):
        self._vy = -self._vy
        self._count += 1
        self.__update_color()

    def bounce_off(self, that):
        dx  = that._x - self._x
        dy  = that._y - self._y
        dvx = that._vx - self._vx
        dvy = that._vy - self._vy
        dvdr = dx*dvx + dy*dvy; # dv dot dr
        dist = self._size + that._size   # distance between particle centers at collison

        # magnitude of normal force
        magnitude = 2 * self.__mass * that.__mass * dvdr / ((self.__mass + that.__mass) * dist)

        # normal force, and in x and y directions
        fx = magnitude * dx / dist
        fy = magnitude * dy / dist

        # update velocities according to normal force
        self._vx += fx / self.__mass
        self._vy += fy / self.__mass
        that._vx -= fx / that.__mass
        that._vy -= fy / that.__mass
        
        # update collision counts
        self._count += 1
        that._count += 1
        self.__update_color()
        that.__update_color()

    def distance(self, that):
        x1 = self._x
        y1 = self._y
        x2 = that._x
        y2 = that._y
        d = math.sqrt((y2-y1)**2 + (x2-x1)**2)
        return d

    def move(self, dt):
        self._x += self._vx*dt
        self._y += self._vy*dt

    def time_to_hit_ball(self, that):
        if self is that:
            return math.inf
        dx  = that._x - self._x
        dy  = that._y - self._y
        dvx = that._vx - self._vx
        dvy = that._vy - self._vy
        dvdr = dx*dvx + dy*dvy
        if dvdr > 0:
            return math.inf
        dvdv = dvx*dvx + dvy*dvy
        if dvdv == 0:
            return math.inf
        drdr = dx*dx + dy*dy
        sigma = self._size + that._size
        d = (dvdr*dvdr) - dvdv * (drdr - sigma*sigma)
        # if drdr < sigma*sigma:
            # print("overlapping particles")
        if d < 0:
            return math.inf
        t = -(dvdr + math.sqrt(d)) / dvdv

        # should't happen, but seems to be needed for some extreme inputs
        # (floating-point precision when dvdv is close to 0, I think)
        if t <= 0:
            return math.inf

        return t

    def time_to_leave_border(self):
        if self._vx > 0:
            return (self.__border_width - self._x + self._size) / self._vx
        elif self._vx < 0:
            return (self.__border_width + self._x + self._size) / (-self._vx)
        else:
            return math.inf

    def time_to_hit_horizontal_wall(self):
        if self._vy > 0:
            return (self.__border_height - self._y - self._size) / self._vy
        elif self._vy < 0:
            return (self.__border_height + self._y - self._size) / (-self._vy)
        else:
            return math.inf

    def __rotate_xy_around_pivot(self, x, y, pivot_x, pivot_y, angle_add_degree):
            angle_add = math.radians(angle_add_degree)
            angle_origin = math.atan2((y - pivot_y),(x - pivot_x))

            radius = math.dist([x, y],[pivot_x, pivot_y])

            final_y = radius * math.sin(angle_origin + angle_add) + pivot_y
            final_x = radius * math.cos(angle_origin + angle_add) + pivot_x
            return final_x, final_y

    def time_to_hit_paddle_horizontal(self, paddle):
        magic_x, magic_y = self.__rotate_xy_around_pivot(self._x, self._y, paddle._x, paddle._y, -paddle._angle_deg)
        magic_vx, magic_vy = self.__rotate_xy_around_pivot(self._vx, self._vy, 0, 0, -paddle._angle_deg)

        if (magic_vx > 0) and ((magic_x + self._size) > (paddle._x - paddle._width/2)):
            return math.inf
        if (magic_vx < 0) and ((magic_x - self._size) < (paddle._x + paddle._width/2)):
            return math.inf

        dtx = (abs(paddle._x - magic_x) - self._size - paddle._width/2) / abs(magic_vx)

        paddle_bottom_edge = paddle._y - paddle._height/2
        paddle_top_edge = paddle._y + paddle._height/2

        if paddle_bottom_edge - self._size <= magic_y + (magic_vy*dtx) <= paddle_top_edge + self._size:
            return dtx
        else:
            return math.inf

    def time_to_hit_paddle_vertical(self, paddle):
        magic_x, magic_y = self.__rotate_xy_around_pivot(self._x, self._y, paddle._x, paddle._y, -paddle._angle_deg)
        magic_vx, magic_vy = self.__rotate_xy_around_pivot(self._vx, self._vy, 0, 0, -paddle._angle_deg)

        if (magic_vy > 0) and ((magic_y + self._size) > (paddle._y - paddle._height/2)):
            return math.inf
        if (magic_vy < 0) and ((magic_y - self._size) < (paddle._y + paddle._height/2)):
            return math.inf

        if magic_vy == 0:
            return math.inf
        dty = (abs(paddle._y - magic_y) - self._size - paddle._height/2) / abs(magic_vy)


        paddle_left_edge = paddle._x - paddle._width/2
        paddle_right_edge = paddle._x + paddle._width/2

        if paddle_left_edge - self._size <= magic_x + (magic_vx*dty) <= paddle_right_edge + self._size:
            return dty
        else:
            return math.inf

    def bounce_off_paddle(self, paddle):
        magic_x, magic_y = self.__rotate_xy_around_pivot(self._x, self._y, paddle._x, paddle._y, -paddle._angle_deg)
        magic_vx, magic_vy = self.__rotate_xy_around_pivot(self._vx, self._vy, 0, 0, -paddle._angle_deg)
        dx = abs(magic_x - paddle._x) - self._size - paddle._width/2
        dy = abs(magic_y - paddle._y) - self._size - paddle._height/2

        if dx > dy:
            magic_vx = -magic_vx
        else:
            magic_vy = -magic_vy
        
        # Convert velocity back to world coordinates
        self._vx, self._vy = self.__rotate_xy_around_pivot(magic_vx, magic_vy, 0, 0, paddle._angle_deg)
        
        # Add some randomization to make it more interesting 
        current_angle_rad = math.atan2(self._vy,self._vx)
        self._vx += self._base_speed * math.cos(current_angle_rad) * 0.1
        self._vy += self._base_speed * math.sin(current_angle_rad) * 0.1
        self._count += 1

        self.__update_color()

    def respawn(self):
        angle_rad = math.radians(random.randint(0, 360))
        self._x = 0
        self._y = 0
        self._vx = self._base_speed * math.cos(angle_rad)
        self._vy = self._base_speed * math.sin(angle_rad)
        self._size = random.randint(self.__size_range[0], self.__size_range[1])
        self.__mass = math.pi * self._size**2
        self._count += 1
        self.__update_color()
    
    def __update_color(self):
        color_gradient = [(200,230,255),(230,20,20)]
        
        current_speed = math.dist([0,0], [self._vx, self._vy])
        current_energy = (1/2) * self.__mass * current_speed**2
        min_energy = 8000
        max_energy = 1000000
        gradient_multiplier = (current_energy - min_energy)/(max_energy - min_energy)

        dR = color_gradient[1][0] - color_gradient[0][0] 
        dG = color_gradient[1][1] - color_gradient[0][1] 
        dB = color_gradient[1][2] - color_gradient[0][2] 

        if gradient_multiplier > 1:
            gradient_multiplier = 1
        elif gradient_multiplier < 0:
            gradient_multiplier = 0

        red = int(color_gradient[0][0] + dR*gradient_multiplier)
        green = int(color_gradient[0][1] + dG*gradient_multiplier)
        blue = int(color_gradient[0][2] + dB*gradient_multiplier)

        self._color = (red, green, blue)

        
    def __str__(self):
        return f"ball id={self._id} pos=({self._x:.2f}, {self._y:.2f}) v=({self._vx:.2f}, {self._vy:.2f}) count={self._count}"
