from turtle import Turtle

class UsaState(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.speed("fastest")

    def write_name(self, state_name, x_coor, y_coor):
        self.goto(x_coor, y_coor)
        self.write(state_name, align="left", font=('Arial', 8, 'normal'))
        