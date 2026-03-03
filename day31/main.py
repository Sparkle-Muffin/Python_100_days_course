from pathlib import Path
from tkinter import *
import pandas as pd
import random

BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
DATA_DIR = BASE_DIR / "data"
card_front_path = IMAGES_DIR / "card_front.png"
card_back_path = IMAGES_DIR / "card_back.png"
wrong_sign_path = IMAGES_DIR / "wrong.png"
right_sign_path = IMAGES_DIR / "right.png"
french_words_path = DATA_DIR / "french_words.csv"
words_to_learn_path = DATA_DIR / "words_to_learn.csv"

BACKGROUND_COLOR = "#B1DDC6"

new_word = None

# ---------------------------- LOAD WORD DATABASE ------------------------------- #
try:
    words_df = pd.read_csv(words_to_learn_path)
except:
    words_df = pd.read_csv(french_words_path)
words_dict = words_df.to_dict(orient="records")

# ---------------------------- FLIP CARD ------------------------------- #
def flip_card(new_word_english):
    canvas.itemconfig(card_img, image=card_back) 
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=new_word_english, fill="white")

# ---------------------------- PICK NEW WORD ------------------------------- #
def next_card():
    global new_word
    if next_card.timer != None:
        window.after_cancel(next_card.timer)
    new_word = random.choice(words_dict)
    new_word_french = new_word["French"]
    new_word_english = new_word["English"]
    canvas.itemconfig(card_img, image=card_front) 
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=new_word_french, fill="black")
    next_card.timer = window.after(3000, flip_card, new_word_english)

next_card.timer = None

# ---------------------------- REMOVE CARD ------------------------------- #
def remove_card():
    global new_word
    words_dict.remove(new_word)
    next_card()

# ---------------------------- SAVE UNKNOWN WORDS ------------------------------- #
def save_unknown_words():
    unknown_words_df = pd.DataFrame(words_dict)
    unknown_words_df.to_csv(words_to_learn_path, index=False)
    window.destroy()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file=card_front_path)
card_back = PhotoImage(file=card_back_path)
card_img = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, font=("Arial", 40, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

wrong_sign_image = PhotoImage(file=wrong_sign_path)
wrong_sign_button = Button(image=wrong_sign_image, highlightthickness=0, command=next_card)
wrong_sign_button.grid(column=0, row=1)

right_sign_image = PhotoImage(file=right_sign_path)
right_sign_button = Button(image=right_sign_image, highlightthickness=0, command=remove_card)
right_sign_button.grid(column=1, row=1)

next_card()

window.wm_protocol("WM_DELETE_WINDOW", save_unknown_words)
mainloop()
