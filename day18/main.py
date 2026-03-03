from pathlib import Path
import colorgram
from turtle import Turtle, Screen
import random
import math

####################################################
#         RETRIEVE COLORS FROM THE IMAGE           #
####################################################
BASE_DIR = Path(__file__).parent
image_path = BASE_DIR / "kiss.jpg"

NUBER_OF_COLORS = 30
# Extract n colors from an image.
colors = colorgram.extract(image_path, NUBER_OF_COLORS)

color_list = []
for color in colors:
    color_tuple = color.rgb
    color_list.append(color_tuple)

####################################################
#               DRAW A DOT PAINTING                #
####################################################
screen = Screen()
screen.colormode(255)

timmy = Turtle()
timmy.speed(10)
timmy.hideturtle()

window_width = screen.window_width()
window_height = screen.window_height()
dot_diameter = 20
dot_centers_distance = 2 * dot_diameter

x_dots = math.floor(window_width / dot_centers_distance)
x_start_pos = 0 - ((x_dots + 1) * dot_centers_distance) / 2
y_dots = math.floor(window_height / dot_centers_distance)
y_start_pos = 0 - ((y_dots + 1) * dot_centers_distance) / 2

for row in range(y_dots):
    timmy.teleport(x_start_pos, y_start_pos + (row + 1) * dot_centers_distance)
    for _ in range(x_dots):
        color = random.choice(color_list)
        timmy.color(color)
        timmy.penup()
        timmy.forward(dot_centers_distance)
        timmy.pendown()
        timmy.dot(dot_diameter)

timmy.teleport(0, 0)

screen.exitonclick()
