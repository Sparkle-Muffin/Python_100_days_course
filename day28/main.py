from pathlib import Path
from tkinter import *
import math
import csv
from datetime import date

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Arial"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
BASE_DIR = Path(__file__).parent
tomato_img_path = BASE_DIR / "tomato.png"
work_time_csv_path = BASE_DIR / "work_time.csv"
reps = 0
timer = None
current_count = 0
is_running = False
current_phase = ""
total_work_seconds = 0


def format_total_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def parse_time_to_seconds(time_str):
    try:
        hours_str, minutes_str, seconds_str = time_str.split(":")
        return int(hours_str) * 3600 + int(minutes_str) * 60 + int(seconds_str)
    except (ValueError, AttributeError):
        return 0


def save_work_time_to_csv():
    today = date.today().isoformat()
    work_by_date = {}

    if work_time_csv_path.exists():
        with work_time_csv_path.open("r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                row_date = row.get("Date")
                row_work_time = row.get("Work_Time", "00:00:00")
                if row_date:
                    work_by_date[row_date] = parse_time_to_seconds(row_work_time)

    work_by_date[today] = work_by_date.get(today, 0) + total_work_seconds

    with work_time_csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Date", "Work_Time"])
        for row_date in sorted(work_by_date.keys()):
            writer.writerow([row_date, format_total_time(work_by_date[row_date])])


def on_window_close():
    if timer is not None:
        window.after_cancel(timer)
    save_work_time_to_csv()
    window.destroy()


def update_skip_break_button_visibility():
    if current_phase == "break":
        skip_break_button.grid(column=2, row=4)
    else:
        skip_break_button.grid_remove()


def skip_break():
    global timer
    global current_count
    global is_running

    if current_phase != "break":
        return

    if timer is not None:
        window.after_cancel(timer)
        timer = None

    current_count = 0
    is_running = True
    start_timer()

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps
    global timer
    global current_count
    global is_running
    global current_phase
    global total_work_seconds

    if timer is not None:
        window.after_cancel(timer)
        timer = None

    is_running = False
    current_phase = ""
    current_count = 0
    total_work_seconds = 0
    start_pause_button.config(text="Start")
    canvas.itemconfig(timer_text, text="00:00")
    label_title.config(text="Timer")
    label_total_work_time.config(text="Total Work Time: 00:00:00")
    label_ticks.config(text="")
    reps = 0
    update_skip_break_button_visibility()

# ---------------------------- TIMER TOGGLE ------------------------------- # 
def toggle_timer():
    global timer
    global current_count
    global is_running

    if is_running:
        if timer is not None:
            window.after_cancel(timer)
            timer = None
        is_running = False
        start_pause_button.config(text="Start")
        return

    is_running = True
    start_pause_button.config(text="Pause")
    if current_count > 0:
        count_down(current_count)
    else:
        start_timer()

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    global current_count
    global current_phase
    global is_running

    work_in_sec = WORK_MIN * 60
    short_break_in_sec = SHORT_BREAK_MIN * 60
    long_break_in_sec = LONG_BREAK_MIN * 60

    reps += 1
    if reps % 8 == 0:
        current_count = long_break_in_sec
        current_phase = "break"
        label_title.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        current_count = short_break_in_sec
        current_phase = "break"
        label_title.config(text="Break", fg=PINK)
    else:
        current_count = work_in_sec
        current_phase = "work"
        label_title.config(text="Work", fg=GREEN)
    is_running = True
    start_pause_button.config(text="Pause")
    update_skip_break_button_visibility()
    count_down(current_count)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count, work_second_elapsed=False):
    global reps
    global timer
    global current_count
    global total_work_seconds
    global current_phase

    if work_second_elapsed and current_phase == "work":
        total_work_seconds += 1
        label_total_work_time.config(text=f"Total Work Time: {format_total_time(total_work_seconds)}")

    current_count = count
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = "0" + str(count_sec)
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1, True)
    else:
        timer = None
        start_timer()
        work_sessions = math.floor(reps/2)
        check_marks = ""
        for _ in range(work_sessions):
            check_marks += "✓"
            label_ticks.config(text=check_marks)
        
        window.deiconify()          # restore if minimized
        window.lift()               # bring to front
        window.attributes('-topmost', True)
        window.focus_force()
        window.after(500, lambda: window.attributes('-topmost', False))

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)
window.protocol("WM_DELETE_WINDOW", on_window_close)

label_title = Label(text="Timer", font=(FONT_NAME, 40, "normal"), bg=YELLOW, fg=GREEN)
label_title.grid(column=1, row=0)

canvas = Canvas(width=202, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file=tomato_img_path)
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

label_total_work_time = Label(
    text="Total Work Time: 00:00:00",
    font=(FONT_NAME, 14, "normal"),
    bg=YELLOW,
    fg=GREEN,
)
label_total_work_time.grid(column=1, row=2)

start_pause_button = Button(text="Start", font=(FONT_NAME, 20, "normal"), command=toggle_timer)
start_pause_button.grid(column=0, row=3)

reset_button = Button(text="Reset", font=(FONT_NAME, 20, "normal"), command=reset_timer)
reset_button.grid(column=2, row=3)

skip_break_button = Button(text="Skip Break", font=(FONT_NAME, 14, "normal"), command=skip_break)
skip_break_button.grid(column=2, row=4)
skip_break_button.grid_remove()

label_ticks = Label(font=(FONT_NAME, 20, "normal"), bg=YELLOW, fg=GREEN)
label_ticks.grid(column=1, row=3)

mainloop()
