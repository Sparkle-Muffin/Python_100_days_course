import random

print("I'm thinking of a number between 1 and 100.")
level = input("Choose a difficulty. Type 'easy' or 'hard': ")

number_of_tries = 10
if level == "hard":
    number_of_tries = 5

number = random.randint(1, 100)

victory = False
for i in range(number_of_tries):
    tries_remaining = number_of_tries - i - 1
    user_number = int(input("Make a guess: "))
    if user_number == number:
        print("You won!")
        victory = True
        break
    elif user_number > number:
        print("Too high.")
    else:
        print("Too low.")
    print("Guess again.")
    print(f"You have ", tries_remaining, "attempts remaining to guess the number.")

if victory == False:
    print("The number was", number)
    print("You lose!")