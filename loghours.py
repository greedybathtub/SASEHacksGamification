import tkinter as tk
from tkinter import messagebox
import addMongo
import pointshelpers

def create_log_hours_tab(parent, username):
    log_hours_frame = tk.Frame(parent, bg="#FFF0FA")

    tk.Label(log_hours_frame, text="🐾 Log Study Hours — Paws & Pages", font=("Arial", 14), bg="#FFF0FA", fg="#F48FB1").pack(pady=10)

    # Fetch current user data from MongoDB
    user_doc = addMongo.users_col.find_one({"_id": username})
    if not user_doc:
        messagebox.showerror("Error", "User not found in database!")
        return log_hours_frame

    # Use helper functions to get current values
    hours_logged = pointshelpers.get_hours(username)
    points = pointshelpers.get_points(username)

    # Display stats
    hours_label = tk.Label(log_hours_frame, text=f"🐱 Total Hours Logged: {hours_logged}", bg="#FFF0FA", fg="#888")
    hours_label.pack(pady=5)

    points_label = tk.Label(log_hours_frame, text=f"🐾 Total Paw Points: {points}", bg="#FFF0FA", fg="#F48FB1", font=("Arial", 10, "bold"))
    points_label.pack(pady=5)

    tk.Label(log_hours_frame, text="🕐 Hours to add:", bg="#FFF0FA", fg="#888").pack(pady=5)
    hours_entry = tk.Entry(log_hours_frame, relief="flat", bg="#FFF5FB", fg="#C06080", highlightthickness=1, highlightbackground="#F9A8C9")
    hours_entry.pack(pady=5)

    def add_hours_gui():
        try:
            added_hours = float(hours_entry.get())
            if added_hours <= 0:
                raise ValueError

            # Use helper function to update MongoDB atomically
            new_hours, new_points = pointshelpers.add_hours(username, added_hours)

            # Update labels
            hours_label.config(text=f"🐱 Total Hours Logged: {hours_logged}")
            points_label.config(text=f"🐾 Total Paw Points: {points}")

            messagebox.showinfo("Success", f"{added_hours} hours added! ({int(added_hours*5)} points)")
            hours_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive number of hours.")

    tk.Button(log_hours_frame, text="🐱 Add Hours", command=add_hours,
              bg="#F9A8C9", fg="white", relief="flat", padx=20, pady=6, cursor="hand2").pack(pady=10)

    return log_hours_frame