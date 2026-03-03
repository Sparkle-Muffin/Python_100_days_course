from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from typing import Iterable, Mapping, Any

from flask import Flask, g, render_template, abort


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "portfolio.db")


app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me-in-production"


def get_db() -> sqlite3.Connection:
    """
    Returns a SQLite connection attached to the Flask `g` object.
    Rows are returned as dictionaries for convenient Jinja use.
    """
    if "db" not in g:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(exception: BaseException | None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """
    Initialize the database.

    Call this manually from a Python shell:

    >>> from day83.main import init_db
    >>> init_db()
    """
    schema = """
    CREATE TABLE IF NOT EXISTS projects (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        title           TEXT NOT NULL,
        subtitle        TEXT,
        short_summary   TEXT NOT NULL,
        full_description TEXT,
        tech_stack      TEXT,
        main_tech       TEXT,
        github_url      TEXT,
        demo_url        TEXT,
        featured        INTEGER NOT NULL DEFAULT 0,
        created_at      TEXT NOT NULL
    );
    """
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        conn.executescript(schema)
        conn.commit()
    finally:
        conn.close()


def query_projects(
    sql: str,
    params: Iterable[Any] | Mapping[str, Any] | None = None,
) -> list[sqlite3.Row]:
    db = get_db()
    cursor = db.execute(sql, params or [])
    rows = cursor.fetchall()
    cursor.close()
    return rows


def get_all_projects() -> list[sqlite3.Row]:
    return query_projects(
        """
        SELECT *
        FROM projects
        ORDER BY featured DESC, created_at DESC, id DESC
        """
    )


def get_featured_projects(limit: int = 3) -> list[sqlite3.Row]:
    return query_projects(
        """
        SELECT *
        FROM projects
        WHERE featured = 1
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    )


def get_project_by_id(project_id: int) -> sqlite3.Row | None:
    rows = query_projects(
        """
        SELECT *
        FROM projects
        WHERE id = ?
        """,
        (project_id,),
    )
    return rows[0] if rows else None


@app.context_processor
def inject_now() -> dict[str, Any]:
    """
    Adds `current_year` into all templates.
    """
    return {"current_year": datetime.utcnow().year}


@app.route("/")
def home():
    featured_projects = get_featured_projects()
    all_projects = get_all_projects()
    return render_template(
        "index.html",
        featured_projects=featured_projects,
        all_projects=all_projects,
    )


@app.route("/projects")
def projects():
    all_projects = get_all_projects()
    return render_template("projects.html", all_projects=all_projects)


@app.route("/project/<int:project_id>")
def project_detail(project_id: int):
    project = get_project_by_id(project_id)
    if project is None:
        return abort(404)
    return render_template("project_detail.html", project=project)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# if __name__ == "__main__":
#     app.run(debug=True, port=5003)

