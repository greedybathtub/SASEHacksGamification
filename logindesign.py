import tkinter as tk
from tkinter import messagebox

# --- Colors from your image ---
BG_OUTSIDE = "#FDE6B0"  # Yellowish cream
BG_CARD = "#C2DFFF"     # Pastel Blue
INPUT_BG = "#F5F5F5"    # Off-white/Light Gray
ACCENT_PINK = "#FFB6C1" # Pink for text/logo

def verify(user1, pass1):
    try:
        with open("users.txt", "r") as file:
            for line in file:
                userpass = line.strip().split(":")
                if len(userpass) == 2:
                    username, password = userpass
                    if username == user1 and password == pass1:
                        return True
        return False
    except FileNotFoundError:
        return False

def login():
    u, p = user_entry.get(), pass_entry.get()
    if verify(u, p):
        messagebox.showinfo("Success", f"Welcome, {u}!")
    else:
        messagebox.showerror("Error", "Invalid credentials")

def create_account():
    # You can apply the same styling logic below to a Toplevel window!
    messagebox.showinfo("Notice", "Redirecting to account creation...")

# --- Main Window Setup ---
window = tk.Tk()
window.title("Pastel Login")
window.geometry("350x600")
window.configure(bg=BG_OUTSIDE)

# The "Card" (The blue rounded rectangle area)
# Since Tkinter doesn't do true rounded corners easily, we use a Frame
card = tk.Frame(window, bg=BG_CARD, padx=30, pady=40)
card.place(relx=0.5, rely=0.5, anchor="center", width=310, height=550)

# 1. "LOGIN" Header (Pixel style simulation)
# Tip: If you have a pixel font installed, change "Courier" to that font name
title_label = tk.Label(
    card, text="LOGIN", 
    font=("Courier", 36, "bold"), 
    bg=BG_CARD, fg=ACCENT_PINK
)
title_label.pack(pady=(20, 40))

# 2. Username Entry
user_entry = tk.Entry(
    card, font=("Helvetica", 12),
    bg=INPUT_BG, fg="#333",
    relief="flat", justify="center"
)
# Note: Adding 'ipady' makes the box taller like in your image
user_entry.pack(fill="x", ipady=15, pady=10)
user_entry.insert(0, "Username") # Placeholder

# 3. Password Entry
pass_entry = tk.Entry(
    card, font=("Helvetica", 12),
    bg=INPUT_BG, fg="#333",
    relief="flat", justify="center", show="*"
)
pass_entry.pack(fill="x", ipady=15, pady=10)

# 4. Login Button (Hidden/Integrated)
# In your image, there isn't a clear "Login" button, so we'll add a styled one
login_btn = tk.Button(
    card, text="GO", command=login,
    font=("Courier", 14, "bold"),
    bg=ACCENT_PINK, fg="white",
    relief="flat", cursor="hand2"
)
login_btn.pack(pady=20, ipadx=20)

# 5. Create Account Link
create_btn = tk.Button(
    card, text="New Member? Create an Account!",
    command=create_account,
    bg=BG_CARD, fg=ACCENT_PINK,
    bd=0, cursor="hand2",
    font=("Helvetica", 9, "bold")
)
create_btn.pack(side="bottom", pady=20)

window.mainloop()