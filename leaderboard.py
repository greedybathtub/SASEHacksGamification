import tkinter as tk
import os
import pointshelpers

# Colors
BG_OUTSIDE   = "#FDE6B0"
BG_CARD      = "#C2DFFF"
ACCENT_PINK  = "#FFB6C1"

def get_rankings(user_folder="userInfo"):
    """Return a list of (username, points) sorted descending."""
    if not os.path.exists(user_folder):
        return []
    rankings = []
    for filename in os.listdir(user_folder):
        if filename.endswith(".txt"):
            username = filename.replace(".txt", "")
            filepath = os.path.join(user_folder, filename)
            points = pointshelpers.get_points(filepath)
            rankings.append((username, points))
    rankings.sort(key=lambda x: x[1], reverse=True)
    return rankings

def create_leaderboard_tab(parent, username):
    """Leaderboard tab showing users ranked by points earned with medals for top 3."""
    leaderboard_frame = tk.Frame(parent, bg=BG_OUTSIDE)
    leaderboard_frame.pack(fill="both", expand=True)

    title = tk.Label(
        leaderboard_frame,
        text="🏆 CAMPUS LEADERBOARD",
        font=("Arial", 16, "bold"),
        bg=BG_OUTSIDE,
        fg=ACCENT_PINK
    )
    title.pack(pady=10)

    card_container = tk.Frame(leaderboard_frame, bg=BG_OUTSIDE)
    card_container.pack(fill="both", expand=True, padx=20, pady=10)

    medals = {0: "🥇", 1: "🥈", 2: "🥉"}

    def load_rankings():
        # Clear old rankings
        for w in card_container.winfo_children():
            w.destroy()

        rankings = get_rankings()
        if not rankings:
            tk.Label(card_container, text="No data yet!", bg=BG_OUTSIDE).pack(pady=20)
            return

        for i, (user, points) in enumerate(rankings):
            # Highlight current user
            bg_color = "#fff" if user == username else BG_CARD
            fg_color = "#000" if user != username else ACCENT_PINK

            frame = tk.Frame(card_container, bg=bg_color, padx=10, pady=6, relief="raised", bd=1)
            frame.pack(fill="x", pady=4)

            # Medal for top 3, otherwise show rank number
            rank_text = medals.get(i, f"#{i+1}")
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
    refresh_btn = tk.Button(leaderboard_frame, text="🔄 Refresh", command=load_rankings, bg=ACCENT_PINK, fg="white")
    refresh_btn.pack(pady=10)

    return leaderboard_frame