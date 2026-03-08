# quests.py - Handles the Quests tab of the PAWS & PAGES app
import tkinter as tk
from tkinter import messagebox
import random
from addMongo import users_col

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

    frame = tk.Frame(parent, bg="#FFF0F8")

    tk.Label(frame, text="🐾 PAWS & PAGES QUESTS 🐾", font=("Arial", 14, "bold"), bg="#FFF0F8", fg="#5B7DB1").pack(pady=(10,2))
    tk.Label(frame, text="✨ Complete quests to earn Paw Points! 😸", font=("Arial", 10), bg="#FFF0F8", fg="#888").pack(pady=(0,10))

    user_doc = users_col.find_one({"_id": username})
    total_points = user_doc.get("pointsEarned", 0) if user_doc else 0

    points_label = tk.Label(frame, text=f"🐾 Total Paw Points: {total_points}", font=("Arial", 12, "bold"), bg="#FFF0F8", fg="#F7A8C4")
    points_label.pack(pady=(0,10))

    quest_container = tk.Frame(frame, bg="#FFF0F8")
    quest_container.pack(fill="both", expand=True)

    def build_quest_card(parent, quest):

        card = tk.Frame(parent, bg="#FFF0F8", padx=8, pady=6, relief="groove", bd=2)
        card.pack(fill="x", pady=4, padx=10)

        icon = tk.Label(card, text=quest["icon"], font=("Arial", 18), bg="#FFF0F8")
        icon.pack(side="left", padx=(0,10))

        text_frame = tk.Frame(card, bg="#FFF0F8")
        text_frame.pack(side="left", fill="x", expand=True)

        task_label = tk.Label(text_frame, text=quest["task"], font=("Arial", 10), anchor="w", bg="#FFF0F8", fg="#FFFFFF")
        task_label.pack(anchor="w")

        reward_label = tk.Label(
            text_frame,
            text=f"+{quest['points_reward']} Paw Points 🐾",
            font=("Arial", 8, "bold"),
            fg="#81C784",
            bg="#FFF0F8"
        )
        reward_label.pack(anchor="w")

        complete_btn = tk.Button(card, text="😸 Complete!", bg="#F9A8C9", fg="#FFFFFF", relief="groove", padx=8, pady=4, cursor="hand2", font=("Arial", 9, "bold"))
        complete_btn.pack(side="right", padx=6)

        def complete():
            complete_btn.config(state="disabled")

            users_col.update_one(
                {"_id": username},
                {"$inc": {"pointsEarned": quest["points_reward"]}},
                upsert=True
            )

            new_total = users_col.find_one({"_id": username}).get("pointsEarned", 0)
            points_label.config(text=f"🐾 Total Paw Points: {new_total}")

            task_label.config(fg="gray")
            reward_label.config(text="Completed ✓", fg="gray")
            complete_btn.config(text="✓ Done!", bg="#C8EAD7", fg="#2e7d52")

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

    tk.Button(frame, text="🐱 Meow! Load New Quests", command=load_quests,
              bg="#F9A8C9", fg="#FFFFFF", relief="groove", padx=16, pady=6, cursor="hand2", font=("Arial", 10, "bold")).pack(pady=6)

    return frame