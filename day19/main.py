from turtle import Turtle, Screen
import random

screen = Screen()
screen.setup(width=500, height=400)

user_input = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")
colors = ["red", "orange", "yellow", "green", "blue", "purple"]

offset = 0
turtles = []
for color in colors:
    tim = Turtle(shape="turtle")
    tim.color(color)
    tim.penup()
    tim.goto(-230, -100 + offset)
    turtles.append(tim)
    offset += 40

finish = 230
race_is_underway = True
while race_is_underway:
    for turtle in turtles:
        random_distance = random.randint(0, 10)
        turtle.forward(random_distance)
        if turtle.xcor() >= finish:
            race_is_underway = False
            winner = turtle.pencolor()
            if winner == user_input:
                print(f"You won! The winner is {winner} turtle.")
            else:
                print(f"You lost! The winner is {winner} turtle.")

screen.exitonclick()
