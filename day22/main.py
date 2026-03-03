from turtle import Screen
import time
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard

L_PADDLE_POSITION = (-350, 0)
R_PADDLE_POSITION = (350, 0)

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)
l_paddle = Paddle(L_PADDLE_POSITION)
r_paddle = Paddle(R_PADDLE_POSITION)
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(fun=l_paddle.up, key="w")
screen.onkey(fun=l_paddle.down, key="s")
screen.onkey(fun=r_paddle.up, key="Up")
screen.onkey(fun=r_paddle.down, key="Down")

game_is_on = True
while game_is_on == True:
    screen.update()
    time.sleep(ball.move_speed)
    ball.move()

    # Detect collision with a wall.
    if ball.ycor() > 280 or ball.ycor() < - 280:
        ball.bounce_y()

    # Detect collision with a paddle.
    if ball.distance(l_paddle) < 50 and ball.xcor() < -320 or ball.distance(r_paddle) < 50 and ball.xcor() > 342:
        ball.bounce_x()

    # Detect L paddle misses.
    if ball.xcor() < -380:
        scoreboard.r_point()
        ball.reset_position()

    # Detect R paddle misses.
    if ball.xcor() > 380:
        scoreboard.l_point()
        ball.reset_position()

screen.exitonclick()
