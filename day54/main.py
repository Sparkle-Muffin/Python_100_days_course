from flask import Flask
from markupsafe import escape

# cd day54/
# flask --app main run --debug

def make_bold(func):
    def wrapper():
        string = func()
        return f"<b>{string}</b>"
    
    return wrapper

def make_emphasis(func):
    def wrapper():
        string = func()
        return f"<em>{string}</em>"
    
    return wrapper

def make_underlined(func):
    def wrapper():
        string = func()
        return f"<u>{string}</u>"
    
    return wrapper

app = Flask(__name__)

@app.route("/")
def hello_world():
    # return "<p>Hello, Worlxd!</p>"
    return "guwno"

@app.route("/users/<name>")
def show_user_profile(name):
    return f"<p>Hello, {escape(name)}!</p>"

@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def bye():
    return f"Bye!"