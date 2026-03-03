import random
import tkinter as tk
from tkinter import messagebox


LANG_STRINGS = {
    "en": {
        "title": "Typing speed test",
        "language_label": "Language:",
        "time_label": "Test time:",
        "start_button": "Start test",
        "reset_button": "Reset",
        "timer_prefix": "Time left:",
        "seconds_suffix": "s",
        "text_to_type": "Text to type:",
        "your_input": "Your input:",
        "results_title": "Results",
        "results_template": (
            "Time: {seconds}s\n"
            "Words typed: {words_typed}\n"
            "Correct words: {correct_words}\n"
            "Accuracy: {accuracy:.1f}%\n"
            "Speed: {wpm:.1f} wpm"
        ),
        "info_not_running": "The test is not running.",
        "info_choose_options": "Choose language and time, then press 'Start test'.",
    },
    "pl": {
        "title": "Test szybkości pisania",
        "language_label": "Język:",
        "time_label": "Czas testu:",
        "start_button": "Start",
        "reset_button": "Resetuj",
        "timer_prefix": "Pozostały czas:",
        "seconds_suffix": "s",
        "text_to_type": "Tekst do przepisania:",
        "your_input": "Twój tekst:",
        "results_title": "Wyniki",
        "results_template": (
            "Czas: {seconds}s\n"
            "Napisane słowa: {words_typed}\n"
            "Poprawne słowa: {correct_words}\n"
            "Dokładność: {accuracy:.1f}%\n"
            "Szybkość: {wpm:.1f} słów/min"
        ),
        "info_not_running": "Test nie jest uruchomiony.",
        "info_choose_options": "Wybierz język i czas, a potem naciśnij 'Start'.",
    },
}


# Short base lists of common words for each language.
# The application expands them internally to reach 1000 items.
BASE_WORDS_EN = [
    "the",
    "be",
    "to",
    "of",
    "and",
    "a",
    "in",
    "that",
    "have",
    "I",
    "it",
    "for",
    "not",
    "on",
    "with",
    "he",
    "as",
    "you",
    "do",
    "at",
    "this",
    "but",
    "his",
    "by",
    "from",
    "they",
    "we",
    "say",
    "her",
    "she",
    "or",
    "an",
    "will",
    "my",
    "one",
    "all",
    "would",
    "there",
    "their",
    "what",
    "so",
    "up",
    "out",
    "if",
    "about",
    "who",
    "get",
    "which",
    "go",
    "me",
    "when",
    "make",
    "can",
    "like",
    "time",
    "no",
    "just",
    "him",
    "know",
    "take",
    "people",
    "into",
    "year",
    "your",
    "good",
    "some",
    "could",
    "them",
    "see",
    "other",
    "than",
    "then",
    "now",
    "look",
    "only",
    "come",
    "its",
    "over",
    "think",
    "also",
    "back",
    "after",
    "use",
    "two",
    "how",
    "our",
    "work",
    "first",
    "well",
    "way",
    "even",
    "new",
    "want",
    "because",
    "any",
    "these",
    "give",
    "day",
    "most",
    "us",
]

BASE_WORDS_PL = [
    "i",
    "w",
    "nie",
    "to",
    "na",
    "się",
    "że",
    "z",
    "do",
    "jest",
    "co",
    "jak",
    "o",
    "ale",
    "tak",
    "dla",
    "po",
    "go",
    "za",
    "jakie",
    "czy",
    "ty",
    "ja",
    "on",
    "ona",
    "my",
    "wy",
    "oni",
    "być",
    "mieć",
    "który",
    "które",
    "która",
    "te",
    "ten",
    "ta",
    "jestem",
    "jesteś",
    "jest",
    "jesteśmy",
    "jesteście",
    "są",
    "był",
    "była",
    "było",
    "byli",
    "tu",
    "tam",
    "jeszcze",
    "bardzo",
    "dobry",
    "dobra",
    "dobre",
    "dobrze",
    "kiedy",
    "teraz",
    "potem",
    "już",
    "więc",
    "może",
    "muszę",
    "chcę",
    "trzeba",
    "można",
    "czego",
    "nic",
    "wszystko",
    "wszyscy",
    "kto",
    "gdzie",
    "dlaczego",
    "ponieważ",
    "przez",
    "przed",
    "nad",
    "pod",
    "między",
    "bez",
    "także",
    "również",
    "zawsze",
    "często",
    "czasem",
    "nigdy",
    "dzisiaj",
    "jutro",
    "wczoraj",
    "dom",
    "dzień",
    "czas",
    "człowiek",
    "rok",
    "ręka",
    "oczko",
    "głowa",
    "noc",
]


def expand_to_1000(base_list):
    """Return a list of at least 1000 items based on base_list."""
    if len(base_list) >= 1000:
        return base_list[:1000]

    words = []
    index = 0
    while len(words) < 1000:
        words.append(base_list[index % len(base_list)])
        index += 1
    return words


WORDS_EN = expand_to_1000(BASE_WORDS_EN)
WORDS_PL = expand_to_1000(BASE_WORDS_PL)


class TypingSpeedTestApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.language = tk.StringVar(value="en")
        self.test_time = tk.IntVar(value=30)

        self.remaining_seconds = 0
        self.timer_id = None
        self.test_running = False
        self.reference_text = ""

        self._build_ui()
        self._apply_language()

    # UI construction -------------------------------------------------
    def _build_ui(self) -> None:
        self.root.geometry("900x600")

        # Top frame for controls
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(fill="x")

        # Language selection
        self.language_label = tk.Label(control_frame, text="")
        self.language_label.grid(row=0, column=0, sticky="w")

        lang_frame = tk.Frame(control_frame)
        lang_frame.grid(row=0, column=1, sticky="w", padx=(5, 20))

        self.lang_radio_en = tk.Radiobutton(
            lang_frame, text="English", variable=self.language, value="en", command=self._apply_language
        )
        self.lang_radio_pl = tk.Radiobutton(
            lang_frame, text="Polski", variable=self.language, value="pl", command=self._apply_language
        )
        self.lang_radio_en.pack(side="left")
        self.lang_radio_pl.pack(side="left", padx=(5, 0))

        # Time selection
        self.time_label = tk.Label(control_frame, text="")
        self.time_label.grid(row=1, column=0, sticky="w", pady=(5, 0))

        time_frame = tk.Frame(control_frame)
        time_frame.grid(row=1, column=1, sticky="w", padx=(5, 20), pady=(5, 0))

        self.time_radio_30 = tk.Radiobutton(
            time_frame, text="30 s", variable=self.test_time, value=30
        )
        self.time_radio_60 = tk.Radiobutton(
            time_frame, text="60 s", variable=self.test_time, value=60
        )
        self.time_radio_30.pack(side="left")
        self.time_radio_60.pack(side="left", padx=(5, 0))

        # Timer label
        self.timer_label = tk.Label(control_frame, text="", font=("Helvetica", 14, "bold"))
        self.timer_label.grid(row=0, column=2, rowspan=2, sticky="e", padx=(20, 0))

        # Buttons
        button_frame = tk.Frame(control_frame)
        button_frame.grid(row=0, column=3, rowspan=2, sticky="e", padx=(20, 0))

        self.start_button = tk.Button(button_frame, text="", command=self.start_test, width=12)
        self.start_button.pack(side="top", pady=(0, 5))

        self.reset_button = tk.Button(button_frame, text="", command=self.reset_test, width=12)
        self.reset_button.pack(side="top")

        control_frame.grid_columnconfigure(2, weight=1)

        # Text to type
        text_frame = tk.Frame(self.root, padx=10, pady=10)
        text_frame.pack(fill="both", expand=True)

        self.text_to_type_label = tk.Label(text_frame, text="")
        self.text_to_type_label.pack(anchor="w")

        self.text_display = tk.Text(
            text_frame,
            height=7,
            wrap="word",
            padx=5,
            pady=5,
            state="disabled",
            bg="#f5f5f5",
        )
        self.text_display.pack(fill="both", expand=False)

        # User input
        self.your_input_label = tk.Label(text_frame, text="")
        self.your_input_label.pack(anchor="w", pady=(10, 0))

        self.input_text = tk.Text(
            text_frame,
            height=7,
            wrap="word",
            padx=5,
            pady=5,
        )
        self.input_text.pack(fill="both", expand=True)

        # Results
        self.results_label = tk.Label(self.root, text="", justify="left", padx=10, pady=10)
        self.results_label.pack(fill="x", anchor="w")

        # Info label
        self.info_label = tk.Label(self.root, text="", padx=10, pady=5, fg="#555555")
        self.info_label.pack(fill="x", anchor="w")

    # Internationalisation --------------------------------------------
    def _apply_language(self) -> None:
        lang = self.language.get()
        strings = LANG_STRINGS[lang]

        self.root.title(strings["title"])
        self.language_label.config(text=strings["language_label"])
        self.time_label.config(text=strings["time_label"])
        self.start_button.config(text=strings["start_button"])
        self.reset_button.config(text=strings["reset_button"])
        self.text_to_type_label.config(text=strings["text_to_type"])
        self.your_input_label.config(text=strings["your_input"])
        self.info_label.config(text=strings["info_choose_options"])

        self._update_timer_label()

    # Test logic ------------------------------------------------------
    def start_test(self) -> None:
        if self.test_running:
            return

        self.test_running = True
        self.remaining_seconds = self.test_time.get()
        self.input_text.delete("1.0", "end")
        self.input_text.focus_set()

        words_source = WORDS_EN if self.language.get() == "en" else WORDS_PL
        # Generate a reasonably long text; timer will limit how much is typed.
        word_count = 250 if self.test_time.get() == 30 else 500
        words = random.choices(words_source, k=word_count)
        self.reference_text = " ".join(words)

        self._set_text_display(self.reference_text)
        self.results_label.config(text="")

        self._update_timer_label()
        self._schedule_tick()

    def reset_test(self) -> None:
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.test_running = False
        self.remaining_seconds = 0
        self.reference_text = ""

        self._set_text_display("")
        self.input_text.delete("1.0", "end")
        self.results_label.config(text="")

        self._update_timer_label()
        lang = self.language.get()
        self.info_label.config(text=LANG_STRINGS[lang]["info_choose_options"])

    def _set_text_display(self, value: str) -> None:
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", "end")
        self.text_display.insert("1.0", value)
        self.text_display.config(state="disabled")

    def _schedule_tick(self) -> None:
        self._update_timer_label()
        if self.remaining_seconds <= 0:
            self._finish_test()
            return

        self.remaining_seconds -= 1
        self.timer_id = self.root.after(1000, self._schedule_tick)

    def _update_timer_label(self) -> None:
        lang = self.language.get()
        strings = LANG_STRINGS[lang]
        if self.test_running:
            text = f"{strings['timer_prefix']} {self.remaining_seconds}{strings['seconds_suffix']}"
        else:
            text = f"{strings['timer_prefix']} 0{strings['seconds_suffix']}"
        self.timer_label.config(text=text)

    def _finish_test(self) -> None:
        self.test_running = False
        self.timer_id = None
        self._update_timer_label()

        lang = self.language.get()
        strings = LANG_STRINGS[lang]

        typed_text = self.input_text.get("1.0", "end-1c").strip()
        ref_words = self.reference_text.split()
        typed_words = typed_text.split()

        total_typed = len(typed_words)
        correct = 0
        for i, word in enumerate(typed_words):
            if i < len(ref_words) and word == ref_words[i]:
                correct += 1

        accuracy = (correct / total_typed * 100.0) if total_typed > 0 else 0.0
        seconds = self.test_time.get()
        wpm = (total_typed / seconds) * 60.0 if seconds > 0 else 0.0

        results_text = strings["results_template"].format(
            seconds=seconds,
            words_typed=total_typed,
            correct_words=correct,
            accuracy=accuracy,
            wpm=wpm,
        )
        self.results_label.config(text=f"{strings['results_title']}:\n{results_text}")
        self.info_label.config(text=strings["info_not_running"])

        messagebox.showinfo(strings["results_title"], results_text)


def main() -> None:
    root = tk.Tk()
    app = TypingSpeedTestApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
