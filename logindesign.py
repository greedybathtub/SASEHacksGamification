import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont

# ── colours ──────────────────────────────────────────────────────────────────
BG_OUTER  = "#F5D6A0"   # warm sandy yellow border
BG_CARD   = "#B8D4EE"   # soft sky blue card
PINK      = "#F4A0B5"   # pixel-art title / link pink
INPUT_BG  = "#F0F4F8"   # near-white input background
INPUT_FG  = "#8AA8C0"   # muted blue placeholder text
BTN_BG    = "#F4A0B5"   # pink login button
BTN_FG    = "#FFFFFF"
BTN_HOV   = "#F08098"

# ── pixel font fallback chain ─────────────────────────────────────────────────
PIXEL_FONTS = ["Press Start 2P", "Courier New", "Courier", "monospace"]


def best_font(families, size, weight="normal"):
    available = tkfont.families()
    for f in families:
        if f in available:
            return (f, size, weight)
    return (families[-1], size, weight)


# ── auth helpers ──────────────────────────────────────────────────────────────
def verify(user1, pass1):
    try:
        with open("users.txt", "r") as fh:
            for line in fh:
                parts = line.strip().split()
                if len(parts) == 2 and parts[0] == user1 and parts[1] == pass1:
                    return True
        return False
    except FileNotFoundError:
        messagebox.showerror("Error", "User file not found.")
        return False


def username_exists(username):
    try:
        with open("users.txt", "r") as fh:
            for line in fh:
                parts = line.strip().split()
                if parts and parts[0] == username:
                    return True
        return False
    except FileNotFoundError:
        return False


# ── rounded-rectangle canvas helper ──────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = [
        x1+r, y1,  x2-r, y1,
        x2,   y1,  x2,   y1+r,
        x2,   y2-r,x2,   y2,
        x2-r, y2,  x1+r, y2,
        x1,   y2,  x1,   y2-r,
        x1,   y1+r,x1,   y1,
        x1+r, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


# ── hover effect for button ───────────────────────────────────────────────────
def on_enter(e, btn):
    btn.config(bg=BTN_HOV)

def on_leave(e, btn):
    btn.config(bg=BTN_BG)


# ── create-account window ─────────────────────────────────────────────────────
def create_account_window():
    win = tk.Toplevel()
    win.title("Create Account")
    win.geometry("320x340")
    win.resizable(False, False)
    win.configure(bg=BG_OUTER)

    card = tk.Frame(win, bg=BG_CARD, bd=0)
    card.place(relx=0.5, rely=0.5, anchor="center", width=280, height=300)

    title_font = best_font(PIXEL_FONTS, 11, "bold")
    label_font = best_font(["Nunito", "Helvetica Neue", "Helvetica"], 9)
    entry_font = best_font(["Nunito", "Helvetica Neue", "Helvetica"], 11)

    tk.Label(card, text="NEW ACCOUNT", font=title_font,
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
                entry.config(fg="#4a6a85")
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
        with open("users.txt", "a") as fh:
            fh.write(uname + " " + pword + "\n")
        messagebox.showinfo("Success", f"Account for {uname} created!", parent=win)
        win.destroy()

    btn = tk.Button(card, text="Create Account", command=save,
                    bg=BTN_BG, fg=BTN_FG, font=(label_font[0], 10, "bold"),
                    bd=0, relief="flat", cursor="hand2",
                    activebackground=BTN_HOV, activeforeground=BTN_FG,
                    padx=20, pady=8)
    btn.pack(pady=(14, 0))
    btn.bind("<Enter>", lambda e: on_enter(e, btn))
    btn.bind("<Leave>", lambda e: on_leave(e, btn))


# ── main window ───────────────────────────────────────────────────────────────
def build_main():
    window = tk.Tk()
    window.title("Login")
    window.geometry("375x667")
    window.resizable(False, False)
    window.configure(bg=BG_OUTER)

    # ── card ──────────────────────────────────────────────────────────────────
    card_w, card_h = 320, 580
    card = tk.Frame(window, bg=BG_CARD, bd=0)
    card.place(relx=0.5, rely=0.5, anchor="center", width=card_w, height=card_h)

    # ── pixel-art title ───────────────────────────────────────────────────────
    title_font = best_font(PIXEL_FONTS, 26, "bold")
    tk.Label(card, text="LOGIN", font=title_font,
             fg=PINK, bg=BG_CARD).pack(pady=(60, 40))

    # ── input factory ─────────────────────────────────────────────────────────
    entry_font = best_font(["Nunito", "Helvetica Neue", "Helvetica"], 13)
    entries = {}

    def make_field(placeholder, show=None):
        outer = tk.Frame(card, bg=INPUT_BG, bd=0)
        outer.pack(padx=24, pady=8, fill="x", ipady=2)
        # rounded feel via canvas
        e = tk.Entry(outer, font=entry_font, bg=INPUT_BG, fg=INPUT_FG,
                     bd=0, relief="flat", show=show or "",
                     highlightthickness=0)
        e.insert(0, placeholder)
        e.pack(padx=18, pady=12, fill="x")

        def focus_in(ev, entry=e, ph=placeholder):
            if entry.get() == ph:
                entry.delete(0, "end")
                entry.config(fg="#2d5578")
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

    # ── login button ──────────────────────────────────────────────────────────
    btn_font = best_font(["Nunito", "Helvetica Neue", "Helvetica"], 12, "bold")

    def do_login():
        u = entries["user"].get()
        p = entries["pass"].get()
        if u in ("", "Username") or p in ("", "Password"):
            messagebox.showerror("Login Failed", "Please enter your credentials.")
            return
        if verify(u, p):
            messagebox.showinfo("Login Successful", f"Welcome, {u}! ♡")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    login_btn = tk.Button(card, text="Login", command=do_login,
                          bg=BTN_BG, fg=BTN_FG, font=btn_font,
                          bd=0, relief="flat", cursor="hand2",
                          activebackground=BTN_HOV, activeforeground=BTN_FG,
                          padx=60, pady=11)
    login_btn.pack(pady=(22, 0))
    login_btn.bind("<Enter>", lambda e: on_enter(e, login_btn))
    login_btn.bind("<Leave>", lambda e: on_leave(e, login_btn))

    # ── "New Member?" link ────────────────────────────────────────────────────
    link_font = best_font(["Nunito", "Helvetica Neue", "Helvetica"], 9)
    link = tk.Label(card, text="New Member? Create an Account!",
                    font=link_font, fg=PINK, bg=BG_CARD, cursor="hand2")
    link.pack(pady=(14, 0))
    link.bind("<Button-1>", lambda e: create_account_window())

    window.mainloop()


if __name__ == "__main__":
    build_main()
