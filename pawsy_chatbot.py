import tkinter as tk, threading
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyDm8MaBxXTzXPbiK2rCeixtmozE7oAtboo"
SYSTEM = """You are Meow, a cat-themed AI assistant. Every response must include 
at least one cat pun. Be playful, warm, and fun. Keep responses short (2-3 sentences). 
Examples of puns: purr-fect, fur-real, claw-some, paw-sible, hiss-terical, meow-velous."""
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro", system_instruction=SYSTEM)
chat = model.start_chat()

# ── palette 
CHAT_BG  = "#FFE8F4"
BOT_BG   = "#FFFFFF"
USER_BG  = "#D6E8FF"
BORDER   = "#F0A8CC"
BTN_PINK = "#F9A8C9"
TXT      = "#2C2C3E"
GRAY     = "#C8A8B8"

root = tk.Tk()
root.title("🐾 Paws & Pages — Pawsy AI")
root.resizable(False, False)
root.configure(bg="#FFF0F8")

outer = tk.Frame(root, bg=BORDER); outer.pack(padx=30, pady=30)
inner = tk.Frame(outer, bg=BORDER); inner.pack(padx=2, pady=2)

# title bar
title_bar = tk.Frame(inner, bg=BTN_PINK, height=56)
title_bar.pack(fill="x"); title_bar.pack_propagate(False)
tk.Label(title_bar, text="≽^•⩊•^≼  PAWS & PAGES!", bg=BTN_PINK, fg=TXT,
         font=("Helvetica", 14, "bold")).pack(expand=True)
tk.Frame(inner, bg="#A8C8F7", height=4).pack(fill="x")

# chat area
chat_frame = tk.Frame(inner, bg=CHAT_BG, width=320, height=280)
chat_frame.pack(fill="both"); chat_frame.pack_propagate(False)
canvas = tk.Canvas(chat_frame, bg=CHAT_BG, highlightthickness=0, width=320, height=280)
canvas.pack(side="left", fill="both", expand=True)
msg_container = tk.Frame(canvas, bg=CHAT_BG)
canvas.create_window((0, 0), window=msg_container, anchor="nw", width=310)
msg_container.bind("<Configure>", lambda e: [canvas.configure(scrollregion=canvas.bbox("all")), canvas.yview_moveto(1.0)])

def add_bubble(text, is_bot):
    row = tk.Frame(msg_container, bg=CHAT_BG); row.pack(fill="x", pady=4)
    bg = BOT_BG if is_bot else USER_BG
    border_c = "#F0A8CC" if is_bot else "#A8C8F0"
    bubble = tk.Frame(row, bg=bg, highlightthickness=1, highlightbackground=border_c)
    bubble.pack(anchor="w" if is_bot else "e", padx=(10,60) if is_bot else (60,10))
    prefix = "🐱 " if is_bot else "🫵 "
    tk.Label(bubble, text=prefix + text, bg=bg, fg=TXT, font=("Helvetica",11),
             wraplength=170, justify="left", padx=10, pady=8).pack()

add_bubble("So purr-leased to meowt you! My name is Pawsy! How can I help?", True)

# bottom bar
bottom = tk.Frame(inner, bg=BTN_PINK, pady=8); bottom.pack(fill="x")
ef = tk.Frame(bottom, bg=BOT_BG, highlightthickness=2, highlightbackground=BORDER)
ef.pack(side="left", padx=(12,6), ipady=4, fill="x", expand=True)
entry = tk.Entry(ef, bg=BOT_BG, fg=GRAY, font=("Helvetica",11), bd=0, highlightthickness=0, insertbackground=TXT)
entry.pack(fill="x", padx=8, pady=4); entry.insert(0, "Ask Meow Anything...")
entry.bind("<FocusIn>",  lambda e: (entry.delete(0,"end"), entry.config(fg=TXT)) if entry.get()=="Ask Meow Anything..." else None)
entry.bind("<FocusOut>", lambda e: (entry.insert(0,"Ask Meow Anything..."), entry.config(fg=GRAY)) if not entry.get() else None)

def send_message():
    text = entry.get().strip()
    if not text or text == "Ask Meow Anything...": return
    entry.delete(0, "end")
    add_bubble(text, False)
    thinking = tk.Frame(msg_container, bg=CHAT_BG); thinking.pack(fill="x", pady=2)
    tk.Label(thinking, text="Pawsy is thinking... 🐈🐈🐈", bg=CHAT_BG, fg=GRAY, font=("Helvetica",10,"italic")).pack(anchor="w", padx=10)
    root.update()
    def fetch():
        try: reply = chat.send_message(text).text
        except Exception as ex: reply = f"Paw-don me, error! ({ex})"
        root.after(0, lambda: [thinking.destroy(), add_bubble(reply, True)])
    threading.Thread(target=fetch, daemon=True).start()

bf = tk.Frame(bottom, bg="#F07AB0", width=48, height=48)
bf.pack(side="right", padx=(0,12)); bf.pack_propagate(False)
tk.Button(bf, text="🐾", bg="#F07AB0", fg="white", font=("Helvetica",16), bd=0,
          cursor="hand2", activebackground=BORDER, command=send_message).pack(expand=True, fill="both")
entry.bind("<Return>", lambda e: send_message())
root.mainloop()