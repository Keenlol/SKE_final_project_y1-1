# Pong Plus 🎮 

##### A 2-player Pong game with extra features like paddle tilting, dynamic ball colors based on kinetic energy, multiple balls, and customizable player names, paddle colors, and winning scores.
![Gameplay GIF](path_to_gif.gif)  
_Include a short GIF showing the gameplay in action._  
---

## Features ✨

- **2 Player Action**: Classic head-to-head Pong gameplay.  
- **Paddle Tilting**: Tilt paddles clockwise or counterclockwise for tricky shots.  
- **Multiple Balls**: Experience the chaos of multiple balls which respawns at the center when leaving the field.  
- **Customization Options**: before the game starts you'll get to
  - Choose paddle colors for each player.  
  - Set player names to personalize the game.  
  - Define the winning score.  
- **Stats & Rematch**:  
  - Displays scores and player names during gameplay.  
  - Includes a **Rematch** button when a player wins.  
- **Dynamic Ball Colors**: Ball colors change based on kinetic energy to shift player's focus to danger!  
- **Paddle animation**: Smooth dynamic animation (using math!!!) for paddle's movement and rotation.
---

## How to Play 🚀

1. Clone the Repository: `git clone https://github.com/Keenlol/SKE_final_project_y1-1 PongPlus`
2. Run the `run_me.py` file.
3. Find a friend (optional)
4. Enter player names, paddle colors, and the winning score when prompted.
5. Let the game begin!

---

## Controls 🎮
| **Player**       | **Move Up** | **Move Down** | **Tilt Clockwise** | **Tilt Counterclockwise** |
|-------------------|-------------|---------------|---------------------|---------------------------|
| Player 1 (Left)  | `W`         | `S`           | `D`                 | `A`                       |
| Player 2 (Right) | `↑`         | `↓`           | `→`                 | `←`                       |


---

## Technical Setup ⚙️

### Prerequisites  
Ensure you have the following installed:  
- Python 3.8 or higher  
- Required libraries: math, random, turtle, tkinter

---

## Known Issues 🐞
- Paddles might ignore the ball when moving into it in a specific way.
- Closing the game may cause flashing windows briefly (cosmetic issue).
- The ball might bounce off a "delayed invisible paddle" if the paddle is moved too quickly.
