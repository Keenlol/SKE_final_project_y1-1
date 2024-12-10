import turtle

class Digit:
    def __init__(self, pos, width, height, color, thickness) -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.thickness = thickness
        self.width = width
        self.height = height

        dx = self.width/2
        dy = self.height/2

        self.grid_points = [[self.x-dx, self.y+dy], [self.x, self.y+dy], [self.x+dx, self.y+dy],
                            [self.x-dx, self.y], [self.x, self.y], [self.x+dx, self.y],
                            [self.x-dx, self.y-dy], [self.x, self.y-dy], [self.x+dx, self.y-dy]]

    def __draw_sequence(self, sequence):
        turtle.penup()
        turtle.goto(self.grid_points[sequence[0]][0], self.grid_points[sequence[0]][1])
        turtle.pendown()
        sequence.pop(0)
        for points in sequence:
            turtle.goto(self.grid_points[points][0], self.grid_points[points][1])
        turtle.penup()


    def draw(self, digit):
        turtle.penup()
        turtle.color(self.color)
        turtle.pensize(self.thickness)
        turtle.goto(self.x, self.y)
        turtle.setheading(0)
        turtle.pendown()

        if digit == 0:
            self.__draw_sequence([6,0,2,8,6])
        if digit == 1:
            self.__draw_sequence([3,1,7])
        if digit == 2:
            self.__draw_sequence([3,0,2,5,6,8])
        if digit == 3:
            self.__draw_sequence([0,2,4,5,8,6])
        if digit == 4:
            self.__draw_sequence([1,3,5,2,8])
        if digit == 5:
            self.__draw_sequence([2,0,3,5,8,6])
        if digit == 6:
            self.__draw_sequence([2,0,6,8,5,3])
        if digit == 7:
            self.__draw_sequence([0,2,7])
        if digit == 8:
            self.__draw_sequence([6,0,2,8,6,3,5])
        if digit == 9:
            self.__draw_sequence([5,3,0,2,8,6])