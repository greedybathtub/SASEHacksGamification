import tkinter as tk
from tkinter import ttk

def open_main_window(username):
    main_window = tk.Toplevel()
    main_window.title("Main Window")
    main_window.geometry("400x300")

    welcome_label = tk.Label(main_window, text=f"Welcome, {username}!", font=("Arial", 16))
    welcome_label.pack(pady=20)

    notebook = ttk.Notebook(main_window)
    notebook.pack(expand=True, fill='both')

    home = tk.Frame(notebook)
    notebook.add(home, text="Home")

    profile = tk.Frame(notebook)
    notebook.add(profile, text="Profile")

    tk.Label(profile, text=f"User: {username}").pack(pady=20)

    settings = tk.Frame(notebook)
    notebook.add(settings, text="Settings")

    tk.Label(settings, text="Settings tab").pack(pady=20)

    main_window.mainloop()

    def logout():
        main_window.destroy()

    tk.Button(main_window, text="Close Window", command=logout).pack(pady=20)


    main_window.mainloop()