import tkinter as tk
from tkinter import messagebox
import os

def create_log_hours_tab(parent, username):
    log_hours_frame = tk.Frame(parent)

    tk.Label(log_hours_frame, text="Log Study Hours", font=("Arial", 14)).pack(pady=10)

    user_file = os.path.join("userInfo", f"{username}.txt")

    hours_logged = 0
    points = 0
    lines = []

    # Load existing data
    if os.path.exists(user_file):
        with open(user_file, "r") as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith("HoursLogged:"):
                hours_logged = float(line.replace("HoursLogged:", "").strip())
            if line.startswith("PointsEarned:"):
                points = int(line.replace("PointsEarned:", "").strip())

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
            points += int(added_hours * 5)

            hours_label.config(text=f"Total Hours Logged: {hours_logged}")
            points_label.config(text=f"Total Points Earned: {points}")

            updated_lines = []
            hours_found = False
            points_found = False

            for line in lines:
                if line.startswith("HoursLogged:"):
                    updated_lines.append(f"HoursLogged: {hours_logged}\n")
                    hours_found = True
                elif line.startswith("PointsEarned:"):
                    updated_lines.append(f"PointsEarned: {points}\n")
                    points_found = True
                else:
                    updated_lines.append(line)

            if not hours_found:
                updated_lines.append(f"HoursLogged: {hours_logged}\n")

            if not points_found:
                updated_lines.append(f"PointsEarned: {points}\n")

            with open(user_file, "w") as f:
                f.writelines(updated_lines)

            messagebox.showinfo("Success", f"{added_hours} hours added!")

            hours_entry.delete(0, tk.END)

        except:
            messagebox.showerror("Error", "Enter a valid number of hours.")

    tk.Button(log_hours_frame, text="Add Hours", command=add_hours).pack(pady=10)

    return log_hours_frame