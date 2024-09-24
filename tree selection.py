import tkinter as tk
from tkinter import ttk

# Create the root window
root = tk.Tk()
root.geometry("600x400")
root.title("Treeview Events Example")

# Sample data
data = [
    ("John", 28, "Engineer"),
    ("Alice", 24, "Doctor"),
    ("Bob", 30, "Artist"),
    ("David", 35, "Lawyer"),
    ("Emma", 22, "Teacher"),
]

# Function to handle Treeview selection event
def on_treeview_select(event):
    selected_item = tree.focus()  # Get the focused (selected) item
    values = tree.item(selected_item, "values")  # Get the values of the selected item
    print("<<TreeviewSelect>> triggered:", values)

# Function to handle ButtonRelease event
def on_treeview_click(event):
    selected_item = tree.focus()  # Get the focused (selected) item
    values = tree.item(selected_item, "values")  # Get the values of the selected item
    print("ButtonRelease triggered:", values)

# Create a Treeview widget
columns = ("Name", "Age", "Occupation")
tree = ttk.Treeview(root, columns=columns, show="headings")

# Define column headings
for col in columns:
    tree.heading(col, text=col)

# Insert data into the Treeview
for row in data:
    tree.insert("", tk.END, values=row)

tree.pack(pady=20)

# Bind Treeview selection event
tree.bind("<<TreeviewSelect>>", on_treeview_select)

# Bind ButtonRelease-1 (left-click) event
tree.bind("<ButtonRelease-1>", on_treeview_click)

# Start the main loop
root.mainloop()
