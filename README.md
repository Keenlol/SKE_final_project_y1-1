# Pong Plus 🎮 

A 2-player Pong game with extra features like paddle tilting, multiple balls, dynamic ball colors based on kinetic energy, and customizable player names, paddle colors, and winning scores.
[Watch the demo here!](https://youtu.be/B3qD5VAks2k)

![Gameplay GIF](‎images/PongPLusDemoGameplay.gif)  
_Gameplay preview._

---

## Features ✨

- **2 Player Action**: Classic head-to-head Pong gameplay.  
- **Paddle Tilting**: Tilt paddles clockwise or counterclockwise for tricky shots.  
- **Multiple Balls**: Experience the chaos of multiple balls which respawns at the center when leaving the field.
- **Speedy Balls**: Ball speed increase everytime it hits the Paddle.
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

## Classes and Diagrams 📈

### Class Overview
- `PongPlus` : The game loops and is the central class of the game.
- `Ball` : All things ball!, position, mass, size, appearance, collision physics, collision prediction.
- `Event` : The event of the game. storing necessary data for each event. Use to queue up all the game activity.
- `Paddle` : The paddle, its angle, position, and appearance.
  - `Player` : The player, control their paddles, their scores and names.
- `Char` : Handles the display of a **sigle** alphanumeric character.
- `Text` : Handles the display of **multiple** alphanumeric character using the `Char` class.
  - `Button` : Clickable Text that do something.

### UML Diagram
![UML diagram of the PongPlus game](/images/UML_class_PongPlus.svg)
_UML diagram of the game._

---

## Project sophistication level ⭐

### 95
- An event-based game involving multiple ball objects colliding with one another and with multiple surfaces, one of which is a control-able and tilt-able paddles that can be oriented at an angle.
- The paddle has an animation using math instead of pre-coding it frame by frame.
- The ball linearly changes the color according to its kenetic engergy by following a set of color as a gradient.
- A custom fonts drawn purely with turtle in which its height, width and spacing can be easily adjusted if needed to.
- Includes an ending screen with a button that can restart the game as much as desired.
- 
---

## Project design and implementation 💻

-  As for the paddles, form Aj.Paruj's code which only detects and calculate collision from the top and bottom of the paddle. I added collisions detection and calculation from the side of the paddle.
-  As for calculating the collisions for tilting paddles, I rotate everything around the middle of the paddle and pretend like the paddle is up right, so that I can reuse the code for the not-tilted paddles. I created a helper function that rotate an (x, y) position around a certain pivot and that allows me to rotate the ball's position and velocity vectors around the paddle so that I can easily calculate it and rotate it back to apply the correct values.
-  Paddles animation where made by having a target location and then set the current position x% the distance between the current position and the target position so you have this kinda of nice *easing out* animation.
-  For the ball I added calculation for mass according to its size and also a color gradient code that will change the ball color based on its kenetic energy. The colors is from `rgb(200, 230, 255)` to `rgb(230, 20, 20)` (low to high), so that players can pay attention to the right ball among the chaos of it all. 
-  I added an extra class for displaying characters using turtle, which is basically a 3x3 grid which each point having its own id:
```
points:
0  1  2
3  4  5
6  7  8
```
- I can draw any character based this grid which the distance between each point can be adjusted by the given character width, height and spacing. I can draw characters it based on certain sequences such as...
  - `[0, 2, 8, 6]` for "0"
  - `[6, 3, 1, 5, 8, 5, 3]` for "A"
  - `[]` for " " (space)
  - 
- I also add the "REMATCH" button to replay the game.
- I use tkinter (which is module that turtle use to display stuff) to pop up prompts for the customization of the game which includes player names, number of balls and 7 colors that player can pick.
---


## Known Issues 🐞
- Paddles might ignore the ball when moving into it in a specific way that causes it to overlap with the ball, increasing the event frequency might fix it.
- Closing the game may cause flashing windows briefly (cosmetic issue).
