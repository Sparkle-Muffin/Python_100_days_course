import time
from turtle import Screen, Turtle


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_Y_OFFSET = -250
BALL_SPEED = 0.015  # lower is faster; used as sleep delay
BALL_SIZE = 20
BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
BRICK_Y_START = 200
BRICK_GAP_X = 10
BRICK_GAP_Y = 10
LIVES = 3


class Paddle(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=PADDLE_HEIGHT / 20, stretch_len=PADDLE_WIDTH / 20)
        self.penup()
        self.goto(0, PADDLE_Y_OFFSET)

    def move_left(self) -> None:
        new_x = self.xcor() - 30
        min_x = -SCREEN_WIDTH // 2 + PADDLE_WIDTH // 2
        if new_x < min_x:
            new_x = min_x
        self.goto(new_x, self.ycor())

    def move_right(self) -> None:
        new_x = self.xcor() + 30
        max_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
        if new_x > max_x:
            new_x = max_x
        self.goto(new_x, self.ycor())


class Ball(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.shapesize(stretch_wid=BALL_SIZE / 20, stretch_len=BALL_SIZE / 20)
        self.penup()
        self.goto(0, 0)
        self.dx = 4
        self.dy = 4

    def move(self) -> None:
        self.goto(self.xcor() + self.dx, self.ycor() + self.dy)

    def bounce_x(self) -> None:
        self.dx *= -1

    def bounce_y(self) -> None:
        self.dy *= -1

    def reset_position(self) -> None:
        self.goto(0, 0)
        self.bounce_y()


class Brick(Turtle):
    def __init__(self, position: tuple[float, float], color: str) -> None:
        super().__init__()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=BRICK_HEIGHT / 20, stretch_len=BRICK_WIDTH / 20)
        self.penup()
        self.goto(position)


class Scoreboard(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.score = 0
        self.lives = LIVES
        self.hideturtle()
        self.color("white")
        self.penup()
        self.goto(0, SCREEN_HEIGHT // 2 - 40)
        self.update_display()

    def update_display(self) -> None:
        self.clear()
        self.write(
            f"Score: {self.score}   Lives: {self.lives}",
            align="center",
            font=("Courier", 18, "normal"),
        )

    def increase_score(self, points: int = 10) -> None:
        self.score += points
        self.update_display()

    def lose_life(self) -> None:
        self.lives -= 1
        self.update_display()

    def game_over(self, message: str) -> None:
        self.goto(0, 0)
        self.write(
            message,
            align="center",
            font=("Courier", 24, "bold"),
        )


def create_bricks() -> list[Brick]:
    bricks: list[Brick] = []
    colors = ["red", "orange", "yellow", "green", "blue"]

    total_width = BRICK_COLUMNS * BRICK_WIDTH + (BRICK_COLUMNS - 1) * BRICK_GAP_X
    start_x = -total_width / 2 + BRICK_WIDTH / 2

    for row in range(BRICK_ROWS):
        y = BRICK_Y_START - row * (BRICK_HEIGHT + BRICK_GAP_Y)
        color = colors[row % len(colors)]
        for col in range(BRICK_COLUMNS):
            x = start_x + col * (BRICK_WIDTH + BRICK_GAP_X)
            brick = Brick((x, y), color)
            bricks.append(brick)

    return bricks


def ball_hits_paddle(ball: Ball, paddle: Paddle) -> bool:
    if ball.ycor() < PADDLE_Y_OFFSET + PADDLE_HEIGHT and ball.ycor() > PADDLE_Y_OFFSET:
        if abs(ball.xcor() - paddle.xcor()) < PADDLE_WIDTH / 2:
            return True
    return False


def ball_hits_brick(ball: Ball, brick: Brick) -> bool:
    return (
        abs(ball.xcor() - brick.xcor()) < BRICK_WIDTH / 2
        and abs(ball.ycor() - brick.ycor()) < BRICK_HEIGHT / 2
    )


def main() -> None:
    screen = Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.bgcolor("black")
    screen.title("Breakout - Day 87")
    screen.tracer(0)

    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    scoreboard = Scoreboard()

    screen.listen()
    screen.onkeypress(paddle.move_left, "Left")
    screen.onkeypress(paddle.move_right, "Right")
    screen.onkeypress(paddle.move_left, "a")
    screen.onkeypress(paddle.move_right, "d")

    game_is_on = True

    while game_is_on:
        time.sleep(BALL_SPEED)
        screen.update()
        ball.move()

        if ball.xcor() > SCREEN_WIDTH / 2 - BALL_SIZE / 2 or ball.xcor() < -SCREEN_WIDTH / 2 + BALL_SIZE / 2:
            ball.bounce_x()

        if ball.ycor() > SCREEN_HEIGHT / 2 - BALL_SIZE / 2:
            ball.bounce_y()

        if ball_hits_paddle(ball, paddle) and ball.dy < 0:
            ball.bounce_y()
            offset = (ball.xcor() - paddle.xcor()) / (PADDLE_WIDTH / 2)
            ball.dx = 4 * offset

        for brick in bricks[:]:
            if ball_hits_brick(ball, brick):
                brick.goto(1000, 1000)
                bricks.remove(brick)
                scoreboard.increase_score(10)
                ball.bounce_y()
                break

        if ball.ycor() < -SCREEN_HEIGHT / 2:
            scoreboard.lose_life()
            if scoreboard.lives <= 0:
                scoreboard.game_over("GAME OVER")
                game_is_on = False
            else:
                ball.reset_position()
                paddle.goto(0, PADDLE_Y_OFFSET)
                time.sleep(1)

        if not bricks:
            scoreboard.game_over("YOU WIN!")
            game_is_on = False

    # Keep the window open until the user clicks.
    screen.exitonclick()


if __name__ == "__main__":
    main()

