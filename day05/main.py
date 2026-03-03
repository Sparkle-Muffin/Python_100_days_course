import random
import string

print("Welcome to the PyPassword Generator!")
nr_letters = int(input("How many letters do you want?\n"))
nr_numbers = int(input("How many numbers do you want?\n"))
nr_symbols = int(input("How many symbols do you want?\n"))

lowercases = string.ascii_lowercase
uppercases = string.ascii_uppercase
digits = string.digits
punctuation = string.punctuation

lowercases_arr = []
uppercases_arr = []
digits_arr = []
punctuation_arr = []

for letter in range(0, nr_letters+1):
	lowercases_arr.append(random.choice(lowercases))
for letter in range(0, nr_letters+1):
	uppercases_arr.append(random.choice(uppercases))
for digit in range(0, nr_numbers+1):
	digits_arr.append(random.choice(digits))
for symbol in range(0, nr_symbols+1):
	punctuation_arr.append(random.choice(punctuation))
	
cases_arr = lowercases_arr + uppercases_arr
cases_new_arr = []

for letter in range(0, nr_letters+1):
	cases_new_arr.append(random.choice(cases_arr))

all_array = cases_new_arr + digits_arr + punctuation_arr
password = []

pass_length = nr_letters + nr_numbers + nr_symbols

for character in range(0, pass_length+1):
	password.append(random.choice(all_array))	
	
password_str = ""
for character in password:
	password_str += character
	
print(password_str)
