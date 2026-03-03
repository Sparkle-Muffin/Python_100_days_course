import turtle
from pathlib import Path
import pandas as pd
from usa_state import UsaState

BASE_DIR = Path(__file__).parent
image_path = BASE_DIR / "blank_states_img.gif"
states_path = BASE_DIR / "50_states.csv"
output_file_path = BASE_DIR / "states_to_learn.csv"

screen = turtle.Screen()
screen.title("USA States Game")
screen.addshape(str(image_path))
turtle.shape(str(image_path))

states = pd.read_csv(states_path)
usa_state = UsaState()
number_of_states = len(states)
guessed_states = []
number_of_guessed_states = 0

while number_of_guessed_states < number_of_states:
    score = str(number_of_guessed_states) + "/" + str(number_of_states)
    answer_state = screen.textinput(title=f"{score} States Correct", prompt="What's another state name?")
    answer_state = answer_state.title()

    if answer_state == "Exit":
        states_names = states["state"].to_list()
        states_to_learn = [state_name for state_name in states_names if state_name not in guessed_states]
        states_to_learn_df = pd.DataFrame(states_to_learn)
        states_to_learn_df.to_csv(output_file_path, index=False, header=False)
        break

    elif answer_state in states["state"].values:
        x_coor = states[states["state"] == answer_state]["x"].item()
        y_coor = states[states["state"] == answer_state]["y"].item()
        usa_state.write_name(answer_state, x_coor, y_coor)
        if answer_state not in guessed_states:
            guessed_states.append(answer_state)
            number_of_guessed_states += 1

