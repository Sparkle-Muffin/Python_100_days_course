from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from datetime import datetime


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me-in-production"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kanban.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="todo")
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f"<Task {self.id} {self.title!r} ({self.status})>"


def _next_position_for_status(status: str) -> int:
    last_task = (
        db.session.execute(
            db.select(Task)
            .where(Task.status == status)
            .order_by(Task.position.desc())
        )
        .scalars()
        .first()
    )
    if last_task is None:
        return 1
    return (last_task.position or 0) + 1


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    tasks = db.session.execute(
        db.select(Task).order_by(Task.status, Task.position, Task.created_at)
    ).scalars().all()

    columns = {
        "todo": [],
        "in_progress": [],
        "done": [],
    }

    for task in tasks:
        if task.status not in columns:
            columns.setdefault(task.status, [])
        columns[task.status].append(task)

    return render_template("index.html", columns=columns)


@app.route("/task/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    initial_status = request.form.get("status", "todo").strip() or "todo"

    if not title:
        flash("Title is required.", "danger")
        return redirect(url_for("index"))

    if initial_status not in {"todo", "in_progress", "done"}:
        initial_status = "todo"

    new_task = Task(
        title=title,
        description=description or None,
        status=initial_status,
        position=_next_position_for_status(initial_status),
        created_at=datetime.utcnow().isoformat(timespec="seconds"),
    )
    db.session.add(new_task)
    db.session.commit()

    flash("Task created.", "success")
    return redirect(url_for("index"))


@app.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id: int):
    task = db.session.get(Task, task_id)
    if task is None:
        flash("Task not found.", "warning")
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", task.status).strip() or task.status

        if not title:
            flash("Title is required.", "danger")
            return redirect(url_for("edit_task", task_id=task.id))

        if status not in {"todo", "in_progress", "done"}:
            status = task.status

        if status != task.status:
            task.status = status
            task.position = _next_position_for_status(status)

        task.title = title
        task.description = description or None

        db.session.commit()
        flash("Task updated.", "success")
        return redirect(url_for("index"))

    return render_template("edit_task.html", task=task)


@app.route("/task/<int:task_id>/move", methods=["POST"])
def move_task(task_id: int):
    task = db.session.get(Task, task_id)
    if task is None:
        flash("Task not found.", "warning")
        return redirect(url_for("index"))

    new_status = request.form.get("new_status", "").strip()
    if new_status not in {"todo", "in_progress", "done"}:
        flash("Invalid target column.", "danger")
        return redirect(url_for("index"))

    if new_status != task.status:
        task.status = new_status
        task.position = _next_position_for_status(new_status)
        db.session.commit()
        flash("Task moved.", "success")

    return redirect(url_for("index"))


@app.route("/task/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id: int):
    task = db.session.get(Task, task_id)
    if task is None:
        flash("Task not found.", "warning")
        return redirect(url_for("index"))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

