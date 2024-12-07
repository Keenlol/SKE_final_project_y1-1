import turtle
import math
import random

class Ball:
    def __init__(self, size, x, y, vx, vy, color, id, canvas_width, canvas_height):
        self.size = size
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.mass = 100*size**2
        self.count = 0
        self.id = id
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        

    def draw(self):
        # draw a circle of radius equals to size centered at (x, y) and paint it with color
        turtle.penup()
        turtle.color(self.color)
        turtle.fillcolor(self.color)
        turtle.goto(self.x, self.y-self.size)
        turtle.setheading(0)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(self.size)
        turtle.end_fill()

    def bounce_off_vertical_wall(self):
        self.vx = -self.vx
        self.count += 1

    def bounce_off_horizontal_wall(self):
        self.vy = -self.vy
        self.count += 1

    def bounce_off(self, that):
        dx  = that.x - self.x
        dy  = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx*dvx + dy*dvy; # dv dot dr
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
        self.count += 1
        that.count += 1

    def distance(self, that):
        x1 = self.x
        y1 = self.y
        x2 = that.x
        y2 = that.y
        d = math.sqrt((y2-y1)**2 + (x2-x1)**2)
        return d

    def move(self, dt):
        self.x += self.vx*dt
        self.y += self.vy*dt

    def time_to_hit(self, that):
        if self is that:
            return math.inf
        dx  = that.x - self.x
        dy  = that.y - self.y
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

    def time_to_hit_vertical_wall(self):
        if self.vx > 0:
            return (self.canvas_width - self.x - self.size) / self.vx
        elif self.vx < 0:
            return (self.canvas_width + self.x - self.size) / (-self.vx)
        else:
            return math.inf

    def time_to_hit_horizontal_wall(self):
        if self.vy > 0:
            return (self.canvas_height - self.y - self.size) / self.vy
        elif self.vy < 0:
            return (self.canvas_height + self.y - self.size) / (-self.vy)
        else:
            return math.inf

    def __rotate_xy_around_pivot(self, x, y, pivot_x, pivot_y, angle_add_degree):
            angle_add = math.radians(angle_add_degree)
            angle_origin = math.atan2((y - pivot_y),(x - pivot_x))

            radius = math.dist([x, y],[pivot_x, pivot_y])

            final_y = radius * math.sin(angle_origin + angle_add) + pivot_y
            final_x = radius * math.cos(angle_origin + angle_add) + pivot_x
            return final_x, final_y

    def time_to_hit_paddle(self, paddle):

        magic_x, magic_y = self.__rotate_xy_around_pivot(self.x, self.y, paddle.x, paddle.y, -paddle.degree)
        magic_vx, magic_vy = self.__rotate_xy_around_pivot(self.vx, self.vy, 0, 0, -paddle.degree)

        if (magic_vy > 0) and ((magic_y + self.size) > (paddle.y - paddle.height/2)):
            return math.inf
        if (magic_vy < 0) and ((magic_y - self.size) < (paddle.y + paddle.height/2)):
            return math.inf
        if (magic_vx > 0) and ((magic_x + self.size) > (paddle.x - paddle.width/2)):
            return math.inf
        if (magic_vx < 0) and ((magic_x - self.size) < (paddle.x + paddle.width/2)):
            return math.inf

        dty = (abs(paddle.y - magic_y) - self.size - paddle.height/2) / abs(magic_vy)
        dtx = (abs(paddle.x - magic_x) - self.size - paddle.width/2) / abs(magic_vx)

        paddle_left_edge = paddle.x - paddle.width/2
        paddle_right_edge = paddle.x + paddle.width/2
        paddle_bottom_edge = paddle.y - paddle.height/2
        paddle_top_edge = paddle.y + paddle.height/2

        if paddle_left_edge - self.size <= magic_x + (magic_vx*dty) <= paddle_right_edge + self.size:
            return dty
        elif paddle_bottom_edge - self.size <= magic_y + (magic_vy*dtx) <= paddle_top_edge + self.size:
            return dtx
        else:
            return math.inf

    def bounce_off_paddle(self):
        self.vy = -self.vy
        self.count += 1
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def __str__(self):
        return str(self.x) + ":" + str(self.y) + ":" + str(self.vx) + ":" + str(self.vy) + ":" + str(self.count) + str(self.id)
