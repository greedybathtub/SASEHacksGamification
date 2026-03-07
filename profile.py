import tkinter as tk
from tkinter import messagebox
import os

def create_profile_tab(parent, username):
    profile_frame = tk.Frame(parent)

    tk.Label(profile_frame, text=f"User: {username}", font=("Arial", 14)).pack(pady=10)

    tk.Label(profile_frame, text="Points Earned:").pack(anchor='w', padx=10)
    points_var = tk.StringVar(value="0")  # default 0 if file doesn't exist
    points_entry = tk.Entry(profile_frame, textvariable=points_var, width=10, state='readonly')
    points_entry.pack(padx=10, pady=5, anchor='w')

    tk.Label(profile_frame, text="Hours Logged:").pack(anchor='w', padx=10)
    hours_var = tk.StringVar(value="0")  # default 0 if file doesn't exist
    hours_entry = tk.Entry(profile_frame, textvariable=hours_var, width=10, state='readonly')
    hours_entry.pack(padx=10, pady=5, anchor='w')

    tk.Label(profile_frame, text="School:").pack(anchor='w', padx=10)
    school_entry = tk.Entry(profile_frame, width=50)
    school_entry.pack(padx=10, pady=5)

    tk.Label(profile_frame, text="Bio:").pack(anchor='w', padx=10)
    bio_text = tk.Text(profile_frame, width=50, height=5)
    bio_text.pack(padx=10, pady=5)

    tk.Label(profile_frame, text="Subjects of Interest (comma-separated):").pack(anchor='w', padx=10)
    subjects_entry = tk.Entry(profile_frame, width=50)
    subjects_entry.pack(padx=10, pady=5)

    tk.Label(profile_frame, text="Group Study Preferences Quiz:", font=("Arial", 12, "bold")).pack(pady=10)

    quiz_frame = tk.Frame(profile_frame)
    quiz_frame.pack(padx=10, pady=5)

    tk.Label(quiz_frame, text="1. Preferred study style:").grid(row=0, column=0, sticky='w')
    study_style_var = tk.StringVar(value="Group")
    tk.Radiobutton(quiz_frame, text="Quiet group", variable=study_style_var, value="Quiet group").grid(row=0, column=1)
    tk.Radiobutton(quiz_frame, text="Active discussion", variable=study_style_var, value="Active discussion").grid(row=0, column=2)
    tk.Radiobutton(quiz_frame, text="Either", variable=study_style_var, value="Either").grid(row=0, column=3)

    tk.Label(quiz_frame, text="2. Preferred study time:").grid(row=1, column=0, sticky='w')
    study_time_var = tk.StringVar(value="Afternoon")
    tk.Radiobutton(quiz_frame, text="Morning", variable=study_time_var, value="Morning").grid(row=1, column=1)
    tk.Radiobutton(quiz_frame, text="Afternoon", variable=study_time_var, value="Afternoon").grid(row=1, column=2)
    tk.Radiobutton(quiz_frame, text="Evening", variable=study_time_var, value="Evening").grid(row=1, column=3)

    tk.Label(quiz_frame, text="3. Preferred study location:").grid(row=2, column=0, sticky='w')
    study_location_var = tk.StringVar(value="Library")
    tk.Radiobutton(quiz_frame, text="Library", variable=study_location_var, value="Library").grid(row=2, column=1)
    tk.Radiobutton(quiz_frame, text="Cafe", variable=study_location_var, value="Cafe").grid(row=2, column=2)
    tk.Radiobutton(quiz_frame, text="Dorm/Room", variable=study_location_var, value="Dorm/Room").grid(row=2, column=3)
    tk.Radiobutton(quiz_frame, text="Either", variable=study_location_var, value="Either").grid(row=2, column=4)

    tk.Label(quiz_frame, text="4. Preferred group size:").grid(row=3, column=0, sticky='w')
    group_size_var = tk.StringVar(value="Small (2-3)")
    tk.Radiobutton(quiz_frame, text="Small (2-3)", variable=group_size_var, value="Small (2-3)").grid(row=3, column=1)
    tk.Radiobutton(quiz_frame, text="Medium (4-6)", variable=group_size_var, value="Medium (4-6)").grid(row=3, column=2)
    tk.Radiobutton(quiz_frame, text="Large (7+)", variable=group_size_var, value="Large (7+)").grid(row=3, column=3)

    user_file_path = os.path.join("userInfo", f"{username}.txt")
    if os.path.exists(user_file_path):
        with open(user_file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("PointsEarned:"):
                    points_var.set(line.replace("PointsEarned:", "").strip())
                elif line.startswith("HoursLogged:"):
                    hours_var.set(line.replace("HoursLogged:", "").strip())
                elif line.startswith("School:"):
                    school_entry.insert(0, line.replace("School:", "").strip())
                elif line.startswith("Bio:"):
                    bio_text.insert(tk.END, line.replace("Bio:", "").strip())
                elif line.startswith("Subjects:"):
                    subjects_entry.insert(0, line.replace("Subjects:", "").strip())
                elif line.startswith("StudyStyle:"):
                    study_style_var.set(line.replace("StudyStyle:", "").strip())
                elif line.startswith("StudyTime:"):
                    study_time_var.set(line.replace("StudyTime:", "").strip())
                elif line.startswith("Location:"):
                    study_location_var.set(line.replace("Location:", "").strip())
                elif line.startswith("GroupSize:"):
                    group_size_var.set(line.replace("GroupSize:", "").strip())

    def save_profile():
        points = points_var.get()
        hours = hours_var.get()
        school = school_entry.get().strip()
        bio = bio_text.get("1.0", tk.END).strip()
        subjects = subjects_entry.get().strip()
        study_style = study_style_var.get()
        study_time = study_time_var.get()
        location = study_location_var.get()
        group_size = group_size_var.get()

        if not os.path.exists("userInfo"):
            os.makedirs("userInfo")

        with open(user_file_path, "w") as f:
            f.write(f"PointsEarned: {points_var.get()}\n")
            f.write(f"HoursLogged: {hours}\n")
            f.write(f"School: {school}\n")
            f.write(f"Bio: {bio}\n")
            f.write(f"Subjects: {subjects}\n")
            f.write(f"StudyStyle: {study_style}\n")
            f.write(f"StudyTime: {study_time}\n")
            f.write(f"Location: {location}\n")
            f.write(f"GroupSize: {group_size}\n")

        messagebox.showinfo("Saved", f"{username}'s profile has been saved!")

    tk.Button(profile_frame, text="Save Profile", command=save_profile).pack(pady=10)

    return profile_frame