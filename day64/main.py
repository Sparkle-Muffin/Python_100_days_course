from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import json
import datetime as dt
import os
from dotenv import load_dotenv
load_dotenv()


# To see a db run this command in Bash: 
# sqlitebrowser
# cd day64
# flask --app main run --debug


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class RateMovieForm(FlaskForm):
    rating = FloatField(label='Your Rating Out Of 10 e.g 7.5', validators=[DataRequired()])
    review = StringField(label='Your Review', validators=[DataRequired()])
    submit = SubmitField(label="Done")

class FindMovieForm(FlaskForm):
    title = StringField(label='Movie Title', validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")

# CREATE DB
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
# initialize the app with the extension
db.init_app(app)

class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[float] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    review: Mapped[str] = mapped_column(String, nullable=True)
    img_url: Mapped[str] = mapped_column(String, nullable=False)

# CREATE TABLE
# Run this code only when creating a new database:
with app.app_context():
    db.create_all()

# with app.app_context():
#     new_movie = Movie(
#         title="Phone Booth",
#         year=2002,
#         description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#         rating=7.3,
#         review="My favourite character was the caller.",
#         img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#     )
#     db.session.add(new_movie)
#     db.session.commit()


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating.desc()))
    all_movies = result.scalars().all()
    for movie in all_movies:
        print(movie.title)

    return render_template("index.html", all_movies=all_movies)


@app.route("/edit/<movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    form = RateMovieForm()
    if form.validate_on_submit():
        result = db.session.execute(db.select(Movie).where(Movie.id==movie_id))
        movie = result.scalar()
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit() 
        
        return redirect(url_for("home"))

    else:
        return render_template("edit.html", form=form)


@app.route("/delete/<movie_id>", methods=["GET", "POST"])
def delete(movie_id):
    result = db.session.execute(db.select(Movie).where(Movie.id==movie_id))
    movie_to_delete = result.scalar()
    db.session.delete(movie_to_delete)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = FindMovieForm()
    if form.validate_on_submit():
        parameters = {
            "query": form.title.data
        }
        headers = {
            "Authorization": f"{os.getenv("TMDB_BEARER_TOKEN")}",
            "accept": "application/json"
            }
        response = requests.get("https://api.themoviedb.org/3/search/movie", params=parameters, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Use for test purposes
        # with open("movie.json") as file:
        #     data = json.load(file)

        all_movies = data["results"]

        for movie in all_movies:
            movie["release_date"] = dt.datetime.fromisoformat(movie["release_date"]).strftime("%Y")

        return render_template("select.html", all_movies=all_movies)
    else:
        return render_template("add.html", form=form)


@app.route("/add_to_db", methods=["POST"])
def add_to_db():
    movie = json.loads(request.form["movie"])
    new_movie = Movie(
        title = movie["title"],
        year = movie["release_date"],
        description = movie["overview"],
        img_url = "https://image.tmdb.org/t/p/original" + movie["poster_path"]
    )
    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for('edit', movie_id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
