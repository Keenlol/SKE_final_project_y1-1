from paddle import Paddle

class Player(Paddle):
    def __init__(self, name, id, color, size, pos, border_height):
        super().__init__(size, color)
        self._name = name
        self._id = id
        self._score = 0
        self.__border_height = border_height
        self.__initailize_input_set()

        self._x = pos[0]
        self._y = pos[1]
        self._max_tilt_angle_deg = 40
        self._target_angle_deg = 0
        self.__dist_per_move = self._height*0.8
        self.__target_y = self._y

    def __initailize_input_set(self):
        if self._id == 1:
            self.__input_set = {"move_up": "w",
                              "move_down": "s",
                              "tilt_cw": "d",
                              "tilt_ccw": "a"}
        elif self._id == 2:
            self.__input_set = {"move_up": "Up",
                              "move_down": "Down",
                              "tilt_cw": "Right",
                              "tilt_ccw": "Left"}

    def get_input(self, screen):
        screen.listen()
        screen.onkeypress(self.move_up, self.__input_set["move_up"])
        screen.onkeypress(self.move_down, self.__input_set["move_down"])
        screen.onkeypress(self.tilt_cw, self.__input_set["tilt_cw"])
        screen.onkeypress(self.tilt_ccw, self.__input_set["tilt_ccw"])

        screen.onkeyrelease(self.tilt_reset, self.__input_set["tilt_cw"])
        screen.onkeyrelease(self.tilt_reset, self.__input_set["tilt_ccw"])
        
    
    def move_up(self):
        if self.__target_y < self.__border_height/2:
            self.__target_y += self.__dist_per_move

    def move_down(self):
        if self.__target_y > -self.__border_height/2:
            self.__target_y -= self.__dist_per_move

    def update_position(self):
        dy = self.__target_y - self._y
        self.pos = [self._x, self._y + 0.3 * dy]

    def tilt_cw(self):
        self._target_angle_deg = -self._max_tilt_angle_deg

    def tilt_ccw(self):
        self._target_angle_deg = self._max_tilt_angle_deg
    
    def tilt_reset(self):
        self._target_angle_deg = 0

    def update_angle(self):
        d_angle = self._target_angle_deg - self._angle_deg
        self._angle_deg = self._angle_deg + d_angle * 0.3
