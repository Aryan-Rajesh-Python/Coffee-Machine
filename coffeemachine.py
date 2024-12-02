import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import matplotlib.pyplot as plt
from tkinter import ttk

# Global variables
MENU = {
    "Espresso": {"ingredients": {"water": 50, "coffee": 18}, "cost": 1.5},
    "Latte": {"ingredients": {"water": 200, "milk": 150, "coffee": 24}, "cost": 2.5},
    "Cappuccino": {"ingredients": {"water": 250, "milk": 100, "coffee": 24}, "cost": 3.0},
}

resources = {"water": 10000000, "milk": 10000000, "coffee": 10000000, "money": 0.0}
sales_log = []
user_data = {}  # Store user info like username, loyalty points, purchase history
current_user = None
points_per_purchase = 10
drink_categories = {"Coffee": [], "Tea": []}  # Added categories for drinks

# Check if resources are sufficient
def check_resources(order_ingredients):
    for item in order_ingredients:
        if order_ingredients[item] > resources[item]:
            messagebox.showerror("Resource Error", f"Not enough {item} available!")
            return False
    return True

# Handle payment and loyalty points
def process_payment(drink_cost):
    try:
        payment = float(payment_entry.get())
        if payment >= drink_cost:
            change = round(payment - drink_cost, 2)
            resources["money"] += drink_cost
            messagebox.showinfo("Payment Successful", f"Transaction successful! Your change is ${change}.")
            if current_user:
                user_data[current_user]['loyalty_points'] += points_per_purchase
                messagebox.showinfo("Loyalty Reward", f"You've earned {points_per_purchase} loyalty points!")
            return True
        else:
            messagebox.showerror("Payment Error", "Insufficient payment! Money refunded.")
            return False
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid payment amount.")
        return False

# Make the coffee and log the sale
def make_coffee(drink_name, order_ingredients):
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sales_log.append({"drink": drink_name, "time": timestamp, "price": MENU[drink_name]["cost"]})
    if current_user:
        user_data[current_user]['purchase_history'].append({"drink": drink_name, "time": timestamp})
    messagebox.showinfo("Enjoy!", f"Your {drink_name} is ready! ☕")
    update_report()

# Select a drink
def select_drink(drink_name):
    drink = MENU[drink_name]
    if check_resources(drink["ingredients"]):
        if process_payment(drink["cost"]):
            make_coffee(drink_name, drink["ingredients"])

# Add custom drink
def add_custom_drink():
    drink_name = simpledialog.askstring("New Drink", "Enter the drink name:")
    if not drink_name:
        return
    try:
        water = int(simpledialog.askinteger("Water", "Enter water amount (ml):"))
        milk = int(simpledialog.askinteger("Milk", "Enter milk amount (ml):", initialvalue=0))
        coffee = int(simpledialog.askinteger("Coffee", "Enter coffee amount (g):"))
        cost = float(simpledialog.askfloat("Cost", "Enter drink cost ($):"))
        
        # Validate the price
        if cost <= 0:
            messagebox.showerror("Invalid Price", "Price must be greater than 0.")
            return
        
        MENU[drink_name] = {"ingredients": {"water": water, "milk": milk, "coffee": coffee}, "cost": cost}
        messagebox.showinfo("Success", f"Custom drink '{drink_name}' added!")
        update_menu_buttons()
    except (TypeError, ValueError):
        messagebox.showerror("Input Error", "Invalid input. Drink not added.")

# Add custom category
def add_category():
    category_name = simpledialog.askstring("New Category", "Enter new drink category name:")
    if category_name:
        drink_categories[category_name] = []
        messagebox.showinfo("Success", f"Category '{category_name}' added!")

# Add drink to a category
def assign_drink_to_category():
    drink_name = simpledialog.askstring("Assign Drink", "Enter the drink name:")
    category_name = simpledialog.askstring("Assign Category", "Enter the category name:")
    if drink_name in MENU and category_name in drink_categories:
        drink_categories[category_name].append(drink_name)
        messagebox.showinfo("Success", f"'{drink_name}' assigned to category '{category_name}'!")
        update_menu_buttons()
    else:
        messagebox.showerror("Error", "Invalid drink or category.")

# View purchase history
def view_purchase_history():
    if current_user:
        history = "\n".join([f"{entry['time']} - {entry['drink']}" for entry in user_data[current_user]['purchase_history']])
        messagebox.showinfo(f"{current_user}'s Purchase History", history)
    else:
        messagebox.showinfo("No User", "Please log in to view purchase history.")

# Redeem loyalty points for discount
def redeem_points():
    if current_user:
        points = user_data[current_user]["loyalty_points"]
        if points >= 10:
            discount = points // 10 * 0.5  # Redeem 10 points for $0.5 discount
            messagebox.showinfo("Loyalty Points", f"You've redeemed {discount} dollars in loyalty points!")
            return discount
        else:
            messagebox.showinfo("Loyalty Points", "Not enough points to redeem.")
    else:
        messagebox.showinfo("No User", "Please log in to redeem points.")
    return 0

# User registration or login
def register_user():
    global current_user
    username = simpledialog.askstring("User Registration", "Enter your username:")
    if username:
        if username not in user_data:
            user_data[username] = {"loyalty_points": 0, "purchase_history": []}
        current_user = username
        messagebox.showinfo("Welcome", f"Welcome back, {username}!")
        update_report()

# View sales log
def view_sales_log():
    if not sales_log:
        messagebox.showinfo("Sales Log", "No sales yet!")
        return
    sales_details = "\n".join([f"{sale['time']} - {sale['drink']}: ${sale['price']}" for sale in sales_log])
    messagebox.showinfo("Sales Log", sales_details)

# Show resource depletion chart
def show_resource_chart():
    labels = ["Water (ml)", "Milk (ml)", "Coffee (g)"]
    values = [resources["water"], resources["milk"], resources["coffee"]]
    plt.bar(labels, values, color=["blue", "orange", "brown"])
    plt.title("Current Resources")
    plt.ylabel("Amount")
    plt.show()

# Generate sales chart
def show_sales_chart():
    drinks = {}
    for sale in sales_log:
        drink = sale["drink"]
        if drink in drinks:
            drinks[drink] += 1
        else:
            drinks[drink] = 1

    drink_names = list(drinks.keys())
    drink_sales = list(drinks.values())

    plt.bar(drink_names, drink_sales, color="green")
    plt.title("Drink Sales Overview")
    plt.xlabel("Drink")
    plt.ylabel("Quantity Sold")
    plt.show()

# Update report with user data
def update_report():
    if current_user:
        user_report = f"User: {current_user}\nLoyalty Points: {user_data[current_user]['loyalty_points']}\n"
    else:
        user_report = "No user logged in.\n"
    report_text.set(
        f"Water: {resources['water']}ml\nMilk: {resources['milk']}ml\n"
        f"Coffee: {resources['coffee']}g\nMoney: ${resources['money']:.2f}\n\n"
        + user_report
    )

# Admin Panel (for refills)
def admin_panel():
    password = simpledialog.askstring("Admin Panel", "Enter admin password:", show="*")
    if password == "admin123":
        refill_resources()
    else:
        messagebox.showerror("Access Denied", "Incorrect password.")

# Refill resources
def refill_resources():
    resources["water"] += 5000000
    resources["milk"] += 3000000
    resources["coffee"] += 1000000
    messagebox.showinfo("Resources Refilled", "Machine resources have been refilled.")
    update_report()

# Update menu buttons based on available drinks
def update_menu_buttons():
    for widget in menu_frame.winfo_children():
        widget.destroy()  # Clear existing buttons

    tk.Label(menu_frame, text="Available Drinks", font=("Arial", 16)).pack()

    for drink_name in MENU:
        drink_button = tk.Button(menu_frame, text=drink_name, width=15, height=2, command=lambda name=drink_name: select_drink(name))
        drink_button.pack(pady=5)

# GUI setup
root = tk.Tk()
root.title("Coffee Machine")

# Menu frame
menu_frame = tk.Frame(root)
menu_frame.pack(pady=20)

# Payment input and submit
payment_label = tk.Label(root, text="Enter Payment ($):")
payment_label.pack()
payment_entry = tk.Entry(root)
payment_entry.pack()

# Loyalty points and login
login_button = tk.Button(root, text="Login", width=15, height=2, command=register_user)
login_button.pack(pady=10)

# Report Display
report_text = tk.StringVar()
report_label = tk.Label(root, textvariable=report_text, font=("Arial", 14), justify=tk.LEFT)
report_label.pack(pady=10)

# Admin and additional features
admin_button = tk.Button(root, text="Admin Panel", width=15, height=2, command=admin_panel)
admin_button.pack(pady=5)

view_sales_button = tk.Button(root, text="View Sales Log", width=15, height=2, command=view_sales_log)
view_sales_button.pack(pady=5)

resource_chart_button = tk.Button(root, text="Resource Chart", width=15, height=2, command=show_resource_chart)
resource_chart_button.pack(pady=5)

sales_chart_button = tk.Button(root, text="Sales Chart", width=15, height=2, command=show_sales_chart)
sales_chart_button.pack(pady=5)

# Load initial menu
update_menu_buttons()

root.mainloop()
