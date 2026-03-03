from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random
import json


# https://chatgpt.com/c/6981f34c-3030-8390-ae22-0e6cf34a2cd1
# To see a db run this command in Bash: 
# sqlitebrowser
# cd day66
# flask --app main run --debug

API_KEY = "TopSecretAPIKey"

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
    @classmethod
    def from_dict(cls, data: dict):
        filtered = {
            c.name: data[c.name]
            for c in cls.__table__.columns
            if c.name in data and c.name != "id"
        }
        return cls(**filtered)
    
    
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)

    return jsonify(random_cafe.to_dict())


# HTTP GET - Read Record
@app.route("/all")
def get_all():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    all_cafes_list = []
    for cafe in all_cafes:
        all_cafes_list.append(cafe.to_dict())

    return jsonify({"cafes": all_cafes_list})


# HTTP GET - Read Record
@app.route("/search")
def get_at_location():
    loc = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location==loc))
    all_cafes = result.scalars().all()
    all_cafes_list = []
    for cafe in all_cafes:
        all_cafes_list.append(cafe.to_dict())

    if len(all_cafes_list) > 0:
        return jsonify({"cafes": all_cafes_list})
    else:
        return jsonify({"error": {"Not Found": "Sorry, we don't have a cefe at that location."}}), 404


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    content = request.json
    new_cafe_json = content["cafe"]
    print(new_cafe_json)

    new_cafe = Cafe.from_dict(new_cafe_json)
    db.session.add(new_cafe)
    db.session.commit()

    return jsonify({"success":"Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    result = db.session.execute(db.select(Cafe).where(Cafe.id==cafe_id))
    try:
        cafe = result.scalars().one()
        print(cafe.coffee_price)
        cafe.coffee_price = new_price
        db.session.commit() 
        return jsonify({"success":"Successfully updated the price."})
    except:
        return jsonify({"error": {"Not Found": "Sorry, a cafe with that id was not found in the database."}}), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key != API_KEY:
        return jsonify({"error": {"Not Found": "Sorry, that's not allowed. Make sure you have the correct api-key."}}), 403
    else:
        result = db.session.execute(db.select(Cafe).where(Cafe.id==cafe_id))
        try:
            cafe_to_delete = result.scalars().one()
            db.session.delete(cafe_to_delete)
            db.session.commit() 
            return jsonify({"success":"Successfully deleted the cafe."})
        except:
            return jsonify({"error": {"Not Found": "Sorry, a cafe with that id was not found in the database."}}), 404
        

if __name__ == '__main__':
    app.run(debug=True)
