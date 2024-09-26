import customtkinter as ctk
from tkinter import ttk
from tkinter import Tk, messagebox

# Create the root window using CTk
root = ctk.CTk()
root.geometry("600x400")
root.title("Handle Treeview Update and Selection")

# Sample data
initial_data = [
    ("John", 28, "Engineer"),
    ("Alice", 24, "Doctor"),
    ("Bob", 30, "Artist"),
]

new_data = [
    ("David", 35, "Teacher"),
    ("Emma", 29, "Scientist"),
    ("Chris", 32, "Writer"),
]

# Global variable to hold the selected item
selected_item_global = None

# Function to handle Treeview row selection
def on_tree_select(event):
    global selected_item_global
    selected_item = tree.selection()  # Get selected item
    print(selected_item)
    if selected_item:
        selected_item_global = selected_item[0]  # Save the selection globally
        values = tree.item(selected_item_global, "values")
        print(f"Selected: {values}")
    else:
        print("No row selected")
        selected_item_global = None  # Clear the global if no row is selected

# Function to clear and update Treeview with new data
def update_treeview():
    global selected_item_global
    # Temporarily disable event bindings to prevent errors
    tree.unbind("<<TreeviewSelect>>")
    
    # Clear the Treeview
    for row in tree.get_children():
        tree.delete(row)
    
    # Insert new data into the Treeview
    for row in new_data:
        tree.insert("", "end", values=row)
    
    # Reset the global selected item as there is no valid selection after update
    selected_item_global = None
    
    # Rebind the event after updating the Treeview
    tree.bind("<<TreeviewSelect>>", on_tree_select)
    print("Treeview updated with new data.")

# Function to confirm the selected row on button click
def confirm_selection():
    global selected_item_global
    if selected_item_global:
        values = tree.item(selected_item_global, "values")
        messagebox.showinfo("Selected Row", f"Selected row values: {values}")
    else:
        messagebox.showwarning("No Selection", "No row is currently selected!")

# Create a Treeview widget using ttk
columns = ("Name", "Age", "Occupation")
tree = ttk.Treeview(root, columns=columns, show="headings")

# Define column headings
for col in columns:
    tree.heading(col, text=col)

# Insert initial data into the Treeview
for row in initial_data:
    tree.insert("", "end", values=row)

# Add the Treeview to the CTk window
tree.pack(pady=20)

# Bind the selection event
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Button to update the Treeview
update_button = ctk.CTkButton(root, text="Update Treeview", command=update_treeview)
update_button.pack(pady=10)

# Button to confirm the selected row
confirm_button = ctk.CTkButton(root, text="Confirm Selection", command=confirm_selection)
confirm_button.pack(pady=10)

# Start the main loop
root.mainloop()
