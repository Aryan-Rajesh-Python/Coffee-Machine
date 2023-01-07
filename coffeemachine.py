import pyfiglet
app=pyfiglet.figlet_format("Coffee Machine")
print(app)
MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 20,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 25,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 25,
        },
        "cost": 3.0,
    }
}
profit=0
resources = {
    "water": 50000,
    "milk": 100000,
    "coffee": 5000,
}
def is_resources_sufficient(order_ingredients):
    is_enough=True
    for item in order_ingredients:
        if(order_ingredients[item]>=resources[item]):
            print(f"Sorry there is no enough {item} to prepare your drink!")
            is_enough=False
    return is_enough
is_on=True
def process_coins():
    print("Please insert the coins: ")
    quarters=int(input("Enter the number of quarters: "))
    dimes=int(input("Enter the number of dimes: "))
    nickles=int(input("Enter the number of nickles: "))
    pennies=int(input("Enter number of pennies: "))
    total=(quarters*0.25)
    total+=(dimes*0.1)
    total+=(nickles*0.05)
    total+=(pennies*0.01)
    return total
def is_transaction_successful(money_received,drink_cost):
    if money_received>=drink_cost:
        change=round(money_received-drink_cost,2)
        print(f"Here's your change of ${change}!")
        global profit
        profit+=drink_cost
        return True
    else:
        print("Sorry the money you paid is insufficient and we can't make you a drink!")
        return False
def make_coffee(drink_name,order_ingredients):
    for item in order_ingredients:
        resources[item]-=order_ingredients[item]
    print(f"Here is your {drink_name}☕️. Enjoy your drink!")
while is_on:
    choice=input("What would you like? (espresso/latte/cappuccino): ")
    if(choice=="off"):
        is_on=False
    elif(choice=="report"):
        print(f"Water: {resources['water']}ml")
        print(f"Milk: {resources['milk']}ml")
        print(f"Coffee: {resources['coffee']}g")
        print(f"Profit: ${profit}")
    else:
        drink=MENU[choice]
        if(is_resources_sufficient(drink["ingredients"])):
            payment=process_coins()
            if(is_transaction_successful(payment,drink["cost"])):
                make_coffee(choice,drink["ingredients"])
