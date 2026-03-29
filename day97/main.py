"""
Serpentarium — demo e‑commerce with Flask + Stripe Checkout (day 97).

Catalogue is read from ./input/<slug> (description.txt + one .jpg per species).

Environment:
  STRIPE_SECRET_KEY   — Stripe secret key (sk_test_… or sk_live_…)
  PUBLIC_BASE_URL     — Optional. Public URL of this app, e.g. https://abc.ngrok.io
                        Used for Stripe success/cancel redirects. Defaults to request.url_root.
  FLASK_SECRET_KEY    — Optional. For flash messages; defaults to an insecure dev value.

Do not commit real API keys.

Run (after installing deps): flask --app main run --debug
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import stripe

try:
    StripeError = stripe.StripeError
except AttributeError:  # older stripe-python
    StripeError = stripe.error.StripeError  # type: ignore[attr-defined]

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-insecure-change-for-production")


def _slug_to_label(slug: str) -> str:
    return re.sub(r"[_-]+", " ", slug).strip().title()


def _assign_price_cents(slugs: list[str]) -> dict[str, int]:
    """Test-only prices in PLN grosze (smallest currency unit)."""
    ordered = sorted(slugs)
    return {s: 12_900 + i * 4_500 for i, s in enumerate(ordered)}


def load_catalog() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Build product list and id → product map from input/."""
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


def _public_base_url() -> str:
    base = os.environ.get("PUBLIC_BASE_URL", "").strip().rstrip("/")
    if base:
        return base
    return request.url_root.rstrip("/")


def _configure_stripe() -> bool:
    key = os.environ.get("STRIPE_SECRET_KEY", "").strip()
    if not key:
        return False
    stripe.api_key = key
    return True


def _checkout_email(customer_details: Any) -> str | None:
    if not customer_details:
        return None
    if isinstance(customer_details, dict):
        return customer_details.get("email")
    return getattr(customer_details, "email", None)


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


@app.post("/create-checkout-session")
def create_checkout_session():
    if not _configure_stripe():
        flash("Stripe nie jest skonfigurowany: ustaw zmienną STRIPE_SECRET_KEY.", "danger")
        pid = request.form.get("product_id", "")
        if pid in PRODUCTS_BY_ID:
            return redirect(url_for("product_detail", product_id=pid))
        return redirect(url_for("index"))

    product_id = request.form.get("product_id", "")
    prod = PRODUCTS_BY_ID.get(product_id)
    if prod is None:
        flash("Nieznany produkt.", "warning")
        return redirect(url_for("index"))

    base = _public_base_url()
    try:
        checkout_session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[
                {
                    "quantity": 1,
                    "price_data": {
                        "currency": "pln",
                        "unit_amount": prod["price_cents"],
                        "product_data": {
                            "name": prod["name"],
                            "description": prod["short_description"][:500],
                            "images": [
                                f"{base}{url_for('catalog_asset', slug=prod['id'], filename=prod['image_file'])}"
                            ],
                        },
                    },
                }
            ],
            success_url=base + url_for("checkout_success") + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=base + url_for("checkout_cancel"),
            metadata={"product_id": prod["id"]},
        )
    except StripeError as e:
        flash(f"Błąd Stripe: {getattr(e, 'user_message', None) or str(e)}", "danger")
        return redirect(url_for("product_detail", product_id=product_id))

    return redirect(checkout_session.url, code=303)


@app.route("/success")
def checkout_success():
    session_id = request.args.get("session_id", "").strip()
    session_data: dict[str, Any] | None = None
    if session_id and _configure_stripe():
        try:
            sess = stripe.checkout.Session.retrieve(session_id)
            details = sess.get("customer_details")
            session_data = {
                "payment_status": sess.get("payment_status"),
                "customer_email": _checkout_email(details),
                "amount_total": sess.get("amount_total"),
                "currency": (sess.get("currency") or "").upper(),
            }
        except StripeError:
            session_data = None
    return render_template("success.html", session=session_data)


@app.route("/cancel")
def checkout_cancel():
    return render_template("cancel.html")

