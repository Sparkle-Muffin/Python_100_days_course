import random
from art import logo

want_to_play = "y"

while want_to_play == "y":
    def pick_one_card():
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, "ace"]
        card = random.choice(deck)
        return card
    def calculate_score(hand):
        score = 0
        aces = 0
        for card in hand:
            if card != "ace":
                score += card
            else:
                aces += 1
        for ace in range(aces):
            if score + 11 <= 21:
                score += 11
            else:
                score += 1
        return score

    want_to_play = input("Do you want to play a game of Blackjack? Type 'y' or 'n': ")
    if want_to_play == "n":
        break
    print(logo)
    user_hand = [pick_one_card(), pick_one_card()]
    computer_hand = [pick_one_card(), pick_one_card()]

    game_over = False
    while game_over == False:
        hit = "n"
        user_score = calculate_score(user_hand)

        if user_score < 21:
            print(f"Your cards: ", user_hand, ", current score: ", user_score)
            print(f"Computer's first card: ", computer_hand[0])

            hit = input("Type 'y' to get another card, type 'n' to pass: ")

        if hit == "n":
            computer_score = calculate_score(computer_hand)
            if user_score <= 21:
                while computer_score <= 16:
                    computer_hand.append(pick_one_card())
                    computer_score = calculate_score(computer_hand)
            if user_score > 21:
                print(f"Your cards: ", user_hand, ", final score: ", user_score)
                print(f"Computer's cards: ", computer_hand, ", final score: ", computer_score)
                print(f"You lose!")
            elif computer_score > 21:
                print(f"Your cards: ", user_hand, ", final score: ", user_score)
                print(f"Computer's cards: ", computer_hand, ", final score: ", computer_score)
                print(f"You win!")                
            elif computer_score == user_score:
                print(f"Your cards: ", user_hand, ", final score: ", user_score)
                print(f"Computer's cards: ", computer_hand, ", final score: ", computer_score)
                print(f"Draw!")
            elif computer_score > user_score:
                print(f"Your cards: ", user_hand, ", final score: ", user_score)
                print(f"Computer's cards: ", computer_hand, ", final score: ", computer_score)
                print(f"You lose!")
            else:
                print(f"Your cards: ", user_hand, ", final score: ", user_score)
                print(f"Computer's cards: ", computer_hand, ", final score: ", computer_score)
                print(f"You win!")
            game_over = True

        else:
            user_hand.append(pick_one_card())
