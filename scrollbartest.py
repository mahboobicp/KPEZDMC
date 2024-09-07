import tkinter as tk
from tkinter import ttk

# Initialize the root window
root = tk.Tk()
root.title("Treeview with Fixed Width Columns")

# Create a frame to hold the Treeview and Scrollbars
frame = tk.Frame(root)
frame.pack(pady=20)

# Create a Treeview widget with columns
tree = ttk.Treeview(frame, columns=("Name", "Age", "City"), show='headings', height=5)

# Define columns with fixed widths and no stretching
tree.column("Name", anchor=tk.W, width=150, stretch=False)  # Prevent stretch
tree.column("Age", anchor=tk.CENTER, width=100, stretch=False)
tree.column("City", anchor=tk.W, width=150, stretch=False)

# Define the headings
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("City", text="City")

# Add some data to the Treeview
tree.insert("", "end", values=("Alice", 25, "New York"))
tree.insert("", "end", values=("Bob", 30, "Los Angeles"))
tree.insert("", "end", values=("Charlie", 35, "Chicago"))
tree.insert("", "end", values=("David", 40, "Houston"))
tree.insert("", "end", values=("Eva", 29, "Miami"))

# Create vertical scrollbar
v_scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=v_scroll.set)

# Create horizontal scrollbar
h_scroll = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
tree.configure(xscrollcommand=h_scroll.set)

# Pack the treeview and scrollbars
tree.pack(side=tk.LEFT)  # Fixed size (no expand or fill)
v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

# Start the main loop
root.mainloop()
