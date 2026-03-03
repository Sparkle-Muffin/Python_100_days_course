from flask import Flask, render_template
import requests

# cd day59
# flask --app main run --debug

response = requests.get("https://api.npoint.io/674f5423f73deab1e9a7")
all_posts = response.json()

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html", all_posts=all_posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/post/<post_id>")
def post(post_id):
    post_id = int(post_id) - 1
    post = all_posts[post_id]
    return render_template("post.html", post=post)
