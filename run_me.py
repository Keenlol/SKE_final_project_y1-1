from pong_plus import PongPlus


color_preset = {"purple": (160, 76, 245),
                "cyan": (0, 181, 194),
                "blue": (32, 76, 247),
                "green": (50, 179, 59),
                "yellow": (165, 171, 2),
                "orange": (237, 106, 24),
                "red": (222, 51, 51),
                }


print("------------ PongPlus ------------")
print()
print("- Choose Names -")
name1 = input("Player 1 name: ")
name2 = input("Player 2 name: ")
print()
print("- Choose Colors -")
print("Avaliable_color : ", end="")

for key in list(color_preset.keys()):
    print(key, end=" / ")

print()
color1 = input("Player 1 color: ")
color2 = input("Player 2 color: ")

print()
winning_score = int(input("winning score: "))

game = PongPlus(num_balls=2,
                player_names=[name1, name2],
                player_colors=[color_preset[color1], color_preset[color2]],
                winning_score=winning_score)
game.play()
