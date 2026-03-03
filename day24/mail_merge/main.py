from pathlib import Path
import os

# Define dirs and paths.
BASE_DIR = Path(__file__).parent
LETTER_PATTERN_PATH = BASE_DIR / "Input" / "Letters" / "starting_letter.txt"
NAMES_PATH = BASE_DIR / "Input" / "Names" / "invited_names.txt"
LETTERS_WITH_NAMES_DIR = BASE_DIR / "Output"

# Create Output dir.
os.makedirs(LETTERS_WITH_NAMES_DIR, exist_ok = True)

# Read names.
with open(NAMES_PATH) as file:
    raw_names = file.readlines()

# Remove "\n" from names.
names = [name.strip() for name in raw_names]

# Read letter pattern.
with open(LETTER_PATTERN_PATH) as file:
    pattern_letter = file.read()

# Add names to letters.
letters_with_names = []
for name in names:
    letter_with_name = pattern_letter.replace("[name]", name)
    letters_with_names.append(letter_with_name)

# Save letters.
for i, letter in enumerate(letters_with_names):
    name = names[i]
    letter_name = "letter_for_" + name + ".txt"
    letter_path = LETTERS_WITH_NAMES_DIR / letter_name
    with open(letter_path, mode="w") as file:
        file.write(letter)
        