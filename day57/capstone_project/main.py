from flask import Flask, render_template
import requests

# cd day57/capstone_project
# flask --app main run --debug

response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
blog_posts = response.json()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", blog_posts=blog_posts)

@app.route("/post/<post_id>")
def get_post(post_id):
    post = blog_posts[int(post_id)-1]
    return render_template("post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)
