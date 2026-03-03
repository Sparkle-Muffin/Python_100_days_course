from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

def coffee_machine():
    menu = Menu()
    coffee_maker = CoffeeMaker()
    money_machine = MoneyMachine()
    menu_items = menu.get_items()

    while True:
        answer = input(f"​What would you like? ({menu_items}): ")

        # Turn off the machine.
        if answer == "off":
            return
        # Print resources report.
        elif answer == "report":
            coffee_maker.report()
            money_machine.report()
        # Serve customer.
        else:
            # Coffee does not exist.
            coffee_type = menu.find_drink(answer)
            if coffee_type == False:
                continue
            # Coffee exist.
            else:
                # Not enough resources.
                if coffee_maker.is_resource_sufficient(coffee_type) == False:
                    continue
                # Enough resources.
                else:
                    price = coffee_type.cost
                    # Not enough money.
                    if money_machine.make_payment(price) == False:
                        continue
                    # Enough money.
                    else:
                        coffee_maker.make_coffee(coffee_type)

coffee_machine()
