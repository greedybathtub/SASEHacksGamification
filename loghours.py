import tkinter as tk
from tkinter import messagebox
from addMongo import users_col  # MongoDB UserInfo collection

def create_log_hours_tab(parent, username):
    log_hours_frame = tk.Frame(parent, bg="#FFF0FA")

    tk.Label(log_hours_frame, text="🐾 Log Study Hours — Paws & Pages", font=("Arial", 14), bg="#FFF0FA", fg="#F48FB1").pack(pady=10)

    # Fetch current user data from MongoDB
    user_doc = users_col.find_one({"_id": username})
    if not user_doc:
        messagebox.showerror("Error", "User not found in database!")
        return log_hours_frame

    hours_logged = user_doc.get("hoursLogged", 0.0)
    points = user_doc.get("pointsEarned", 0)

    # Display stats
    hours_label = tk.Label(log_hours_frame, text=f"🐱 Total Hours Logged: {hours_logged}", bg="#FFF0FA", fg="#888")
    hours_label.pack(pady=5)

    points_label = tk.Label(log_hours_frame, text=f"🐾 Total Paw Points: {points}", bg="#FFF0FA", fg="#F48FB1", font=("Arial", 10, "bold"))
    points_label.pack(pady=5)

    tk.Label(log_hours_frame, text="🕐 Hours to add:", bg="#FFF0FA", fg="#888").pack(pady=5)
    hours_entry = tk.Entry(log_hours_frame, relief="flat", bg="#FFF5FB", fg="#C06080", highlightthickness=1, highlightbackground="#F9A8C9")
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
            hours_label.config(text=f"🐱 Total Hours Logged: {hours_logged}")
            points_label.config(text=f"🐾 Total Paw Points: {points}")

            messagebox.showinfo("Success", f"{added_hours} hours added! ({earned_points} points)")
            hours_entry.delete(0, tk.END)

        except:
            messagebox.showerror("Error", "Enter a valid number of hours.")

    tk.Button(log_hours_frame, text="🐱 Add Hours", command=add_hours,
              bg="#F9A8C9", fg="white", relief="flat", padx=20, pady=6, cursor="hand2").pack(pady=10)

    return log_hours_frame