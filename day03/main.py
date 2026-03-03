print("Welcome to Treasure Island. Your mission is to find the treasure.")
direction = input("Do you go left or right? type \"l\" or \"r\". ")
if direction != "l":
	print("Game Over")
else:
	activity = input("Do you swim or wait? type \"s\" or \"w\". ")
	if activity != "w":
		print("Game Over")
	else:
		door = input("You have to choose between red, yellow and blue door. Which do you choose? type \"r\", \"y\" or \"b\". ")
		if door != "y":
			print("Game Over")
		else:
			print("You Win!")
            