import tkinter as tk
from tkinter import messagebox
from addMongo import users_col  # MongoDB UserInfo collection

def create_log_hours_tab(parent, username):
    log_hours_frame = tk.Frame(parent)

    tk.Label(log_hours_frame, text="Log Study Hours", font=("Arial", 14)).pack(pady=10)

    # Fetch current user data from MongoDB
    user_doc = users_col.find_one({"_id": username})
    if not user_doc:
        messagebox.showerror("Error", "User not found in database!")
        return log_hours_frame

    hours_logged = user_doc.get("hoursLogged", 0.0)
    points = user_doc.get("pointsEarned", 0)

    # Display stats
    hours_label = tk.Label(log_hours_frame, text=f"Total Hours Logged: {hours_logged}")
    hours_label.pack(pady=5)

    points_label = tk.Label(log_hours_frame, text=f"Total Points Earned: {points}")
    points_label.pack(pady=5)

    tk.Label(log_hours_frame, text="Hours to add:").pack(pady=5)
    hours_entry = tk.Entry(log_hours_frame)
    hours_entry.pack(pady=5)

    def add_hours():
        nonlocal hours_logged, points

        try:
            added_hours = float(hours_entry.get())
            if added_hours <= 0:
                raise ValueError

            hours_logged += added_hours
            earned_points = int(added_hours * 5)
            points += earned_points

            # Update MongoDB
            users_col.update_one(
                {"_id": username},
                {"$set": {"hoursLogged": hours_logged, "pointsEarned": points}}
            )

            # Update labels
            hours_label.config(text=f"Total Hours Logged: {hours_logged}")
            points_label.config(text=f"Total Points Earned: {points}")

            messagebox.showinfo("Success", f"{added_hours} hours added! ({earned_points} points)")
            hours_entry.delete(0, tk.END)

        except:
            messagebox.showerror("Error", "Enter a valid number of hours.")

    tk.Button(log_hours_frame, text="Add Hours", command=add_hours).pack(pady=10)

    return log_hours_frame