import string

def caesar(direction, text, shift):
	text = text.lower()
	alphabet = string.ascii_lowercase
	alphabet_length = len(alphabet)
	result = ""
	
	if direction == "decode":
		shift *= -1
	
	for letter in text:
		if letter in alphabet:
			letter_index = alphabet.index(letter)
			offset = (letter_index + shift) % alphabet_length
			result += alphabet[offset]
		else:
			result += letter

	return print(f"Here is {direction}ed result: ", result)

choice = "yes"
while choice == "yes":
	direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
	text = input("Type your message:\n").lower()
	shift = int(input("Type the shift number:\n"))

	caesar(direction, text, shift)

	choice = input("Do you want to run this program again?\nType 'yes' or 'no': ")
