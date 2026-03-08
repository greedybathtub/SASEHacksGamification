import tkinter as tk
from addMongo import users_col

# Colors
BG_OUTSIDE   = "#FFF0F8"
BG_CARD      = "#FFFFFF"
ACCENT_PINK  = "#F7A8C4"

def create_leaderboard_tab(parent, username):
    """Leaderboard tab showing users ranked by points earned with medals for top 3."""
    leaderboard_frame = tk.Frame(parent, bg=BG_OUTSIDE)
    leaderboard_frame.pack(fill="both", expand=True)

    title = tk.Label(
        leaderboard_frame,
        text="=^.^=  PAWS & PAGES LEADERBOARD  =^.^=",
        font=("Arial", 16, "bold"),
        bg=BG_OUTSIDE,
        fg=ACCENT_PINK
    )
    title.pack(pady=10)

    card_container = tk.Frame(leaderboard_frame, bg=BG_OUTSIDE)
    card_container.pack(fill="both", expand=True, padx=20, pady=10)

    medals = {0: "😺 1st", 1: "😸 2nd", 2: "😻 3rd"}

    def load_rankings():
        # Clear old rankings
        for w in card_container.winfo_children():
            w.destroy()

        # MongoDB query for all users, sort descending by pointsEarned
        rankings_cursor = users_col.find({}, {"_id": 1, "pointsEarned": 1}).sort("pointsEarned", -1)
        rankings = [(doc["_id"], doc.get("pointsEarned", 0)) for doc in rankings_cursor]

        if not rankings:
            tk.Label(card_container, text="No data yet!", bg=BG_OUTSIDE).pack(pady=20)
            return

        for i, (user, points) in enumerate(rankings):
            # Highlight current user
            bg_color = "#FFD6EC" if user == username else "#FFF0F8"
            fg_color = "#2C3E6B" if user == username else "#555577"

            frame = tk.Frame(card_container, bg=bg_color, padx=10, pady=6, relief="flat", bd=0)
            frame.pack(fill="x", pady=4)

            rank_text = medals.get(i, f"#{i+1}")  # medal for top 3, else rank number
            rank_label = tk.Label(frame, text=rank_text, width=4, bg=bg_color, fg=fg_color, font=("Arial", 10, "bold"))
            rank_label.pack(side="left")

            name_label = tk.Label(frame, text=user, bg=bg_color, fg=fg_color,
                                  font=("Arial", 10, "bold" if user == username else "normal"))
            name_label.pack(side="left", padx=10)

            points_label = tk.Label(frame, text=f"{points} pts", bg=bg_color, width=10, anchor="e")
            points_label.pack(side="right")

    # Initial load
    load_rankings()

    # Refresh button
    refresh_btn = tk.Button(
        leaderboard_frame,
        text="🐾 Refresh Rankings",
        command=load_rankings,
        bg="#F9A8C9",
        fg="#FFFFFF",
        relief="groove",
        padx=20,
        pady=6,
        cursor="hand2"
    )
    refresh_btn.pack(pady=10)

    return leaderboard_frame