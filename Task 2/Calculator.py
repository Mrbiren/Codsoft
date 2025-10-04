import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


def press(key):
    entry_var.set(entry_var.get() + str(key))

def clear():
    entry_var.set("")

def calculate():
    try:
        ans = str(eval(entry_var.get()))
        entry_var.set(ans)
        # Flash effect
        entry.config(background="#004d40")
        root.after(200, lambda: entry.config(background="#1a1a2e"))
    except:
        messagebox.showerror("Error", "Invalid Input")

def backspace():
    entry_var.set(entry_var.get()[:-1])


root = tk.Tk()
root.title("Rounded Calculator")
root.geometry("380x500")
root.config(bg="#0f0f1f")
root.resizable(False, False)

entry_var = tk.StringVar()


entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 22),
                 bd=5, relief="flat", justify="right",
                 bg="#1a1a2e", fg="#00ffcc", insertbackground="white")
entry.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=20, pady=12, padx=12, sticky="nsew")


buttons = [
    ["Clear", "Backspace", "", ""], 
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "+", "="]
]


style = ttk.Style()
style.theme_use("clam")

style.configure("Rounded.TButton",
                font=("Arial", 18, "bold"),
                padding=10,
                foreground="white",
                background="#2d3436",
                borderwidth=0,
                relief="flat")

style.map("Rounded.TButton",
          background=[("active", "#00cc99")],
          foreground=[("active", "white")])


def create_button(parent, text, cmd, bg):
    btn = ttk.Button(parent, text=text, command=cmd, style="Rounded.TButton")
    btn.config(width=5)
    style.configure(f"{text}.TButton",
                    background=bg,
                    foreground="white",
                    font=("Arial", 18, "bold"),
                    padding=12)
    btn.config(style=f"{text}.TButton")
    return btn

for r in range(len(buttons)):
    for c in range(len(buttons[r])):
        text = buttons[r][c]
        if text == "":
            continue  
        if text == "=":
            btn = create_button(root, text, calculate, "#00b894")  
        elif text == "Backspace":
            btn = create_button(root, "🔙", backspace, "#e67e22") 
        elif text == "Clear":
            btn = create_button(root, text, clear, "#d63031")     
            btn.config(width=10)
        elif text in ["+", "-", "*", "/"]:
            btn = create_button(root, text, lambda t=text: press(t), "#0984e3")  
        else:
            btn = create_button(root, text, lambda t=text: press(t), "#2d3436")  

        btn.grid(row=r+1, column=c, padx=6, pady=6, sticky="nsew")


for i in range(len(buttons) + 1):
    root.grid_rowconfigure(i, weight=1)

for j in range(4):
    root.grid_columnconfigure(j, weight=1)

root.bind("<Return>", lambda e: calculate())
root.bind("<BackSpace>", lambda e: backspace())

root.mainloop()
