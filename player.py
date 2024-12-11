from paddle import Paddle

class Player(Paddle):
    def __init__(self, id, color, width, height, pos, canvas_info):
        super().__init__(width, height, color)
        self.id = id
        self.score = 0
        self.input_set = {}
        self.canvas_width = canvas_info[0]
        self.canvas_height = canvas_info[1]
        self.__initailize_input_set()

        self.x = pos[0]
        self.y = pos[1]
        self.tilt_degree = 40
        self.move_per_step = self.height*0.8

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
        screen.onkeypress(self.move_up, self.input_set["move_up"])
        screen.onkeypress(self.move_down, self.input_set["move_down"])
        screen.onkeypress(self.tilt_cw, self.input_set["tilt_cw"])
        screen.onkeypress(self.tilt_ccw, self.input_set["tilt_ccw"])

        screen.onkeyrelease(self.tilt_reset, self.input_set["tilt_cw"])
        screen.onkeyrelease(self.tilt_reset, self.input_set["tilt_ccw"])
        
    
    def move_up(self):
        if self.y < self.canvas_height/2:
            self.set_location([self.x, self.y + self.move_per_step])

    def move_down(self):
        if self.y > -self.canvas_height/2:
            self.set_location([self.x, self.y - self.move_per_step])

    def tilt_cw(self):
        self.degree = -self.tilt_degree

    def tilt_ccw(self):
        self.degree = self.tilt_degree
    
    def tilt_reset(self):
        self.degree = 0