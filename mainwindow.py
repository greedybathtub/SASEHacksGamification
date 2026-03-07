import tkinter as tk
from tkinter import ttk
from profile import create_profile_tab
from studyMatch import create_match_tab

def open_main_window(username):
    main_window = tk.Toplevel()
    main_window.title("Main Window")
    main_window.geometry("600x500")

    welcome_label = tk.Label(main_window, text=f"Welcome, {username}!", font=("Arial", 16))
    welcome_label.pack(pady=20)

    notebook = ttk.Notebook(main_window)
    notebook.pack(expand=True, fill='both')

    home = tk.Frame(notebook)
    notebook.add(home, text="Home")

    profile = create_profile_tab(notebook, username)
    notebook.add(profile, text="Profile")

    studyMatch = create_match_tab(notebook, username)
    notebook.add(studyMatch, text="Study Match")

    settings = tk.Frame(notebook)
    notebook.add(settings, text="Settings")

    tk.Label(settings, text="Settings tab").pack(pady=20)

    def logout():
        main_window.destroy()

    tk.Button(main_window, text="Close", command=logout).pack(pady=10)

    main_window.mainloop()