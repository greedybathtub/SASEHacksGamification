import tkinter as tk
from tkinter import messagebox
from addMongo import users_col  # MongoDB Users collection

def create_match_tab(parent, username):
    match_frame = tk.Frame(parent)

    tk.Label(match_frame, text="Find study partners!", font=("Arial", 14)).pack(pady=10)

    # Load all users except current
    other_users_cursor = users_col.find({"_id": {"$ne": username}})
    other_users = list(other_users_cursor)

    # Load current user's matches to skip already matched users
    current_user_doc = users_col.find_one({"_id": username})
    existing_matches = current_user_doc.get("matches", []) if current_user_doc else []

    # Filter out users already matched
    unmatched_users = [u for u in other_users if u["_id"] not in existing_matches]

    if not unmatched_users:
        tk.Label(match_frame, text="No other users found.").pack(pady=20)
        return match_frame

    profile_index = tk.IntVar(value=0)

    profile_display = tk.Frame(match_frame)
    profile_display.pack(pady=20)

    # UI Labels
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

    # Current user's quiz data
    current_user_data = {
        "StudyStyle": current_user_doc.get("studyStyle", "") if current_user_doc else "",
        "StudyTime": current_user_doc.get("studyTime", "") if current_user_doc else "",
        "Location": current_user_doc.get("location", "") if current_user_doc else "",
        "GroupSize": current_user_doc.get("groupSize", "") if current_user_doc else "",
    }

    def calculate_compatibility(other_user_data):
        quiz_keys = ["StudyStyle", "StudyTime", "Location", "GroupSize"]
        matches = sum(1 for key in quiz_keys if current_user_data.get(key) == other_user_data.get(key, ""))
        return int((matches / len(quiz_keys)) * 100)

    def load_profile(index):
        if index >= len(unmatched_users):
            messagebox.showinfo("Done!", "No more users to view.")
            return

        other_user_doc = unmatched_users[index]
        score = calculate_compatibility(other_user_doc)

        compatibility_label.config(text=f"Compatibility Score: {score}%")
        username_label.config(text=f"Username: {other_user_doc['_id']}")
        bio_label.config(text=f"Bio: {other_user_doc.get('bio','')}")
        school_label.config(text=f"School: {other_user_doc.get('school','')}")
        subjects_label.config(text=f"Subjects: {', '.join(other_user_doc.get('subjects', []))}")
        study_style_label.config(text=f"Study Style: {other_user_doc.get('studyStyle','')}")
        study_time_label.config(text=f"Study Time: {other_user_doc.get('studyTime','')}")
        location_label.config(text=f"Location: {other_user_doc.get('location','')}")
        group_size_label.config(text=f"Group Size: {other_user_doc.get('groupSize','')}")

    def save_match(matched_user):
        # Update matches array in MongoDB for current user
        users_col.update_one(
            {"_id": username},
            {"$addToSet": {"matches": matched_user}}
        )

    def match():
        if profile_index.get() < len(unmatched_users):
            matched_user = unmatched_users[profile_index.get()]["_id"]
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