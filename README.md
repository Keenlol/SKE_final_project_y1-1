# Pong Plus 🎮 

A 2-player Pong game with extra features like paddle tilting, multiple balls, dynamic ball colors based on kinetic energy, and customizable player names, paddle colors, and winning scores.

![Gameplay GIF](path_to_gif.gif)  
_Gameplay preview._  

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

### Classes and Diagrams

## Class Overview
- `PongPlus` : The game loops and is the central class of the game.
- `Ball` : All things ball!, position, mass, size, appearance, collision physics, collision prediction.
- `Event` : The event of the game. storing necessary data for each event. Use to queue up all the game activity.
- `Paddle` : The paddle, its angle, position, and appearance.
  - `Player` : The player, control their paddles, their scores and names.
- `Char` : Handles the display of a **sigle** alphanumeric character.
- `Text` : Handles the display of **multiple** alphanumeric character using the `Char` class.
  - `Button` : Clickable Text that do something.

## UML Diagram
![UML diagram of the PongPlus game](/images/UML_class_PongPlus.svg)
_UML diagram of the game._

---

## Known Issues 🐞
- Paddles might ignore the ball when moving into it in a specific way.
- Closing the game may cause flashing windows briefly (cosmetic issue).
- The ball might bounce off a "delayed invisible paddle" if the paddle is moved too quickly.
