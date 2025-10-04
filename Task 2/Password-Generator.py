import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    try:
        length = int(entry_length.get())
        if length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long.")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
        return

    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation
    all_characters = letters + digits + symbols

    password = [
        random.choice(letters),
        random.choice(digits),
        random.choice(symbols)
    ]

    if length > 3:
        password += random.choices(all_characters, k=length-3)

    random.shuffle(password)
    password_str = ''.join(password)

    result_label.config(text=password_str)

def copy_password():
    password = result_label.cget("text")
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

root = tk.Tk()
root.title("🔐--- Password --- Generator")
root.geometry("420x250")
root.configure(bg="#f0f4f7")
root.resizable(False, False)


title_label = tk.Label(root, text="Secure Password Generator", 
                       font=("Arial", 16, "bold"), fg="#333", bg="#f0f4f7")
title_label.pack(pady=15)


frame = tk.Frame(root, bg="#f0f4f7")
frame.pack(pady=10)

tk.Label(frame, text="Enter Password Length:", font=("Arial", 12), bg="#f0f4f7").grid(row=0, column=0, padx=5)
entry_length = tk.Entry(frame, font=("Arial", 12), width=10, justify="center")
entry_length.grid(row=0, column=1, padx=5)

btn_frame = tk.Frame(root, bg="#f0f4f7")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Generate", command=generate_password, font=("Arial", 12), bg="#4CAF50", fg="white", padx=15).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Copy", command=copy_password, font=("Arial", 12), bg="#2196F3", fg="white", padx=15).grid(row=0, column=1, padx=5)

result_label = tk.Label(root, text="", font=("Consolas", 14, "bold"), fg="#2E86C1", bg="#f0f4f7")
result_label.pack(pady=20)

root.mainloop()
