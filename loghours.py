import tkinter as tk
from tkinter import messagebox
import addMongo
import pointshelpers

def create_log_hours_tab(parent, username):
    log_hours_frame = tk.Frame(parent, bg="#FFF0F8")

    tk.Label(log_hours_frame, text="🐾 Log Study Hours — Paws & Pages", font=("Arial", 14), bg="#FFF0F8", fg="#F7A8C4").pack(pady=10)

    # Fetch current user data from MongoDB
    user_doc = addMongo.users_col.find_one({"_id": username})
    if not user_doc:
        messagebox.showerror("Error", "User not found in database!")
        return log_hours_frame

    # Display stats
    hours_label = tk.Label(log_hours_frame, text=f"🐱 Total Hours Logged: {pointshelpers.get_hours(username)}", bg="#FFF0F8", fg="#888")
    hours_label.pack(pady=5)

    points_label = tk.Label(log_hours_frame, text=f"🐾 Total Paw Points: {pointshelpers.get_points(username)}", bg="#FFF0F8", fg="#F7A8C4", font=("Arial", 10, "bold"))
    points_label.pack(pady=5)

    tk.Label(log_hours_frame, text="🕐 Hours to add:", bg="#FFF0F8", fg="#888").pack(pady=5)
    hours_entry = tk.Entry(log_hours_frame, relief="flat", bg="#FFF0F8", fg="#C06080", highlightthickness=1, highlightbackground="#A8C8F7")
    hours_entry.pack(pady=5)

    def add_hours_gui():
        try:
            added_hours = float(hours_entry.get())
            if added_hours <= 0:
                raise ValueError

            # Update MongoDB atomically and get new totals back
            new_hours, new_points = pointshelpers.add_hours(username, added_hours)

            # ✅ Fix 1: Update labels with the NEW values returned from DB
            hours_label.config(text=f"🐱 Total Hours Logged: {new_hours}")
            points_label.config(text=f"🐾 Total Paw Points: {new_points}")

            messagebox.showinfo("Success", f"{added_hours} hours added! ({int(added_hours * 5)} points)")
            hours_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive number of hours.")

    # ✅ Fix 2: Button now correctly calls add_hours_gui, not the raw helper
    tk.Button(log_hours_frame, text="🐱 Add Study Hours", command=add_hours_gui,
              bg="#F9A8C9", fg="#FFFFFF", relief="groove", padx=20, pady=6, cursor="hand2", font=("Arial", 10, "bold")).pack(pady=10)

    return log_hours_frame