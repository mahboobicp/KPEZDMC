import customtkinter as ctk

# Initialize the root window
root = ctk.CTk()
root.geometry("400x200")
root.title("CTkEntry Focus Out Between Entry Fields")

# Define the callback function that will be triggered when focus is lost
def on_focus_out(event):
    print(f"Focus lost from entry: {event.widget.get()}")

# Create multiple CTkEntry widgets
entry1 = ctk.CTkEntry(root, width=200)
entry1.pack(pady=10)

entry2 = ctk.CTkEntry(root, width=200)
entry2.pack(pady=10)

entry3 = ctk.CTkEntry(root, width=200)
entry3.pack(pady=10)

# Bind the "<FocusOut>" event to each entry field
entry1.bind("<FocusOut>", on_focus_out)
entry2.bind("<FocusOut>", on_focus_out)
entry3.bind("<FocusOut>", on_focus_out)

# Start the main loop
root.mainloop()
