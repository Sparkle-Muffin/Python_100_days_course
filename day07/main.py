import random
from hangman_words import word_list
from hangman_art import stages

word = random.choice(word_list)
word_len = len(word)
user_guess = ""
total_lives = len(stages) - 1
remaining_lives = total_lives
success = False
end_of_game = False

for letter in range(word_len):
	user_guess += "_"

print("Secret word: ", word)
print("You have to guess the following word: ", user_guess)
while end_of_game == False:
	user_letter = input("type a letter:\n").lower()

	right_guess = False
	for i, letter in enumerate(word):
		if letter == user_letter:
			user_guess = user_guess[:i] + letter + user_guess[i+1:]
			right_guess = True
	print(user_guess)
	if right_guess == False:
		remaining_lives -= 1
		if remaining_lives == 0:
			end_of_game = True
			success = False

	else:
		if word == user_guess:
			end_of_game = True
			success = True

	print(stages[remaining_lives])

if success == False:
	print("You lose")
else:
	print("You win")
