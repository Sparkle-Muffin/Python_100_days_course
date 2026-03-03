import random
from game_data import data

def draw_data():
    data_X = random.choice(data)
    data_X_index = data.index(data_X)
    data.pop(data_X_index)
    return data_X

game_over = False
current_score = 0

data_A = draw_data()
data_B = draw_data()

while game_over == False:
    print(f"Compare A: {data_A['name']}")
    print(f"Against B: {data_B['name']}")

    answer = input("Who has more followers? Type 'A' or 'B': ").upper()

    if answer == "A" and data_A['follower_count'] < data_B['follower_count']:
        print(f"Sorry, that's wrong. Final score: {current_score}.")
        game_over = True
    elif answer == "B" and data_A['follower_count'] > data_B['follower_count']:
        print(f"Sorry, that's wrong. Final score: {current_score}.")
        game_over = True
    else:
        current_score += 1
        data_A = data_B
        data_B = draw_data()
        print(f"You're right! Current score: {current_score}.")