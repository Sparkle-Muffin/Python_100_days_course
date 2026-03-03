from flask import Flask, render_template
import datetime as dt
import requests
import os

# cd day57/
# flask --app main run --debug

app = Flask(__name__)

@app.route("/")
def main():
    current_year = dt.datetime.now().strftime("%Y")
    name = "Dupa Dupa"
    return render_template("index.html", current_year=current_year, name=name)

@app.route("/guess/<name>")
def guess(name):
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    data = response.json()
    cat_url = data[0]["url"]

    return render_template("guess.html", name=name.title(), cat_url=cat_url)

@app.route("/blog/<num>")
def get_blog(num):
    print(num)
    response = requests.get("https://api.npoint.io/80c175e2c081b664e415")
    data = response.json()
    
    return render_template("blog.html", blog_posts=data)
