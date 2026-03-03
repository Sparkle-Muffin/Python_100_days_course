auctioneers = {}
more_auctioneers = True

while more_auctioneers == True:
	print("Welcome to the private bidding auction")
	name  = input("What is your name?: ").title()
	bid = float(input("How much would you like to bid?: $"))
	others = input("Are there any other bidders for this auction? Type 'yes' or 'no'.\n")
	
	if others == "no":
		more_auctioneers = False
	
	print("\n" * 100)
	
	auctioneers[name] = bid

highest_bid = 0.0
winner = {}

for name in auctioneers:
	if auctioneers[name] > highest_bid:
		highest_bid = auctioneers[name]
		winner = {name: auctioneers[name]}
		
print(winner)