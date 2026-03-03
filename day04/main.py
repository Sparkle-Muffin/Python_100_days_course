import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

symbols = [rock, paper, scissors]
choices = ["r", "p", "s"]

user_choice = input("Let's play a game. Choose between rock, paper and scissors. Type \"r\", \"p\" or \"s\".\n")

if user_choice not in choices:
	print("You typed a wrong letter.")

else:
    computer_choice = random.choice(choices)

    user_index = choices.index(user_choice)
    computer_index = choices.index(computer_choice)

    print("You: \n", symbols[user_index])
    print("Computer: \n", symbols[computer_index])

    if user_choice == computer_choice:
        print("Tie")

    elif user_choice == "r" and computer_choice == "p" or user_choice == "p" and computer_choice == "s" or user_choice == "s" and computer_choice == "r":
        print("You lose")

    else:
        print("You win")