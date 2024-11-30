class Paddle:
    def __init__(self, width, height, color, my_turtle):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.color = color
        self.my_turtle = my_turtle
        self.my_turtle.penup()
        self.my_turtle.setheading(0)
        self.my_turtle.hideturtle()

    def set_location(self, location):
        self.x = location[0]
        self.y = location[1]
        self.my_turtle.goto(self.x, self.y)

    def draw(self):
        self.my_turtle.color(self.color)
        self.my_turtle.goto(self.x, self.y - self.height/2)
        self.my_turtle.forward(self.width/2)
        self.my_turtle.pendown()
        self.my_turtle.begin_fill()
        for _ in range(2):
            self.my_turtle.left(90)
            self.my_turtle.forward(self.height)
            self.my_turtle.left(90)
            self.my_turtle.forward(self.width)
        self.my_turtle.end_fill()
        self.my_turtle.penup()
        self.my_turtle.goto(self.x, self.y)

    def clear(self):
        self.my_turtle.clear()

    def __str__(self):
        return "paddle"
