import tkinter as tk
from tkinter import ttk
from profile import create_profile_tab
from studyMatch import create_match_tab
from messages import create_messages_tab
from loghours import create_log_hours_tab
from leaderboard import create_leaderboard_tab
from quests import create_quests_tab
import os
import sys  # needed to fully exit

# ── colors & fonts ─────────────────────────────────────────────────────────────
BG_OUTER  = "#F5D6A0"
BG_CARD   = "#B8D4EE"
ACCENT    = "#F4A0B5"
BTN_HOV   = "#F08098"
PIXEL_FONTS = ["Press Start 2P", "Courier New", "Courier", "monospace"]

def best_font(families, size, weight="normal"):
    import tkinter.font as tkfont
    available = tkfont.families()
    for f in families:
        if f in available:
            return (f, size, weight)
    return (families[-1], size, weight)

def open_main_window(username):
    main_window = tk.Toplevel()
    main_window.title("Study App")
    main_window.geometry("820x620")
    main_window.configure(bg=BG_OUTER)

    title_font = best_font(PIXEL_FONTS, 18, "bold")
    tab_font   = best_font(["Nunito", "Helvetica Neue", "Arial"], 10, "bold")

    # ── Top frame for welcome & logout ─────────────────────────────────
    top_frame = tk.Frame(main_window, bg=BG_OUTER)
    top_frame.pack(fill="x", padx=20, pady=(20,10))

    welcome_card = tk.Frame(top_frame, bg=BG_CARD, padx=15, pady=10, relief="raised", bd=2)
    welcome_card.pack(side="left", fill="x", expand=True)

    tk.Label(
        welcome_card,
        text=f"Welcome, {username}!",
        font=title_font,
        bg=BG_CARD,
        fg=ACCENT
    ).pack()

    # ── Logout button in top-right ─────────────────────────────────────
    def logout():
        main_window.destroy()
        sys.exit()  # fully exit program

    logout_btn = tk.Button(
        top_frame,
        text="Logout",
        command=logout,
        bg=ACCENT,
        fg="white",
        font=tab_font,
        padx=16,
        pady=6,
        relief="flat",
        cursor="hand2",
        activebackground=BTN_HOV,
        activeforeground="white"
    )
    logout_btn.pack(side="right")

    def on_enter(e):
        logout_btn.config(bg=BTN_HOV)
    def on_leave(e):
        logout_btn.config(bg=ACCENT)

    logout_btn.bind("<Enter>", on_enter)
    logout_btn.bind("<Leave>", on_leave)

    # ── Notebook / Tabs ───────────────────────────────────────────────
    notebook = ttk.Notebook(main_window)
    notebook.pack(expand=True, fill="both", padx=20, pady=(0,20))

    # ── Helper to wrap tabs in a card-style frame ──────────────────────
    def wrap_tab(tab_func):
        container = tk.Frame(notebook, bg=BG_OUTER)
        card = tk.Frame(container, bg=BG_CARD, padx=10, pady=10)
        card.pack(expand=True, fill="both", padx=10, pady=10)
        tab_frame = tab_func(card, username)
        tab_frame.pack(expand=True, fill="both")
        return container

    notebook.add(wrap_tab(create_leaderboard_tab), text="Leaderboard")
    notebook.add(wrap_tab(create_profile_tab), text="Profile")
    notebook.add(wrap_tab(create_match_tab), text="Study Match")
    notebook.add(wrap_tab(create_messages_tab), text="Messages")
    notebook.add(wrap_tab(create_quests_tab), text="Quests")
    notebook.add(wrap_tab(create_log_hours_tab), text="Log Hours")

    main_window.mainloop()