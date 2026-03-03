from art import logo

def add(a, b):
	return a + b
	
def subtract(a, b):
	return a - b
	
def multiply(a, b):
	return a * b
	
def divide(a, b):
	return a / b
	
operations = {"+": add,
	"-": subtract,
	"*": multiply,
	"/": divide}
	

new_calculation = True
while new_calculation == True:
	print(logo)

	number_1 = float(input("What is the first number? "))

	continue_calculations = True
	while continue_calculations == True:
		for operation in operations:
			print(operation)
			
		operation = input("Type a math operation: ")

		number_2 = float(input("What is the next number? "))

		result = operations[operation](number_1, number_2)

		print(f"{number_1} {operation} {number_2} = {result}")

		print(f"Type 'y' to continue calculating with {result}, type 'n' to exit or type 'new' for a brand new calculation")
		
		decision = input("Type y/n/new: ")
		
		if decision == "y":
			number_1 = result
		elif decision == "n":
			print("Goodbye")
			continue_calculations = False
			new_calculation = False
		else:
			continue_calculations = False
			