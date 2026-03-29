"""
Serpentarium — demo sklep z mockiem płatności i kontami klientów (dzień 97).

Katalog: ./input/<slug> (description.txt + jeden plik .jpg).

Baza: SQLite w ./instance/serpentarium.db (SQLAlchemy).

Zainstaluj: flask sqlalchemy flask-sqlalchemy
  (hasła: werkzeug jest w zestawie z Flask).

Uruchom: flask --app main run --debug
"""

from __future__ import annotations

import functools
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)

app = Flask(__name__, instance_path=str(INSTANCE_DIR))
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-insecure-change-for-production")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{INSTANCE_DIR / 'serpentarium.db'}",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    orders = db.relationship("Order", backref="user", lazy="dynamic")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    product_id = db.Column(db.String(128), nullable=False)
    product_name = db.Column(db.String(256), nullable=False)
    price_cents = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(32), nullable=False)
    delivery_method = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


PAYMENT_METHODS: dict[str, str] = {
    "card": "Karta płatnicza (symulacja)",
    "blik": "BLIK (symulacja)",
    "transfer": "Przelew bankowy (symulacja)",
}

DELIVERY_METHODS: dict[str, str] = {
    "courier": "Kurier (1–2 dni robocze)",
    "pickup": "Odbiór osobisty — punkt Serpentarium",
    "parcel_locker": "Paczkomat (symulacja)",
}


def _slug_to_label(slug: str) -> str:
    return re.sub(r"[_-]+", " ", slug).strip().title()


def _assign_price_cents(slugs: list[str]) -> dict[str, int]:
    ordered = sorted(slugs)
    return {s: 12_900 + i * 4_500 for i, s in enumerate(ordered)}


def load_catalog() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    if not INPUT_DIR.is_dir():
        return [], {}

    raw: list[tuple[str, Path]] = []
    for entry in INPUT_DIR.iterdir():
        if entry.is_dir():
            raw.append((entry.name, entry))

    if not raw:
        return [], {}

    slugs = [name for name, _ in raw]
    prices = _assign_price_cents(slugs)
    products: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}

    for slug, folder in sorted(raw, key=lambda x: x[0]):
        desc_path = folder / "description.txt"
        if not desc_path.is_file():
            continue
        jpgs = sorted(folder.glob("*.jpg"))
        if not jpgs:
            continue

        description = desc_path.read_text(encoding="utf-8").strip()
        short_len = 220
        short = description if len(description) <= short_len else description[: short_len - 1] + "…"

        prod = {
            "id": slug,
            "name": _slug_to_label(slug),
            "description": description,
            "short_description": short,
            "price_cents": prices[slug],
            "image_file": jpgs[0].name,
        }
        products.append(prod)
        by_id[slug] = prod

    return products, by_id


CATALOG, PRODUCTS_BY_ID = load_catalog()


def get_current_user() -> User | None:
    uid = session.get("user_id")
    if not uid:
        return None
    return db.session.get(User, uid)


def login_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if get_current_user() is None:
            flash("Zaloguj się, aby kontynuować.", "warning")
            return redirect(url_for("login", next=request.url))
        return view(*args, **kwargs)

    return wrapped


@app.context_processor
def inject_shop():
    return {
        "current_user": get_current_user(),
        "payment_methods": PAYMENT_METHODS,
        "delivery_methods": DELIVERY_METHODS,
    }


@app.route("/")
def index():
    return render_template("index.html", products=CATALOG)


@app.route("/product/<product_id>")
def product_detail(product_id: str):
    prod = PRODUCTS_BY_ID.get(product_id)
    if prod is None:
        abort(404)
    return render_template("product.html", product=prod)


@app.route("/input/<slug>/<path:filename>")
def catalog_asset(slug: str, filename: str):
    if slug not in PRODUCTS_BY_ID:
        abort(404)
    folder = INPUT_DIR / slug
    if not folder.is_dir():
        abort(404)
    return send_from_directory(folder, filename)


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _normalize_email(value: str) -> str:
    return value.strip().lower()


@app.route("/register", methods=["GET", "POST"])
def register():
    if get_current_user() is not None:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = _normalize_email(request.form.get("email", ""))
        password = request.form.get("password", "")
        password2 = request.form.get("password_confirm", "")

        if not email or not _EMAIL_RE.match(email):
            flash("Podaj poprawny adres e-mail.", "danger")
        elif len(password) < 6:
            flash("Hasło musi mieć co najmniej 6 znaków.", "danger")
        elif password != password2:
            flash("Hasła nie są takie same.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("Konto z tym adresem już istnieje.", "warning")
        else:
            user = User(email=email, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            flash("Konto utworzone. Witamy w Serpentarium.", "success")
            return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if get_current_user() is not None:
        return redirect(url_for("index"))

    next_url = request.args.get("next", "")

    if request.method == "POST":
        next_url = request.form.get("next", "") or next_url
        email = _normalize_email(request.form.get("email", ""))
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first() if email else None

        if user is None or not check_password_hash(user.password_hash, password):
            flash("Nieprawidłowy e-mail lub hasło.", "danger")
        else:
            session["user_id"] = user.id
            flash("Zalogowano.", "success")
            if next_url and next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)
            return redirect(url_for("index"))

    return render_template("login.html", next_url=next_url)


@app.get("/logout")
def logout():
    session.pop("user_id", None)
    flash("Wylogowano.", "info")
    return redirect(url_for("index"))


@app.route("/checkout/<product_id>", methods=["GET", "POST"])
@login_required
def checkout(product_id: str):
    prod = PRODUCTS_BY_ID.get(product_id)
    if prod is None:
        abort(404)

    if request.method == "POST":
        payment = request.form.get("payment_method", "")
        delivery = request.form.get("delivery_method", "")
        if payment not in PAYMENT_METHODS or delivery not in DELIVERY_METHODS:
            flash("Wybierz metodę płatności i dostawy.", "warning")
            return redirect(url_for("checkout", product_id=product_id))

        user = get_current_user()
        assert user is not None
        order = Order(
            user_id=user.id,
            product_id=prod["id"],
            product_name=prod["name"],
            price_cents=prod["price_cents"],
            payment_method=payment,
            delivery_method=delivery,
        )
        db.session.add(order)
        db.session.commit()
        flash("Zamówienie zapisane. Płatność i logistyka są tylko symulowane.", "success")
        return redirect(url_for("order_confirmation", order_id=order.id))

    return render_template("checkout.html", product=prod)


@app.get("/order/<int:order_id>")
@login_required
def order_confirmation(order_id: int):
    user = get_current_user()
    order = db.session.get(Order, order_id)
    if order is None or user is None or order.user_id != user.id:
        abort(404)
    return render_template("order_confirmation.html", order=order)


with app.app_context():
    db.create_all()
