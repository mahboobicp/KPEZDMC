import customtkinter as ctk

# Function to handle button clicks
def button_click(button):
    global highlighted_button  # Keep track of the currently highlighted button

    # If there is a previously highlighted button, reset its appearance
    if highlighted_button is not None and highlighted_button != button:
        highlighted_button.configure(fg_color="green")  # Reset color of previous button
    
    # Highlight the clicked button
    button.configure(fg_color="darkblue")  # Change color of clicked button
    highlighted_button = button  # Update the highlighted button

# Initialize the application
app = ctk.CTk()
app.title("Highlight CTkButton Example")

# Initialize a variable to keep track of the highlighted button
highlighted_button = None

# Create buttons
button1 = ctk.CTkButton(app, text="Button 1", command=lambda: button_click(button1))
button1.pack(pady=10)

button2 = ctk.CTkButton(app, text="Button 2", command=lambda: button_click(button2))
button2.pack(pady=10)

button3 = ctk.CTkButton(app, text="Button 3", command=lambda: button_click(button3))
button3.pack(pady=10)

# Run the application
app.mainloop()
