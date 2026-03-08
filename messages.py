import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from addMongo import users_col, messages_col  # MongoDB collections

def create_messages_tab(parent, username):
    messages_frame = tk.Frame(parent, bg="#FFF0F8")

    tk.Label(messages_frame, text="💌 Paws & Pages Messages 🐱", font=("Arial", 14), bg="#FFF0F8", fg="#F7A8C4").pack(pady=10)

    chat_list_frame = tk.Frame(messages_frame, bg="#FFF0F8")
    chat_list_frame.pack()

    # ── Helper: get mutual matches from DB ─────────────────────────────
    def get_mutual_matches():
        user_doc = users_col.find_one({"_id": username})
        if not user_doc:
            return []
        matches = user_doc.get("matches", [])

        mutual = []
        for match in matches:
            match_doc = users_col.find_one({"_id": match})
            if match_doc and username in match_doc.get("matches", []):
                mutual.append(match)
        return mutual

    # ── Open a chat window with a matched user ─────────────────────────
    def open_chat(other_user):
        chat_window = tk.Toplevel()
        chat_window.title(f"🐱 Chat with {other_user}")
        chat_window.geometry("400x400")
        chat_window.configure(bg="#FFF0F8")

        users = sorted([username, other_user])
        chat_id = f"{users[0]}-{users[1]}"

        chat_display = tk.Text(chat_window, state="disabled", bg="#FFF0F8", fg="#555", relief="flat", padx=8, pady=8)
        chat_display.pack(padx=10, pady=10, fill="both", expand=True)

        entry = tk.Entry(chat_window, bg="#FFF0F8", fg="#5B7DB1", relief="flat", highlightthickness=1, highlightbackground="#A8C8F7")
        entry.pack(fill="x", padx=10, pady=5)

        def load_chat():
            chat_display.config(state="normal")
            chat_display.delete("1.0", tk.END)

            chat_doc = messages_col.find_one({"_id": chat_id})
            if chat_doc:
                for msg in chat_doc.get("chat", []):
                    chat_display.insert(tk.END, f"{msg['sender']}: {msg['message']}\n")

            chat_display.config(state="disabled")
            chat_display.see(tk.END)

        def send_message():
            msg_text = entry.get().strip()
            if not msg_text:
                return

            timestamp = datetime.now().isoformat(timespec="seconds")
            new_msg = {"sender": username, "message": msg_text, "timestamp": timestamp}

            # Update the chat in MongoDB
            messages_col.update_one(
                {"_id": chat_id},
                {"$push": {"chat": new_msg}},
                upsert=True
            )

            entry.delete(0, tk.END)
            load_chat()

        tk.Button(chat_window, text="💌 Send Meow-ssage", command=send_message, bg="#F9A8C9", fg="#FFFFFF", relief="groove", padx=16, pady=6, cursor="hand2", font=("Arial", 10, "bold")).pack(pady=5)

        # Auto-refresh chat every second
        def auto_refresh():
            if chat_window.winfo_exists():
                load_chat()
                chat_window.after(1000, auto_refresh)

        load_chat()
        auto_refresh()

    # ── Refresh the chat list of mutual matches ────────────────────────
    def refresh_chats():
        for widget in chat_list_frame.winfo_children():
            widget.destroy()

        mutual_matches = get_mutual_matches()

        if not mutual_matches:
            tk.Label(chat_list_frame, text="😿 No mutual matches yet", bg="#FFF0F8", fg="#9999BB").pack()
        else:
            for user in mutual_matches:
                tk.Button(
                    chat_list_frame,
                    text=f"🐱 Chat with {user}",
                    width=25,
                    bg="#F9A8C9",
                    fg="#FFFFFF",
                    relief="groove",
                    cursor="hand2",
                    font=("Arial", 10, "bold"),
                    command=lambda u=user: open_chat(u)
                ).pack(pady=3)

        messages_frame.after(3000, refresh_chats)  # refresh chat list every 3s

    refresh_chats()

    return messages_frame