from text import Text
import turtle

class Button(Text):
    def __init__(self, text, pos, char_size, idle_color, thickness, spacing, hover_color) -> None:
        super().__init__(text ,pos, char_size, idle_color, thickness, spacing)
        self.hover_color = hover_color
        self.idle_color = idle_color
        self.raw_x_constant = 1535
        self.raw_y_constant = 863
        self.screen_width = 1920
        self.screen_height = 1080

    def __get_cursor_pos(self, canvas):
        raw_x = canvas.winfo_pointerx()
        raw_y = canvas.winfo_pointery()

        max_raw_x = self.raw_x_constant #I measured these
        max_raw_y = -self.raw_y_constant

        percent_x = (raw_x/max_raw_x) - 0.5
        percent_y = (raw_y/max_raw_y) + 0.5

        cursor_x = percent_x * (self.screen_width)
        cursor_y = percent_y * (self.screen_height)
        return cursor_x, cursor_y

    def __get_window_pos(self, canvas):
        root = canvas.winfo_toplevel()

        x_pos = root.winfo_x()
        y_pos = root.winfo_y()

        return x_pos, y_pos


    def __get_window_size(self, canvas):
        # Get the current width and height
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        return width, height

    def draw_animation(self):
        canvas = turtle.getcanvas()
        cursor_x, cursor_y = self.__get_cursor_pos(canvas)
        window_x, window_y = self.__get_window_pos(canvas)
        window_width, window_height = self.__get_window_size(canvas)

        print("win x y",self.char_list[0].grid_points[8], "cursor x y:",[int(cursor_x),int(cursor_y)])
        offset_x = (window_x + ((self.raw_x_constant - window_width) / 2)) * (self.screen_width / self.raw_x_constant)
        offset_y = - (window_y + ((self.raw_y_constant - window_height) / 2)) * (self.screen_height / self.raw_y_constant)

        bottom_right = [self.char_list[0].grid_points[8][0] + offset_x,
                        self.char_list[0].grid_points[8][1] + offset_y]

        top_left = [self.char_list[-1].grid_points[0][0] + offset_y,
                    self.char_list[-1].grid_points[0][1] + offset_x] 

        if bottom_right[0] <= cursor_x <= top_left[0] and bottom_right[1] <= cursor_y <= top_left[1]:
            self.color = self.hover_color
        else:
            self.color = self.idle_color
        
        self.draw()
