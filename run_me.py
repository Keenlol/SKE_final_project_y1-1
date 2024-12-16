""" A main file to input the values for PongPlus"""

import tkinter as tk
from tkinter import ttk
from pong_plus import PongPlus

class GameSetupWindow:
    """
    A GUI window for setting up PongPlus game parameters.

    This class creates and manages a tkinter window that allows users to input
    game settings before starting a PongPlus game.

    Attributes:
        + root (tk.Tk): Main tkinter window instance
        + color_preset (dict): Dictionary mapping color names to RGB tuples
        # _p1_name (ttk.Entry): Input field for Player 1's name
        # _p1_color (ttk.Combobox): Color selection dropdown for Player 1
        # _p2_name (ttk.Entry): Input field for Player 2's name
        # _p2_color (ttk.Combobox): Color selection dropdown for Player 2
        # _winning_score (ttk.Entry): Input field for winning score

    Methods:
        + create_widgets(): Creates and arranges all GUI elements
        + validate_inputs(): Checks if all inputs are valid
        + start_game(): Initializes and starts the game with input values
        + run(): Starts the GUI event loop
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PongPlus!!")
        self.root.geometry("400x500")
        
        # Color presets
        self.color_preset = {
            "purple": (160, 76, 245),
            "cyan": (0, 181, 194),
            "blue": (32, 76, 247),
            "green": (50, 179, 59),
            "yellow": (165, 171, 2),
            "orange": (237, 106, 24),
            "red": (222, 51, 51),
        }

        # Create and pack widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="PongPlus Setup", font=('Arial', 18, 'bold'))
        title.pack(pady=20)

        # Player 1 frame
        p1_frame = ttk.LabelFrame(self.root, text="Player 1")
        p1_frame.pack(padx=20, pady=10, fill="x")

        ttk.Label(p1_frame, text="Name:").pack(padx=5, pady=5)
        self.p1_name = ttk.Entry(p1_frame)
        self.p1_name.pack(padx=5, pady=5)

        ttk.Label(p1_frame, text="Color:").pack(padx=5, pady=5)
        self.p1_color = ttk.Combobox(p1_frame, values=list(self.color_preset.keys()))
        self.p1_color.pack(padx=5, pady=5)

        # Player 2 frame
        p2_frame = ttk.LabelFrame(self.root, text="Player 2")
        p2_frame.pack(padx=20, pady=10, fill="x")

        ttk.Label(p2_frame, text="Name:").pack(padx=5, pady=5)
        self.p2_name = ttk.Entry(p2_frame)
        self.p2_name.pack(padx=5, pady=5)

        ttk.Label(p2_frame, text="Color:").pack(padx=5, pady=5)
        self.p2_color = ttk.Combobox(p2_frame, values=list(self.color_preset.keys()))
        self.p2_color.pack(padx=5, pady=5)

        # Winning score frame
        score_frame = ttk.LabelFrame(self.root, text="Game Settings")
        score_frame.pack(padx=20, pady=10, fill="x")

        ttk.Label(score_frame, text="Winning Score:").pack(padx=5, pady=5)
        self.winning_score = ttk.Entry(score_frame)
        self.winning_score.pack(padx=5, pady=5)

        # Start button
        ttk.Button(self.root, text="Start Game", command=self.start_game).pack(pady=20)

    def validate_inputs(self):
        """Validate all inputs before starting the game"""
        if not all([self.p1_name.get(), self.p2_name.get(), 
                   self.p1_color.get(), self.p2_color.get(),
                   self.winning_score.get()]):
            return False
        try:
            score = int(self.winning_score.get())
            if score <= 0:
                return False
        except ValueError:
            return False
        return True

    def start_game(self):
        """Start the game if all inputs are valid"""
        if not self.validate_inputs():
            tk.messagebox.showerror("Error", "Please fill all fields correctly.\nWinning score must be a positive number.")
            return

        # Get all values
        name1 = self.p1_name.get()
        name2 = self.p2_name.get()
        color1 = self.p1_color.get()
        color2 = self.p2_color.get()
        winning_score = int(self.winning_score.get())

        # Close the setup window
        self.root.destroy()

        # Start the game
        game = PongPlus(
            num_balls=2,
            player_names=[name1, name2],
            player_colors=[self.color_preset[color1], self.color_preset[color2]],
            winning_score=winning_score
        )
        game.play()

    def run(self):
        """Start the setup window"""
        self.root.mainloop()

if __name__ == "__main__":
    setup = GameSetupWindow()
    setup.run()
