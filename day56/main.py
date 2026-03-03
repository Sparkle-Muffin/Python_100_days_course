from flask import Flask, render_template

# cd day56/
# flask --app main run --debug

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")
