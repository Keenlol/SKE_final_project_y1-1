""" A main file to input the values for PongPlus"""


import tkinter as tk
from tkinter import simpledialog
from pong_plus import PongPlus


color_preset = {"purple": (160, 76, 245),
                "cyan": (0, 181, 194),
                "blue": (32, 76, 247),
                "green": (50, 179, 59),
                "yellow": (165, 171, 2),
                "orange": (237, 106, 24),
                "red": (222, 51, 51),
                }

root = tk.Tk()
root.withdraw()  # Hide the root window

name1 = simpledialog.askstring("Input", "Player 1 name:")
name2 = simpledialog.askstring("Input", "Player 2 name:")

color1 = simpledialog.askstring("Input", "Player 1 color (purple/cyan/blue/green/yellow/orange/red):")
color2 = simpledialog.askstring("Input", "Player 2 color (purple/cyan/blue/green/yellow/orange/red):")

winning_score = simpledialog.askinteger("Input", "Winning score:")

game = PongPlus(num_balls=2,
                player_names=[name1, name2],
                player_colors=[color_preset[color1], color_preset[color2]],
                winning_score=winning_score)
game.play()
