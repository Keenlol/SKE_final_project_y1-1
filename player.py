from paddle import Paddle

class Player(Paddle):
    def __init__(self, name, id, color, width, height, pos, canvas_info):
        super().__init__(width, height, color)
        self.name = name
        self.id = id
        self.score = 0
        self.input_set = {}
        self.canvas_width = canvas_info[0]
        self.canvas_height = canvas_info[1]
        self.__initailize_input_set()

        self.x = pos[0]
        self.y = pos[1]
        self.max_tilt_degree = 40
        self.target_degree = 0
        self.move_per_step = self.height*0.8
        self.target_x = self.x
        self.target_y = self.y

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
        if self.target_y < self.canvas_height/2:
            self.target_y += self.move_per_step

    def move_down(self):
        if self.target_y > -self.canvas_height/2:
            self.target_y -= self.move_per_step

    def update_position(self):
        dy = self.target_y - self.y
        self.set_location([self.x, self.y + 0.3 * dy])

    def tilt_cw(self):
        self.target_degree = -self.max_tilt_degree

    def tilt_ccw(self):
        self.target_degree = self.max_tilt_degree
    
    def tilt_reset(self):
        self.target_degree = 0

    def update_angle(self):
        d_angle = self.target_degree - self.degree
        self.degree = self.degree + d_angle * 0.3