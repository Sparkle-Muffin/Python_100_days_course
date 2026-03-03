from tkinter import *
from pathlib import Path
from quiz_brain import QuizBrain


BASE_DIR = Path(__file__).parent
yes_image_path = BASE_DIR / "images" / "true.png"
no_image_path = BASE_DIR / "images" / "false.png"

THEME_COLOR = "#375362"
FONT_SCORE = ("Arial", 10, "normal")
FONT_QUESTION = ("Arial", 15, "italic")
PADDING = 20

class QuizzInterface():
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(bg=THEME_COLOR)

        self.label_score = Label(text="Score: 0/10", font=FONT_SCORE, bg=THEME_COLOR, fg="white")
        self.label_score.grid(column=1, row=0, padx=PADDING, pady=PADDING)

        self.canvas = Canvas(width=300, height=250, highlightthickness=0, bg="white")
        self.question_text = self.canvas.create_text(150, 125, width = 280, font=FONT_QUESTION, fill=THEME_COLOR)
        self.canvas.grid(column=0, row=1, columnspan=2, padx=PADDING, pady=PADDING)

        yes_image = PhotoImage(file=yes_image_path)
        self.yes_button = Button(image=yes_image, highlightthickness=0, command=self.answer_yes)
        self.yes_button.grid(column=0, row=2, padx=PADDING, pady=PADDING)

        no_image = PhotoImage(file=no_image_path)
        self.no_button = Button(image=no_image, highlightthickness=0, command=self.answer_no)
        self.no_button.grid(column=1, row=2, padx=PADDING, pady=PADDING)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz.")
            self.yes_button.config(state="disabled")
            self.no_button.config(state="disabled")

    def answer_yes(self):
        is_right = self.quiz.check_answer("True")
        self.give_feedback(is_right)

    def answer_no(self):
        is_right = self.quiz.check_answer("False")
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        if is_right == True:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.label_score.config(text=f"Score: {self.quiz.score}/{self.quiz.number_of_questions}")
        self.window.after(1000, self.get_next_question)
