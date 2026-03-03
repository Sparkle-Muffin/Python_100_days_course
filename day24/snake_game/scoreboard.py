from turtle import Turtle
from pathlib import Path
import os

base_dir = Path(__file__).parent
HIGH_SCORE_DIR = "/home/pervitin/Desktop/temp/huj.txt"

ALIGNMENT = "center"
FONT = ('Courier', 18, 'normal')

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.pencolor("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 270)
        self.score = 0
        self.high_score = self.read_high_score()
        self.update_scoreboard()

    def read_high_score(self):
        with open(HIGH_SCORE_DIR) as file:
            high_score = int(file.read())
            return high_score

    def save_high_score(self):
        with open(HIGH_SCORE_DIR, mode="w") as file:
            file.write(str(self.high_score))
        
    def update_scoreboard(self):
        self.clear()
        self.write(arg=f"Score: {self.score} High Score: {self.high_score}", align=ALIGNMENT, font=FONT)

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        self.score = 0
        self.update_scoreboard()

    def increase_score(self):
        self.score += 1
        self.update_scoreboard()