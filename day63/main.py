from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, Float, VARCHAR

# To see a db run this command in Bash: 
# sqlitebrowser
# cd day63
# flask --app main run --debug

# 0) Init Flask
app = Flask(__name__)

# 1) Init SQLAlchemy
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# initialize the app with the extension
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(VARCHAR(250), nullable=False)
    review: Mapped[float] = mapped_column(Float, nullable=False)

# Run this code only when creating a new database:
# with app.app_context():
#     db.create_all()

# with app.app_context():
#     new_book = Book(
#         id = 1,
#         title = "Harry Potter",
#         author = "J. K. Rowling",
#         review = 9.3
#     )
#     db.session.add(new_book)
#     db.session.commit()


# 2) Run app
@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()

    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template('add.html')
    
    elif request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        review = float(request.form["review"])
        new_book = Book(title=title, author=author, review=review)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for("home"))


@app.route("/edit_rating/<book_id>", methods=["GET", "POST"])
def edit_rating(book_id):
    if request.method == "GET":
        result = db.session.execute(db.select(Book).where(Book.id==book_id))
        book = result.scalars().one()
        print(book.title)

        return render_template('edit_rating.html', book=book)
    
    elif request.method == "POST":
        new_rating = request.form["new_rating"]
        book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
        book_to_update.review = new_rating
        db.session.commit() 

        return redirect(url_for("home"))
    

@app.route("/delete/<book_id>")
def delete(book_id):
    book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    # or book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for("home"))
