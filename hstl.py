import customtkinter as ctk
from tkinter import StringVar

# Create the root window using CTk
root = ctk.CTk()
root.geometry("400x200")
root.title("Set CTkEntry based on ComboBox")

# Define a function to update the CTkEntry based on ComboBox selection
def update_entry(selected_value):
    entry_var.set(f"Selected: {selected_value}")  # Set the value in the CTkEntry

# Create a CTkComboBox with some values and use the `command` to trigger the function
combobox = ctk.CTkComboBox(root, values=["Option 1", "Option 2", "Option 3"], command=update_entry)
combobox.pack(pady=20)

# Create a textvariable for the CTkEntry
entry_var = StringVar()

# Create a CTkEntry and link it to the textvariable
entry = ctk.CTkEntry(root, textvariable=entry_var)
entry.pack(pady=20)

# Start the main loop
root.mainloop()
