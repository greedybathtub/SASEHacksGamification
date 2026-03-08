#  chatbot.py - A playful cat-themed AI assistant using Google Gemini API and Tkinter GUI
import tkinter as tk
import threading
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyDm8MaBxXTzXPbiK2rCeixtmozE7oAtboo"
SYSTEM = """You are Meow, a cat-themed AI assistant. Every response must include 
at least one cat pun. Be playful, warm, and fun. Keep responses short (2-3 sentences). 
Examples of puns: purr-fect, fur-real, claw-some, paw-sible, hiss-terical, meow-velous."""
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro", system_instruction=SYSTEM)
chat = model.start_chat()

#  palette 
CHAT_BG  = "#FFE8F4"   
BOT_BG   = "#FFFFFF"   
USER_BG  = "#D6E8FF"   
BORDER   = "#F0A8CC"   
BTN_PINK = "#F9A8C9"   
TXT      = "#2C2C3E"  
GRAY     = "#C8A8B8"  
OUTER_BG = "#FFF0F8"  

class PawsyChatbot:
    def __init__(self, parent):
        self.root_frame = tk.Frame(parent, bg=OUTER_BG)
        self.root_frame.pack(fill="both", expand=True, padx=10, pady=10)
 
        header = tk.Frame(self.root_frame, bg=BTN_PINK, pady=8)
        header.pack(fill="x")
        tk.Label(header, text="≽^•⩊•^≼  Pawsy AI  🐾",
                 bg=BTN_PINK, fg=TXT,
                 font=("Helvetica", 13, "bold")).pack()
        tk.Label(header, text="your purr-sonal study assistant",
                 bg=BTN_PINK, fg="#7A3A5A",
                 font=("Helvetica", 9, "italic")).pack()

        chat_frame = tk.Frame(self.root_frame, bg=CHAT_BG)
        chat_frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(chat_frame, bg=CHAT_BG, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        self.msg_container = tk.Frame(canvas, bg=CHAT_BG)
        canvas.create_window((0, 0), window=self.msg_container, anchor="nw")
        self.msg_container.bind(
            "<Configure>",
            lambda e: [canvas.configure(scrollregion=canvas.bbox("all")), canvas.yview_moveto(1.0)]
        )

        bottom = tk.Frame(self.root_frame, bg=BTN_PINK, pady=8)
        bottom.pack(fill="x")
        ef = tk.Frame(bottom, bg=BOT_BG, highlightthickness=2, highlightbackground=BORDER)
        ef.pack(side="left", padx=(10, 6), ipady=4, fill="x", expand=True)
        self.entry = tk.Entry(ef, bg=BOT_BG, fg=GRAY, font=("Helvetica", 11),
                              bd=0, highlightthickness=0, insertbackground=TXT)
        self.entry.pack(fill="x", padx=8, pady=4)
        self.entry.insert(0, "Ask Meow Anything...")
        self.entry.bind("<FocusIn>",  lambda e: (self.entry.delete(0, "end"), self.entry.config(fg=TXT)) if self.entry.get() == "Ask Meow Anything..." else None)
        self.entry.bind("<FocusOut>", lambda e: (self.entry.insert(0, "Ask Meow Anything..."), self.entry.config(fg=GRAY)) if not self.entry.get() else None)
        self.entry.bind("<Return>", lambda e: self.send_message())
 
        bf = tk.Frame(bottom, bg="#F07AB0", width=48, height=48)
        bf.pack(side="right", padx=(0, 10))
        bf.pack_propagate(False)
        tk.Button(bf, text="🐾", bg="#F07AB0", fg="white",
                  font=("Helvetica", 16), bd=0,
                  cursor="hand2", activebackground=BORDER,
                  command=self.send_message).pack(expand=True, fill="both")

        self.add_bubble("So purr-leased to meowt you! My name is Pawsy! How can I help?", True)

    def add_bubble(self, text, is_bot):
        row = tk.Frame(self.msg_container, bg=CHAT_BG)
        row.pack(fill="x", pady=4)
        bg = BOT_BG if is_bot else USER_BG
        border_c = "#F0A8CC" if is_bot else "#A8C8F0"
        bubble = tk.Frame(row, bg=bg, highlightthickness=1, highlightbackground=border_c)
        bubble.pack(anchor="w" if is_bot else "e",
                    padx=(10, 60) if is_bot else (60, 10))
        prefix = "🐱 " if is_bot else "🫵 "
        tk.Label(bubble, text=prefix + text, bg=bg, fg=TXT,
                 font=("Helvetica", 11),
                 wraplength=200, justify="left", padx=10, pady=8).pack()

    def send_message(self):
        text = self.entry.get().strip()
        if not text or text == "Ask Meow Anything...": return
        self.entry.delete(0, "end")
        self.add_bubble(text, False)
        thinking = tk.Frame(self.msg_container, bg=CHAT_BG)
        thinking.pack(fill="x", pady=2)
        tk.Label(thinking, text="Pawsy is thinking... 🐈🐈🐈",
                 bg=CHAT_BG, fg=GRAY,
                 font=("Helvetica", 10, "italic")).pack(anchor="w", padx=10)

        def fetch():
            try:
                reply = chat.send_message(text).text
            except Exception as ex:
                reply = f"Paw-don me, error! ({ex})"
            self.msg_container.after(0, lambda: [thinking.destroy(), self.add_bubble(reply, True)])

        threading.Thread(target=fetch, daemon=True).start()

def create_chatbot_tab(parent, username=None):
    """Call this to add the chatbot tab inside any parent frame"""
    return PawsyChatbot(parent).root_frame