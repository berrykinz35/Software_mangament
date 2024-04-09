import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import sqlite3


# testing code
current_user_id = 1

# Function to add a new user
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists. Please choose another username.")
    conn.close()


# register user name and password in database
def register_click():
    global registration_window
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    confirm_password = confirm_password_entry.get()
    if password == confirm_password:
        if username and password:
            register_user(username, password)
            registration_window.destroy()  # Close the registration window after successful registration
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    else:
        messagebox.showerror("Error", "Passwords do not match.")


# Create the registration window
def registration_user():
    global registration_window
    global reg_username_entry
    global reg_password_entry
    global confirm_password_entry
    registration_window = tk.Tk()
    registration_window.title("Register")

    # Create and place the widgets for the registration window
    # (Code for username label, entry, password label, entry, confirm password label, entry, and register button)

    # Register button
    register_button = tk.Button(registration_window, text="Register", command=register_click)
    register_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="WE")
    reg_username_label = tk.Label(registration_window, text="Username:")
    reg_username_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")
    reg_username_entry = tk.Entry(registration_window)
    reg_username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="W")

    # Password label and entry
    reg_password_label = tk.Label(registration_window, text="Password:")
    reg_password_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")
    reg_password_entry = tk.Entry(registration_window, show="*")  # Show * for password entry
    reg_password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="W")

    # Confirm Password label and entry
    confirm_password_label = tk.Label(registration_window, text="Confirm Password:")
    confirm_password_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")
    confirm_password_entry = tk.Entry(registration_window, show="*")  # Show * for password entry
    confirm_password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="W")


# select input user from database and login user
def login(user, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    select_query = 'SELECT username, password, id FROM users WHERE username = ?;'
    try:
        c.execute(select_query, (user,))
        value = c.fetchone()
        if value:
            stored_username, stored_password, stored_id = value
            if password == stored_password:
                print("Login Successful!")
                message = f"Welcome, {stored_username}!"
                messagebox.showinfo("Login Successful", message)
                global current_user_id 
                current_user_id = stored_id
                root.destroy()
                open_expense()
            else:
                print("Incorrect password.")
                messagebox.showerror("Login Failed", "Invalid password")

        else:
            messagebox.showerror("Login Failed. User not found.")


    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"Please try again")

    finally:
        c.close()
        conn.close()


# validate user on click
def login_click():
    username = username_entry.get()
    password = password_entry.get()
    login(username, password)


# Create the login window
root = tk.Tk()
root.title("Login")

# (Code for username label, entry, password label, entry, login button)

# Username label and entry
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=5, pady=5)

# Password label and entry
password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Login button
log_in_button = tk.Button(root, text="Login", command=login_click)
log_in_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="WE")

# Register button
register_button = tk.Button(root, text="Registration", command=registration_user)
register_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="WE")


# Function to initialize the database
def initialize_database():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY, item TEXT, amount REAL, category TEXT, userid INTEGER)''')
    conn.commit()
    conn.close()
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT , password TEXT)''')
    conn.commit()
    conn.close()


# Initialize the database
initialize_database()


# Function to add an expense
def add_expense(item, amount, category):

    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (item, amount, category, userid) VALUES (?, ?, ?, ?)", (item, amount, category, current_user_id))
    conn.commit()
    conn.close()


# Function to edit an expense
def edit_expense(id, new_item, new_amount, new_category):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("UPDATE expenses SET item=?, amount=?, category=? WHERE id=?", (new_item, new_amount, new_category, id))
    conn.commit()
    conn.close()


# Function to delete an expense
def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()


# Function to view expenses
def view_expenses(category=None):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    if category:
        c.execute("SELECT * FROM expenses WHERE category=? and userid=?", (category, current_user_id,))
    else:
        c.execute("SELECT * FROM expenses where userid=?", (current_user_id,))
    expenses = c.fetchall()
    conn.close()
    return expenses


# Function to handle the 'Add Expense' button click event
def add_expense_click():
    item = item_entry.get()
    amount = amount_entry.get()
    category = category_entry.get()
    if item and amount and category:
        try:
            amount = float(amount)
            add_expense(item, amount, category)
            messagebox.showinfo("Success", "Expense added successfully!")
            item_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)
            category_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")


# Function to handle the 'View Expenses' button click event
def view_expenses_click():
    expenses = view_expenses()
    if expenses:
        expense_listbox.delete(0, tk.END)
        for expense in expenses:
            expense_listbox.insert(tk.END,
                                   f"ID: {expense[0]}, Item: {expense[1]}, Amount: ${expense[2]}, Category: {expense[3]}")
    else:
        messagebox.showinfo("Info", "No expenses found.")


# Function to handle the 'Delete Expense' button click event
def delete_expense_click():
    selected_index = expense_listbox.curselection()
    if selected_index:
        id = int(expense_listbox.get(selected_index)[4:5])
        delete_expense(id)
        messagebox.showinfo("Success", "Expense deleted successfully!")
        view_expenses_click()
    else:
        messagebox.showerror("Error", "Please select an expense to delete.")


# Function to handle the 'Spending Limits' button click event
def set_spending_limits():
    global expense
    expense.withdraw()

    limit_window = tk.Toplevel()
    limit_window.title("Set Spending Limits")

    categories = ["Food", "Transportation", "Entertainment", "Utilities", "Others"]

    def save_limits():
        limits = {}
        for category in categories:
            limit = limit_entries[category].get()
            if limit:
                try:
                    limit = float(limit)
                    limits[category] = limit
                except ValueError:
                    messagebox.showerror("Error", f"Invalid limit for {category}. Please enter a valid number.")
                    return
        messagebox.showinfo("Success", "Spending limits saved successfully!")
        limit_window.destroy()
        expense.deiconify()

    limit_entries = {}
    for i, category in enumerate(categories):
        tk.Label(limit_window, text=f"{category} Limit:").grid(row=i, column=0, padx=5, pady=5)
        limit_entries[category] = tk.Entry(limit_window)
        limit_entries[category].grid(row=i, column=1, padx=5, pady=5)

    save_button = tk.Button(limit_window, text="Save", command=save_limits)
    save_button.grid(row=len(categories), columnspan=2, padx=5, pady=5, sticky="WE")


# function to handle the 'invite friends' button click event
def invite_expense_report():
    friend_number = simpledialog.askstring("Invite Friend", "Enter friend's phone number:")
    if friend_number:
        self.invited_friends.add(friend_number)
        self.status_label.config(text=f"{friend_number} has been invited!.")
    else:
        print("Error, friend's number not provided")


# Create the Expense Window
def open_expense():
    global expense
    expense = tk.Tk()
    expense.title("Expense Manager")

    # Create and place the widgets
    item_label = tk.Label(expense, text="Item:")
    item_label.grid(row=0, column=0, padx=5, pady=5)

    global item_entry
    item_entry = tk.Entry(expense)
    item_entry.grid(row=0, column=1, padx=5, pady=5)

    amount_label = tk.Label(expense, text="Amount:")
    amount_label.grid(row=1, column=0, padx=5, pady=5)

    global amount_entry
    amount_entry = tk.Entry(expense)
    amount_entry.grid(row=1, column=1, padx=5, pady=5)

    category_label = tk.Label(expense, text="Category:")
    category_label.grid(row=2, column=0, padx=5, pady=5)

    global category_entry
    category_entry = tk.Entry(expense)
    category_entry.grid(row=2, column=1, padx=5, pady=5)

    add_button = tk.Button(expense, text="Add Expense", command=add_expense_click)
    add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="WE")

    view_button = tk.Button(expense, text="View Expenses", command=view_expenses_click)
    view_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="WE")

    delete_button = tk.Button(expense, text="Delete Expense", command=delete_expense_click)
    delete_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="WE")

    limit_button = tk.Button(expense, text="Spending Limits", command=set_spending_limits)
    limit_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="WE")

    invite_button = tk.Button(expense, text="Invite Friends", command=invite_expense_report)
    invite_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="WE")

    global expense_listbox
    expense_listbox = tk.Listbox(expense, height=10, width=50)
    expense_listbox.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

# Test adding an expense
add_expense("Groceries", 50.00, "Food")
add_expense("Gas", 30.00, "Transportation")
add_expense("Movie tickets", 25.00, "Entertainment")

# Test viewing expenses
expenses = view_expenses()
print("All Expenses:")
for expense in expenses:
    print(expense)

# Test viewing expenses for a specific category
expenses_food = view_expenses("Food")
print("\nFood Expenses:")
for expense in expenses_food:
    print(expense)

# Test deleting an expense (assuming an expense ID is known)
# Note: Replace '1' with the actual expense ID you want to delete
delete_expense(1)
print("\nExpense ID 1 deleted.")

# Test viewing expenses after deletion
expenses_after_deletion = view_expenses()
print("\nAll Expenses after deletion:")
for expense in expenses_after_deletion:
    print(expense)

root.mainloop()