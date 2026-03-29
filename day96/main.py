"""
Advice Slip — Flask + Jinja + Bootstrap (day 96).
Run: flask --app main run --debug
"""

import json
import urllib.error
import urllib.request
from typing import Optional, Tuple

from flask import Flask, render_template

ADVICE_API = "https://api.adviceslip.com/advice"

app = Flask(__name__)


def fetch_advice() -> Tuple[Optional[str], Optional[str]]:
    """Returns (advice_text, error_message)."""
    req = urllib.request.Request(
        ADVICE_API,
        headers={"User-Agent": "AdviceSlipApp/1.0 (Flask; educational)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            payload = json.load(resp)
        slip = payload.get("slip") or {}
        text = slip.get("advice")
        if not text:
            return None, "Unexpected response from the advice service."
        return str(text), None
    except urllib.error.HTTPError as e:
        return None, f"The advice service returned an error ({e.code})."
    except urllib.error.URLError as e:
        return None, f"Could not reach the advice service: {e.reason!s}."
    except json.JSONDecodeError:
        return None, "Could not read the advice service response."
    except TimeoutError:
        return None, "The advice service took too long to respond."


@app.route("/")
def index():
    advice, error = fetch_advice()
    return render_template("index.html", advice=advice, error=error)
