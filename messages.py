import tkinter as tk
import os

def create_messages_tab(parent, username):
    messages_frame = tk.Frame(parent)

    tk.Label(messages_frame, text="Messages", font=("Arial", 14)).pack(pady=10)

    chat_list_frame = tk.Frame(messages_frame)
    chat_list_frame.pack()

    def get_mutual_matches():
        user_file = os.path.join("userInfo", f"{username}.txt")
        matches = []

        if os.path.exists(user_file):
            with open(user_file, "r") as f:
                for line in f:
                    if line.startswith("Matches:"):
                        matches = line.replace("Matches:", "").strip().split(",")
                        if matches == ['']:
                            matches = []

        mutual = []

        for match in matches:
            match_file = os.path.join("userInfo", f"{match}.txt")

            if os.path.exists(match_file):
                with open(match_file, "r") as f:
                    for line in f:
                        if line.startswith("Matches:"):
                            their_matches = line.replace("Matches:", "").strip().split(",")
                            if username in their_matches:
                                mutual.append(match)

        return mutual

    def open_chat(other_user):

        chat_window = tk.Toplevel()
        chat_window.title(f"Chat with {other_user}")
        chat_window.geometry("400x400")

        users = sorted([username, other_user])
        chat_file = os.path.join("MessageLog", f"{users[0]}-{users[1]}.txt")

        # Ensure chat file exists
        if not os.path.exists(chat_file):
            open(chat_file, "w").close()

        chat_display = tk.Text(chat_window, state="disabled")
        chat_display.pack(padx=10, pady=10, fill="both", expand=True)

        entry = tk.Entry(chat_window)
        entry.pack(fill="x", padx=10, pady=5)

        def load_chat():
            chat_display.config(state="normal")
            chat_display.delete("1.0", tk.END)

            with open(chat_file, "r") as f:
                chat_display.insert(tk.END, f.read())

            chat_display.config(state="disabled")
            chat_display.see(tk.END)

        def send_message():
            msg = entry.get().strip()
            if msg == "":
                return

            with open(chat_file, "a") as f:
                f.write(f"{username}: {msg}\n")

            entry.delete(0, tk.END)
            load_chat()

        tk.Button(chat_window, text="Send", command=send_message).pack(pady=5)

        def auto_refresh():
            if chat_window.winfo_exists():
                load_chat()
                chat_window.after(1000, auto_refresh)

        load_chat()
        auto_refresh()

    def refresh_chats():
        for widget in chat_list_frame.winfo_children():
            widget.destroy()

        mutual_matches = get_mutual_matches()

        if not mutual_matches:
            tk.Label(chat_list_frame, text="No mutual matches yet").pack()
        else:
            for user in mutual_matches:
                tk.Button(
                    chat_list_frame,
                    text=user,
                    width=25,
                    command=lambda u=user: open_chat(u)
                ).pack(pady=3)

        messages_frame.after(3000, refresh_chats)

    refresh_chats()

    return messages_frame