import customtkinter as ctk

# Initialize the root window
root = ctk.CTk()
root.geometry("400x200")
root.title("Scrolling Text Animation Example")

# Create a CTkLabel to display the scrolling text
label = ctk.CTkLabel(root, text="", font=("Helvetica", 18))
label.pack(pady=40)

# Text to display
text = " Welcome to CustomTkinter! "

# Function to animate text (scrolling effect)
def scrolling_animation():
    current_text = label.cget("text")
    updated_text = current_text[1:] + current_text[0]  # Rotate the text
    label.configure(text=updated_text)
    root.after(150, scrolling_animation)  # Recursive call after 150ms

# Initialize label text and start scrolling animation
label.configure(text=text)
scrolling_animation()

# Start the main loop
root.mainloop()
