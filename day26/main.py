from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent
nato_path = BASE_DIR / "nato_phonetic_alphabet.csv"

nato_df = pd.read_csv(nato_path)

nato_dict = {val['letter']:val['code'] for (i, val) in nato_df.iterrows()}

while True:
    user_input = input("Type a word: ")
    user_input = user_input.upper()

    letters = [letter for letter in user_input]
    codes = [nato_dict[letter] for letter in letters]

    print(codes)
