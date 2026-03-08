import tkinter as tk
from tkinter import messagebox
import os
import random
import pointshelpers

QUEST_POOL = [
    {"task": "Finish 1 LeetCode problem",          "points_reward": 10, "icon": "💻"},
    {"task": "Read 10 pages of textbook",           "points_reward": 5,  "icon": "📖"},
    {"task": "Review your notes for 30 min",        "points_reward": 8,  "icon": "📝"},
    {"task": "Join a group study session",          "points_reward": 15, "icon": "👥"},
    {"task": "Watch a lecture video",               "points_reward": 6,  "icon": "🎬"},
    {"task": "Make flashcards for a topic",         "points_reward": 7,  "icon": "🃏"},
    {"task": "Solve 3 practice problems",           "points_reward": 12, "icon": "🧮"},
    {"task": "Write a summary of today's class",    "points_reward": 9,  "icon": "✍️"},
    {"task": "Study for 2 hours straight",          "points_reward": 20, "icon": "⏱️"},
    {"task": "Help a classmate understand a topic", "points_reward": 15, "icon": "🤝"},
    {"task": "Complete a past exam paper",          "points_reward": 18, "icon": "📄"},
    {"task": "Attend office hours",                 "points_reward": 12, "icon": "🏫"},
]

def create_quests_tab(parent, username):

    frame = tk.Frame(parent)

    tk.Label(frame, text="📋 STUDY QUESTS", font=("Arial", 14, "bold")).pack(pady=(10,2))
    tk.Label(frame, text="Complete quests to earn Points!", font=("Arial", 10)).pack(pady=(0,10))

    user_file = os.path.join("userInfo", f"{username}.txt")

    total_points = pointshelpers.get_points(user_file)

    points_label = tk.Label(frame, text=f"Total Points: {total_points}", font=("Arial", 12, "bold"))
    points_label.pack(pady=(0,10))

    quest_container = tk.Frame(frame)
    quest_container.pack(fill="both", expand=True)


    def build_quest_card(parent, quest):

        card = tk.Frame(parent, bd=1, relief="solid", padx=8, pady=6)
        card.pack(fill="x", pady=4, padx=10)

        icon = tk.Label(card, text=quest["icon"], font=("Arial", 18))
        icon.pack(side="left", padx=(0,10))

        text_frame = tk.Frame(card)
        text_frame.pack(side="left", fill="x", expand=True)

        task_label = tk.Label(text_frame, text=quest["task"], font=("Arial", 10), anchor="w")
        task_label.pack(anchor="w")

        reward_label = tk.Label(
            text_frame,
            text=f"+{quest['points_reward']} Points",
            font=("Arial", 8, "bold"),
            fg="green"
        )
        reward_label.pack(anchor="w")

        complete_btn = tk.Button(card, text="Complete ✓", bg="green", fg="white")
        complete_btn.pack(side="right", padx=6)


        def complete():

            # Disable immediately to prevent double clicks
            complete_btn.config(state="disabled")

            pointshelpers.add_points(user_file, quest["points_reward"])

            total = pointshelpers.get_points(user_file)
            points_label.config(text=f"Total Points: {total}")

            # Mark quest completed visually
            task_label.config(fg="gray")
            reward_label.config(text="Completed ✓", fg="gray")
            complete_btn.config(text="Done", bg="gray")

            messagebox.showinfo(
                "Quest Complete! 🎉",
                f"You earned +{quest['points_reward']} Points!\n{quest['task']}"
            )
        complete_btn.config(command=complete)


    def load_quests():

        for w in quest_container.winfo_children():
            w.destroy()

        selected = random.sample(QUEST_POOL, 5)

        for quest in selected:
            build_quest_card(quest_container, quest)


    load_quests()

    tk.Button(frame, text="🎲 Load New Quests", command=load_quests).pack(pady=6)

    return frame