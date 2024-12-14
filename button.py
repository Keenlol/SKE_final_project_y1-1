from text import Text
import turtle

class Button(Text):
    def __init__(self, text, pos, char_size, idle_color, thickness, spacing, hover_color) -> None:
        super().__init__(text ,pos, char_size, idle_color, thickness, spacing)
        self.hover_color = hover_color
        self.idle_color = idle_color
        self.extra_size = 0

    def __get_cursor_pos(self):
        screen = turtle.Screen()
        cursor_x = screen.getcanvas().winfo_pointerx() - screen.getcanvas().winfo_rootx()
        cursor_y = screen.getcanvas().winfo_pointery() - screen.getcanvas().winfo_rooty()
        
        cursor_x = cursor_x - screen.window_width() // 2
        cursor_y = screen.window_height() // 2 - cursor_y
        
        return cursor_x, cursor_y

    def is_hovered(self, x, y):
        bottom_right = [self.char_list[0].grid_points[8][0] + self.extra_size,
                       self.char_list[0].grid_points[8][1] - self.extra_size]
        top_left = [self.char_list[-1].grid_points[0][0] - self.extra_size,
                    self.char_list[-1].grid_points[0][1] + self.extra_size]
        
        return bottom_right[0] <= x <= top_left[0] and bottom_right[1] <= y <= top_left[1]

    def active(self):
        cursor_x, cursor_y = self.__get_cursor_pos()
        
        if self.is_hovered(cursor_x, cursor_y):
            self.color = self.hover_color
        else:
            self.color = self.idle_color
        
        self.draw()

