import tkinter as tk
import os
from tkinter import messagebox
from mainwindow import open_main_window

def verify(user1, pass1):
    try:
        with open("users.txt", "r") as file:
            for line in file:
                userpass = line.strip().split()
                username, password = userpass
                if username == user1 and password == pass1:
                    return True
        return False
    except FileNotFoundError:
        messagebox.showerror("Error", "User file not found.")
        return False


def login():
    username = user1.get()
    password = pass1.get()
    if verify(username, password):
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        window.withdraw()
        open_main_window(username)
        window.deiconify()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def create_account():
    create_window = tk.Toplevel(window)
    create_window.title("Create Account")
    create_window.geometry("300x150")
    tk.Label(create_window, text="New Username:").pack()
    new_user = tk.Entry(create_window)
    new_user.pack()
    tk.Label(create_window, text="New Password:").pack()
    new_pass = tk.Entry(create_window, show="*")
    new_pass.pack()

    def save_account():
        new_username = new_user.get()
        new_password = new_pass.get()

        if new_username == "" or new_password == "":
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
        if username_exists(new_username):
            messagebox.showerror("Error", "Username already exists.")
            return
        
        with open("users.txt", "a") as file:
            file.seek(0, 2)  # go to end of file
            file.write(new_username + " " + new_password + "\n")

        user_file_path = os.path.join("userInfo", f"{new_username}.txt")
        with open(user_file_path, "w") as f:
            f.write(f"{new_username}\n")
        messagebox.showinfo("Account Created", "Account for " + new_username + " has been created.")
        create_window.destroy()

    tk.Button(create_window, text="Create Account", command=save_account).pack(pady=10)


def username_exists(username):
    try:
        with open("users.txt", "r") as file:
            for line in file:
                userpass = line.strip().split()
                if userpass[0] == username:
                    return True
        return False
    except FileNotFoundError:
        return False

window = tk.Tk()
window.title("Login")
window.geometry("300x300")

title_label = tk.Label(window, text="Please Login")
title_label.pack(pady=10)

username_label = tk.Label(window, text="Username:")
username_label.pack()
user1 = tk.Entry(window)
user1.pack()

password_label = tk.Label(window, text="Password:")
password_label.pack()
pass1 = tk.Entry(window, show="*")
pass1.pack()

login_button = tk.Button(window, text="Login", command=login)
login_button.pack(pady=10)

create_button = tk.Button(window, text="Create Account", command=create_account)
create_button.pack()

window.mainloop()