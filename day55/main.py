from flask import Flask
import random

# cd day54/
# flask --app main run --debug

number = random.randint(0, 9)
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Guess a number between 0 and 9</h1>"\
    "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'>"

@app.route("/<int:user_number>")
def guess(user_number):
    if user_number < number:
        return "<h1 style='color: red'>Too low, try again!</h1>"\
        "<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'>"
    elif user_number > number:
        return "<h1 style='color: magenta'>Too high, try again!</h1>"\
        "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'>"
    else:
        return "<h1 style='color: green'>You found me!</h1>"\
        "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'>"