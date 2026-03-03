START_RESOURCES = {
    "water": 10_000, # ml
    "milk":   5_000, # ml
    "coffee": 7_000, # g
    "money":    200, # $
}

COFFEE_RECIPES = {
    "espresso": {
        "water":  50, # ml
        "milk":    0, # ml
        "coffee": 18, # g
        "money": 1.5, # $
    },
    "latte": {
        "water": 200, # ml
        "milk":  150, # ml
        "coffee": 24, # g
        "money": 2.5, # $
    },
    "cappuccino": {
        "water": 250, # ml
        "milk":  100, # ml
        "coffee": 24, # g
        "money": 3.0, # $
    },
}

QUARTER_VALUE = 0.25
DIME_VALUE = 0.1
NICKLE_VALUE = 0.05
PENNY_VALUE = 0.01


def coffee_machine():
    machine_resources = START_RESOURCES

    def create_report():
        report = ""
        report += "Water: "  + str(machine_resources["water"])  + " ml" + "\n"
        report += "Milk: "   + str(machine_resources["milk"])   + " ml" + "\n"
        report += "Coffee: " + str(machine_resources["coffee"]) + " g"  + "\n"
        report += "Money: $" + str(machine_resources["money"])          + "\n"

        return report

    def check_resources(coffee_type):
        insufficient_resources = []
        for resource in machine_resources:
            if resource != "money":
                if machine_resources[resource] < COFFEE_RECIPES[coffee_type][resource]:
                    insufficient_resources.append(resource)
        return insufficient_resources
    
    def get_price(coffee_type):
        coffee_price = COFFEE_RECIPES[coffee_type]["money"]
        return coffee_price
    
    def calculate_change(coffee_price, payment):
        payment_sum = payment["quarters"] * QUARTER_VALUE + payment["dimes"] * DIME_VALUE + payment["nickles"] * NICKLE_VALUE + payment["pennies"] * PENNY_VALUE

        change = round(payment_sum - coffee_price, 2)
        return change

    def update_resources(coffee_type):
        machine_resources["water"] -= COFFEE_RECIPES[coffee_type]["water"]
        machine_resources["milk"] -= COFFEE_RECIPES[coffee_type]["milk"]
        machine_resources["coffee"] -= COFFEE_RECIPES[coffee_type]["coffee"]
        machine_resources["money"] += COFFEE_RECIPES[coffee_type]["money"]


    while True:
        answer = input("​What would you like? (espresso/latte/cappuccino): ")

        # Turn off the machine.
        if answer == "off":
            return
        # Print resources report.
        elif answer == "report":
            report = create_report()
            print(report)
        # Make coffee
        else:
            insufficient_resources = check_resources(answer)
            # There is not enough of some resource/s.
            if len(insufficient_resources) != 0:
                insufficient_resources_str = ", ".join(insufficient_resources)
                print(f"Sorry, there is not enough {insufficient_resources_str}.")
            # There are enough resources.
            else:
                coffee_price = get_price(answer)
                # Prompt user to insert coins.
                print(f"Please insert coins (${coffee_price}).")
                payment = {
                    "quarters": int(input("How many quarters?: ")),
                    "dimes":    int(input("How many dimes?: ")),
                    "nickles":  int(input("How many nickles?: ")),
                    "pennies":  int(input("How many pennies?: ")),
                }
                # Calculate the change.
                change = calculate_change(coffee_price, payment)
                # User inserted not enough money.
                if change < 0:
                    print("“​Sorry that's not enough money. Money refunded.​")
                # User inserted enough money. Make coffee and give them the change.
                else:
                    update_resources(answer)
                    if change > 0:
                        print(f"Here is ${change} in change.")
                    print(f"Here is your {answer} ☕. Enjoy!")

coffee_machine()