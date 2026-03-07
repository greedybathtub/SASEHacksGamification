import tkinter as tk
from tkinter import messagebox
import os

def create_match_tab(parent, username):
    match_frame = tk.Frame(parent)

    tk.Label(match_frame, text="Find study partners!", font=("Arial", 14)).pack(pady=10)

    user_files = [
        f for f in os.listdir("userInfo")
        if f.endswith(".txt") and f.replace(".txt", "") != username
    ]

    if not user_files:
        tk.Label(match_frame, text="No other users found.").pack(pady=20)
        return match_frame

    profile_index = tk.IntVar(value=0)

    profile_display = tk.Frame(match_frame)
    profile_display.pack(pady=20)

    compatibility_label = tk.Label(profile_display, text="", font=("Arial", 12, "bold"))
    compatibility_label.pack()

    username_label = tk.Label(profile_display, text="", font=("Arial", 12, "bold"))
    username_label.pack()

    bio_label = tk.Label(profile_display, text="", wraplength=350)
    bio_label.pack()

    school_label = tk.Label(profile_display, text="")
    school_label.pack()

    subjects_label = tk.Label(profile_display, text="")
    subjects_label.pack()

    study_style_label = tk.Label(profile_display, text="")
    study_style_label.pack()

    study_time_label = tk.Label(profile_display, text="")
    study_time_label.pack()

    location_label = tk.Label(profile_display, text="")
    location_label.pack()

    group_size_label = tk.Label(profile_display, text="")
    group_size_label.pack()

    # Load current user's answers
    current_user_file = os.path.join("userInfo", f"{username}.txt")
    current_user_data = {}

    if os.path.exists(current_user_file):
        with open(current_user_file, "r") as f:
            for line in f:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    current_user_data[key] = value.strip()

    def calculate_compatibility(other_user_data):
        quiz_keys = ["StudyStyle", "StudyTime", "Location", "GroupSize"]

        matches = 0
        for key in quiz_keys:
            if current_user_data.get(key) == other_user_data.get(key):
                matches += 1

        return int((matches / len(quiz_keys)) * 100)

    def load_profile(index):
        if index >= len(user_files):
            messagebox.showinfo("Done!", "No more users to view.")
            return

        filepath = os.path.join("userInfo", user_files[index])

        info = {}
        with open(filepath, "r") as f:
            for line in f:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    info[key] = value.strip()

        score = calculate_compatibility(info)

        compatibility_label.config(text=f"Compatibility Score: {score}%")
        username_label.config(text=f"Username: {user_files[index].replace('.txt','')}")
        bio_label.config(text=f"Bio: {info.get('Bio','')}")
        school_label.config(text=f"School: {info.get('School','')}")
        subjects_label.config(text=f"Subjects: {info.get('Subjects','')}")
        study_style_label.config(text=f"Study Style: {info.get('StudyStyle','')}")
        study_time_label.config(text=f"Study Time: {info.get('StudyTime','')}")
        location_label.config(text=f"Location: {info.get('Location','')}")
        group_size_label.config(text=f"Group Size: {info.get('GroupSize','')}")

    def save_match(matched_user):
        filepath = os.path.join("userInfo", f"{username}.txt")

        lines = []
        matches = []

        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                lines = f.readlines()

        for line in lines:
            if line.startswith("Matches:"):
                matches = line.replace("Matches:", "").strip().split(",")
                if matches == ['']:
                    matches = []

        if matched_user not in matches:
            matches.append(matched_user)

        updated_lines = []
        found_matches = False

        for line in lines:
            if line.startswith("Matches:"):
                updated_lines.append("Matches: " + ",".join(matches) + "\n")
                found_matches = True
            else:
                updated_lines.append(line)

        if not found_matches:
            updated_lines.append("Matches: " + ",".join(matches) + "\n")

        with open(filepath, "w") as f:
            f.writelines(updated_lines)

    def match():
        if profile_index.get() < len(user_files):
            matched_user = user_files[profile_index.get()].replace(".txt", "")
            save_match(matched_user)

            profile_index.set(profile_index.get() + 1)
            load_profile(profile_index.get())

    def skip():
        profile_index.set(profile_index.get() + 1)
        load_profile(profile_index.get())

    btn_frame = tk.Frame(match_frame)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Pass", command=skip, width=15, bg="red", fg="white").pack(side="right", padx=10)
    tk.Button(btn_frame, text="Match", command=match, width=15, bg="green", fg="white").pack(side="left", padx=10)

    load_profile(profile_index.get())

    return match_frame