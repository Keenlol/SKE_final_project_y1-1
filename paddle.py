import turtle

class Paddle:
    def __init__(self, width, height, color, thickness=10):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.degree = 0
        self.color = color
        self.thickness = thickness
        turtle.penup()
        turtle.setheading(0)
        turtle.hideturtle()

    def set_location(self, location):
        self.x = location[0]
        self.y = location[1]
        turtle.goto(self.x, self.y)
#16 31
    def draw(self):
        turtle.color(self.color)
        turtle.pensize(self.thickness)
        turtle.goto(self.x, self.y)
        turtle.setheading(self.degree)
        turtle.forward(self.width/2)
        turtle.pendown()
        turtle.begin_fill()
        turtle.left(90)
        for _ in range(2):
            turtle.forward(self.height/2)
            turtle.left(90)
            turtle.forward(self.width)
            turtle.left(90)
            turtle.forward(self.height/2)
        turtle.end_fill()
        turtle.penup()
        turtle.goto(self.x, self.y)

    def clear(self):
        turtle.clear()

    def __str__(self):
        return f"paddle ({self.x:.2f}, {self.y:.2f}) a: {self.degree}*"
