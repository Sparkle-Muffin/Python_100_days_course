from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime as dt


# https://chatgpt.com/c/6983071c-5c2c-8332-9fbf-fad8d4076e74
# To see a db run this command in Bash: 
# sqlitebrowser
# cd day67
# flask --app main run --debug


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


class NewPostForm(FlaskForm):
    title = StringField(label='New Post Title', validators=[DataRequired()])
    subtitle = StringField(label='Subtitle', validators=[DataRequired()])
    author = StringField(label='Your Name', validators=[DataRequired()])
    img_url = StringField(label='Blog Image URL', validators=[DataRequired(), URL()])
    body = CKEditorField(label='Blog Content', validators=[DataRequired()])
    submit = SubmitField(label="Submit Post")


# INITIALIZE CKEditor
ckeditor = CKEditor(app)


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    all_posts = result.scalars().all()
    return render_template("index.html", all_posts=all_posts)


@app.route('/show_post/<post_id>')
def show_post(post_id):
    result = db.session.execute(db.select(BlogPost).where(BlogPost.id==post_id))
    requested_post = result.scalars().one()
    return render_template("post.html", post=requested_post)


@app.route('/new-post', methods=["GET", "POST"])
def make_new_post():
    form = NewPostForm()
    now = dt.datetime.now()
    date = now.strftime("%B %d, %Y")
    if form.validate_on_submit():
        new_post = BlogPost(
            title = form.title.data,
            subtitle = form.subtitle.data,
            date = date,
            author = form.author.data,
            img_url = form.img_url.data,
            body = form.body.data,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    else:
        return render_template("make-post.html", form=form)


@app.route('/edit-post/<post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    form = NewPostForm()
    result = db.session.execute(db.select(BlogPost).where(BlogPost.id==post_id))
    requested_post = result.scalars().one()
    if form.validate_on_submit():

        requested_post.title = form.title.data
        requested_post.subtitle = form.subtitle.data
        requested_post.author = form.author.data
        requested_post.img_url = form.img_url.data
        requested_post.body = form.body.data

        db.session.add(requested_post)
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))
    else:
        form = NewPostForm(
            title = requested_post.title,
            subtitle = requested_post.subtitle,
            img_url = requested_post.img_url,
            author = requested_post.author,
            body = requested_post.body
        )
        return render_template("make-post.html", form=form, is_edit=True)
    

@app.route('/delete_post/<post_id>')
def delete_post(post_id):
    result = db.session.execute(db.select(BlogPost).where(BlogPost.id==post_id))
    post_to_delete = result.scalar()
    db.session.delete(post_to_delete)
    db.session.commit()

    return redirect(url_for("get_all_posts"))


# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
