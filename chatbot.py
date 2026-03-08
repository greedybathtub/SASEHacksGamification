import tkinter as tk
import threading
import google.generativeai as genai

# ── Gemini API & chatbot setup ───────────────────────────────────────────────
GEMINI_API_KEY = "AIzaSyDm8MaBxXTzXPbiK2rCeixtmozE7oAtboo"
SYSTEM = """You are Meow, a cat-themed AI assistant. Every response must include 
at least one cat pun. Be playful, warm, and fun. Keep responses short (2-3 sentences). 
Examples of puns: purr-fect, fur-real, claw-some, paw-sible, hiss-terical, meow-velous."""
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro", system_instruction=SYSTEM)
chat = model.start_chat()


class PawsyChatbot:
    def __init__(self, parent):
        # Outer frame for the chatbot
        self.root_frame = tk.Frame(parent, bg="#c8c8c8")
        self.root_frame.pack(fill="both", expand=True, padx=10, pady=10)

        PINK = "#fdbddf"; YELLOW = "#fcf2b9"; BOT_BG = "#ffffff"; USER_BG = "#bfdbfe"
        BORDER = "#4E484B"; TXT = "#1a1a1a"; GRAY = "#9ca3af"

        # Chat display area
        chat_frame = tk.Frame(self.root_frame, bg=YELLOW)
        chat_frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(chat_frame, bg=YELLOW, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        self.msg_container = tk.Frame(canvas, bg=YELLOW)
        canvas.create_window((0, 0), window=self.msg_container, anchor="nw")
        self.msg_container.bind(
            "<Configure>",
            lambda e: [canvas.configure(scrollregion=canvas.bbox("all")), canvas.yview_moveto(1.0)]
        )

        # Bottom input frame
        bottom = tk.Frame(self.root_frame, bg=YELLOW, pady=10)
        bottom.pack(fill="x")
        ef = tk.Frame(bottom, bg=BOT_BG, highlightthickness=2, highlightbackground=BORDER)
        ef.pack(side="left", padx=(6,6), ipady=4, fill="x", expand=True)
        self.entry = tk.Entry(ef, bg=BOT_BG, fg=GRAY, font=("Helvetica",11), bd=0, highlightthickness=0, insertbackground=TXT)
        self.entry.pack(fill="x", padx=8, pady=4)
        self.entry.insert(0, "Ask Meow Anything...")
        self.entry.bind("<FocusIn>", lambda e: (self.entry.delete(0,"end"), self.entry.config(fg=TXT)) if self.entry.get()=="Ask Meow Anything..." else None)
        self.entry.bind("<FocusOut>", lambda e: (self.entry.insert(0,"Ask Meow Anything..."), self.entry.config(fg=GRAY)) if not self.entry.get() else None)
        self.entry.bind("<Return>", lambda e: self.send_message())

        # Send button
        bf = tk.Frame(bottom, bg=BOT_BG, highlightthickness=2, highlightbackground=BORDER, width=42, height=42)
        bf.pack(side="right", padx=(0,12)); bf.pack_propagate(False)
        tk.Button(bf, text="→", bg=BOT_BG, fg=TXT, font=("Helvetica",14), bd=0,
                  cursor="hand2", activebackground="#FF4CA3", command=self.send_message).pack(expand=True, fill="both")

        # Initial greeting
        self.add_bubble("So purr-leased to meowt you! My name is Pawsy! How can I help?", True)

    def add_bubble(self, text, is_bot):
        row = tk.Frame(self.msg_container, bg="#fcf2b9"); row.pack(fill="x", pady=4)
        bg = "#ffffff" if is_bot else "#bfdbfe"
        bubble = tk.Frame(row, bg=bg, highlightthickness=2, highlightbackground="#4E484B")
        bubble.pack(anchor="w" if is_bot else "e", padx=(10,60) if is_bot else (60,10))
        tk.Label(bubble, text=text, bg=bg, fg="#1a1a1a", font=("Helvetica",11),
                 wraplength=170, justify="left", padx=10, pady=8).pack()

    def send_message(self):
        text = self.entry.get().strip()
        if not text or text == "Ask Meow Anything...": return
        self.entry.delete(0, "end")
        self.add_bubble(text, False)
        thinking = tk.Frame(self.msg_container, bg="#fcf2b9"); thinking.pack(fill="x", pady=2)
        tk.Label(thinking, text="Pawsy is thinking... 🐈🐈🐈", bg="#fcf2b9", fg="#9ca3af", font=("Helvetica",10,"italic")).pack(anchor="w", padx=10)

        def fetch():
            try:
                reply = chat.send_message(text).text
            except Exception as ex:
                reply = f"Paw-don me, error! ({ex})"
            # update UI in main thread
            self.msg_container.after(0, lambda: [thinking.destroy(), self.add_bubble(reply, True)])

        threading.Thread(target=fetch, daemon=True).start()


# ── function to create the tab ───────────────────────────────────────────────
def create_chatbot_tab(parent, username=None):
    """Call this to add the chatbot tab inside any parent frame"""
    return PawsyChatbot(parent).root_frame