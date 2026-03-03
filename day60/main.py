from flask import Flask, render_template, request
import requests
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

# cd day60
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


@app.route("/post/<post_id>")
def post(post_id):
    post_id = int(post_id) - 1
    post = all_posts[post_id]
    return render_template("post.html", post=post)


def send_email(title, body):
    my_email = os.getenv("MY_EMAIL")
    app_password = os.getenv("APP_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    print(my_email)
    print(app_password)
    print(recipient_email)

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=app_password)
        connection.sendmail(from_addr=my_email, 
                            to_addrs=recipient_email, 
                            msg=f"Subject:{title}\n\n{body}")


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "GET":
        return render_template("contact.html")
    
    elif request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        mail_title = f"{name} from Clean Blog"
        mail_body = f"{message}\n\n"     \
                    f"e-mail: {email}\n\n" \
                    f"phone: {phone}"
        send_email(mail_title, mail_body)

        return render_template("contact.html", message_sent=True)
