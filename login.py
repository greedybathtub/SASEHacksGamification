import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
from mainwindow import open_main_window
import addMongo

#  colors 
BG_OUTER  = "#FFD6EC"   # pastel pink outer background
BG_CARD   = "#FFFFFF"   # white card
PINK      = "#F07AB0"   # hot pink accent
INPUT_BG  = "#FFF0F8"   # very light pink input
INPUT_FG  = "#C0608A"   # deep pink input text
BTN_BG    = "#F9A8C9"   # pastel pink button
BTN_FG    = "#FFFFFF"   # white button text
BTN_HOV   = "#F07AB0"   # deeper pink hover

PIXEL_FONTS = ["Press Start 2P", "Courier New", "Courier", "monospace"]

def best_font(families, size, weight="normal"):
    available = tkfont.families()
    for f in families:
        if f in available:
            return (f, size, weight)
    return (families[-1], size, weight)

#  MongoDB auth helpers 
def verify(username, password):
    user = addMongo.login_col.find_one({"_id": username})
    return user is not None and user.get("password") == password

def username_exists(username):
    return addMongo.login_col.find_one({"_id": username}) is not None

#  hover effect for button 
def on_enter(e, btn):
    btn.config(bg=BTN_HOV)

def on_leave(e, btn):
    btn.config(bg=BTN_BG)

#  createaccount window 
def create_account_window(parent):
    win = tk.Toplevel(parent)
    win.title("🐾 Paws & Pages — New Account")
    win.geometry("320x340")
    win.resizable(False, False)
    win.configure(bg=BG_OUTER)

    card = tk.Frame(win, bg=BG_CARD, bd=0)
    card.place(relx=0.5, rely=0.5, anchor="center", width=280, height=300)

    title_font = best_font(PIXEL_FONTS, 11, "bold")
    entry_font = best_font(["Nunito", "Helvetica Neue", "Helvetica"], 11)

    tk.Label(card, text="🐾 NEW ACCOUNT 🐾", font=title_font,
             fg=PINK, bg=BG_CARD).pack(pady=(22, 16))

    def make_entry(parent, placeholder, show=None):
        frame = tk.Frame(parent, bg=INPUT_BG, bd=0)
        frame.pack(padx=20, pady=6, fill="x")
        e = tk.Entry(frame, font=entry_font, bg=INPUT_BG, fg=INPUT_FG,
                     bd=0, relief="flat", show=show or "")
        e.insert(0, placeholder)
        e.pack(padx=14, pady=10, fill="x")

        def on_focus_in(ev, entry=e, ph=placeholder):
            if entry.get() == ph:
                entry.delete(0, "end")
                entry.config(fg="#C0608A")
                if show:
                    entry.config(show=show)

        def on_focus_out(ev, entry=e, ph=placeholder):
            if entry.get() == "":
                entry.config(fg=INPUT_FG)
                entry.config(show="")
                entry.insert(0, ph)

        e.bind("<FocusIn>",  on_focus_in)
        e.bind("<FocusOut>", on_focus_out)
        return e, frame

    u_entry, _ = make_entry(card, "Username")
    p_entry, _ = make_entry(card, "Password", show="*")

    def save():
        uname = u_entry.get().strip()
        pword = p_entry.get().strip()
        if uname in ("", "Username") or pword in ("", "Password"):
            messagebox.showerror("Error", "Fields cannot be empty.", parent=win)
            return
        if username_exists(uname):
            messagebox.showerror("Error", "Username already exists.", parent=win)
            return

        # Save login info
        addMongo.login_col.insert_one({"_id": uname, "password": pword})

        # Save empty user profile in user_col
        addMongo.users_col.insert_one({
            "_id": uname,
            "PointsEarned": 0,
            "HoursLogged": 0,
            "Bio": "",
            "School": "",
            "Subjects": "",
            "StudyStyle": "",
            "StudyTime": "",
            "Location": "",
            "GroupSize": "",
            "Matches": []
        })

        messagebox.showinfo("Success", f"Account for {uname} created!", parent=win)
        win.destroy()

    save_btn = tk.Button(
        card,
        text="🐾 Create Account 🐾",
        font=best_font(["Nunito", "Helvetica"], 11, "bold"),
        bg=BTN_BG,
        fg=BTN_FG,
        command=save
    )
    save_btn.pack(pady=20)
    save_btn.bind("<Enter>", lambda e: on_enter(e, save_btn))
    save_btn.bind("<Leave>", lambda e: on_leave(e, save_btn))

#  main login window 
def build_main():
    window = tk.Tk()
    window.title("🐾 Paws & Pages")
    window.geometry("375x667")
    window.resizable(False, False)
    window.configure(bg=BG_OUTER)

    card_w, card_h = 320, 580
    card = tk.Frame(window, bg=BG_CARD, bd=0)
    card.place(relx=0.5, rely=0.5, anchor="center", width=card_w, height=card_h)

    title_font = best_font(PIXEL_FONTS, 26, "bold")
    tk.Label(card, text="≽^•⩊•^≼", font=best_font(PIXEL_FONTS, 18, "bold"),
             fg="#F9A8C9", bg=BG_CARD).pack(pady=(30, 0))
    tk.Label(card, text="Paws & Pages", font=title_font,
             fg=PINK, bg=BG_CARD).pack(pady=(0, 6))
    tk.Label(card, text="~ your purr-fect study companion ~", font=best_font(["Nunito","Helvetica"],10),
             fg="#7A9EC8", bg=BG_CARD).pack(pady=(0, 20))

    entry_font = best_font(["Nunito", "Helvetica Neue", "Helvetica"], 13)
    entries = {}

    def make_field(placeholder, show=None):
        outer = tk.Frame(card, bg=INPUT_BG, bd=0)
        outer.pack(padx=24, pady=8, fill="x", ipady=2)
        e = tk.Entry(outer, font=entry_font, bg=INPUT_BG, fg=INPUT_FG,
                     bd=0, relief="flat", show=show or "",
                     highlightthickness=0)
        e.insert(0, placeholder)
        e.pack(padx=18, pady=12, fill="x")

        def focus_in(ev, entry=e, ph=placeholder):
            if entry.get() == ph:
                entry.delete(0, "end")
                entry.config(fg="#C0608A")
                if show:
                    entry.config(show=show)

        def focus_out(ev, entry=e, ph=placeholder):
            if entry.get() == "":
                entry.config(fg=INPUT_FG, show="")
                entry.insert(0, ph)

        e.bind("<FocusIn>",  focus_in)
        e.bind("<FocusOut>", focus_out)
        return e

    user_entry = make_field("Username")
    pass_entry = make_field("Password", show="*")
    entries["user"] = user_entry
    entries["pass"] = pass_entry

    btn_font = best_font(["Nunito", "Helvetica Neue", "Helvetica"], 12, "bold")

    def do_login():
        u = entries["user"].get()
        p = entries["pass"].get()
        if u in ("", "Username") or p in ("", "Password"):
            messagebox.showerror("Login Failed", "Please enter your credentials.")
            return
        if verify(u, p):
            messagebox.showinfo("Login Successful", f"Welcome, {u}! ♡")
            window.withdraw()
            open_main_window(u)
            window.deiconify()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    login_btn = tk.Button(card, text="🐾 Login 🐾", command=do_login,
                          bg=BTN_BG, fg=BTN_FG, font=btn_font,
                          bd=0, relief="flat", cursor="hand2",
                          activebackground=BTN_HOV, activeforeground=BTN_FG,
                          padx=60, pady=14)
    login_btn.pack(pady=(22, 0))
    login_btn.bind("<Enter>", lambda e: on_enter(e, login_btn))
    login_btn.bind("<Leave>", lambda e: on_leave(e, login_btn))

    link_font = best_font(["Nunito", "Helvetica Neue", "Helvetica"], 9)
    link = tk.Label(card, text="🐾 New here? Join the clowder!",
                    font=link_font, fg=PINK, bg=BG_CARD, cursor="hand2")
    link.pack(pady=(14, 0))
    link.bind("<Button-1>", lambda e: create_account_window(window))

    window.mainloop()


if __name__ == "__main__":
    build_main()