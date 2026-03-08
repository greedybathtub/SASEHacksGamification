# mainwindow.py - Main application window with tabs for Paws & Pages
import tkinter as tk
from tkinter import ttk
from userProfile import create_profile_tab
from studyMatch import create_match_tab
from messages import create_messages_tab
from loghours import create_log_hours_tab
from leaderboard import create_leaderboard_tab
from quests import create_quests_tab
import os
import sys
from chatbot import create_chatbot_tab


BG_OUTER  = "#FFF0F8"   
BG_CARD   = "#FFFFFF"   
ACCENT    = "#F9A8C9"   
BTN_HOV   = "#F07AB0"   
TAB_PINK  = "#F9C8DF"   
TAB_BLUE  = "#A8C8F7"   
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
    main_window.title("🐾 Paws & Pages")
    main_window.geometry("820x620")
    main_window.configure(bg=BG_OUTER)

    tab_font = best_font(["Nunito", "Helvetica Neue", "Arial"], 10, "bold")

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TNotebook",
        background=BG_OUTER,
        borderwidth=0,
        tabmargins=[4, 4, 0, 0]
    )
    style.configure("TNotebook.Tab",
        background=TAB_PINK,
        foreground="#3A2A3A",
        font=("Helvetica", 10, "bold"),
        padding=[14, 7],
        borderwidth=1,
        relief="raised"
    )
    style.map("TNotebook.Tab",
        background=[("selected", TAB_BLUE), ("active", "#FFD6EC")],
        foreground=[("selected", "#1A2C6B"), ("active", "#3A2A3A")],
        relief=[("selected", "flat")]
    )
    style.configure("TFrame", background=BG_OUTER)
 
    top_frame = tk.Frame(main_window, bg=BG_OUTER)
    top_frame.pack(fill="x", padx=20, pady=(20, 10))

    welcome_card = tk.Frame(top_frame, bg=BG_CARD, padx=20, pady=12, relief="groove", bd=2)
    welcome_card.pack(side="left", fill="x", expand=True)

    tk.Label(
        welcome_card,
        text="≽^•⩊•^≼   Paws & Pages",
        font=best_font(PIXEL_FONTS, 20, "bold"),
        bg=BG_CARD,
        fg=TAB_BLUE
    ).pack(anchor="w")

    tk.Label(
        welcome_card,
        text=f"🐾 nyaa, welcome back {username}! ♡",
        font=best_font(["Nunito", "Helvetica Neue", "Arial"], 11),
        bg=BG_CARD,
        fg=ACCENT
    ).pack(anchor="w")

    def logout():
        main_window.destroy()
        sys.exit()

    logout_btn = tk.Button(
        top_frame,
        text="👋 Logout",
        command=logout,
        bg=TAB_PINK,
        fg="#3A2A3A",
        font=tab_font,
        padx=20,
        pady=10,
        relief="groove",
        cursor="hand2",
        activebackground=BTN_HOV,
        activeforeground="white"
    )
    logout_btn.pack(side="right", padx=(16, 0))

    def on_enter(e): logout_btn.config(bg=BTN_HOV, fg="white")
    def on_leave(e): logout_btn.config(bg=TAB_PINK, fg="#3A2A3A")
    logout_btn.bind("<Enter>", on_enter)
    logout_btn.bind("<Leave>", on_leave)
 
    notebook = ttk.Notebook(main_window, style="TNotebook")
    notebook.pack(expand=True, fill="both", padx=20, pady=(0, 20))

    def wrap_tab(tab_func):
        container = tk.Frame(notebook, bg=BG_OUTER)
        card = tk.Frame(container, bg=BG_CARD, padx=10, pady=10)
        card.pack(expand=True, fill="both", padx=10, pady=10)
        tab_frame = tab_func(card, username)
        tab_frame.pack(expand=True, fill="both")
        return container

    notebook.add(wrap_tab(create_leaderboard_tab), text="🏆 Leaderboard")
    notebook.add(wrap_tab(create_profile_tab),      text="🐱 Profile")
    notebook.add(wrap_tab(create_match_tab),         text="🐾 Study Match")
    notebook.add(wrap_tab(create_messages_tab),      text="💌 Messages")
    notebook.add(wrap_tab(create_quests_tab),        text="📋 Quests")
    notebook.add(wrap_tab(create_log_hours_tab),     text="⏱️ Log Hours")
    notebook.add(wrap_tab(create_chatbot_tab),       text="🐈 Pawsy AI")

    main_window.mainloop()