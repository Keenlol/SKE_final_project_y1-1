from paddle import Paddle

class Player(Paddle):
    def __init__(self, id, color, my_turtle, width, height):
        super().__init__(width, height, color, my_turtle)
        self.id = id
        self.score = 0
        self.input_set = {}
        self.__initailize_input_set()

        self.tilt_degree = 40
        self.move_per_step = 100

    def __initailize_input_set(self):
        if self.id == 1:
            self.input_set = {"move_up": "w",
                              "move_down": "s",
                              "tilt_cw": "d",
                              "tilt_ccw": "a"}
        elif self.id == 2:
            self.input_set = {"move_up": "Up",
                              "move_down": "Down",
                              "tilt_cw": "Right",
                              "tilt_ccw": "Left"}

    def get_input(self, screen):
        screen.listen()
        screen.onkey(self.move_up, self.input_set["move_up"])
        screen.onkey(self.move_down, self.input_set["move_down"])
        screen.onkey(self.tilt_cw, self.input_set["tilt_cw"])
        screen.onkey(self.tilt_ccw, self.input_set["tilt_ccw"])
    
    def move_up(self):
        self.set_location([self.x, self.y + self.move_per_step])

    def move_down(self):
        self.set_location([self.x, self.y - self.move_per_step])

    def tilt_cw(self):
        self.degree = -self.tilt_degree

    def tilt_ccw(self):
        self.degree = self.tilt_degree