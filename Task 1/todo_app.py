import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json, os

FILE = "tasks.json"
DATE_FORMAT = "%d-%m-%y %I:%M %p"
BG = "#645E00"
FG = "#EEEEEE"
BTN_BG = "#27282C"
BTN_FG = "#FFFFFF"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List with Reminder")
        self.root.geometry("700x500")
        self.root.configure(bg=BG)

        self.tasks = []
        self.popups = {}
        self.load_tasks()
        self.create_widgets()
        self.update_clock()

    def create_widgets(self):
        tk.Label(self.root, text="To-Do List", font=("Segoe UI", 20, "bold"), bg=BG, fg=FG).pack(pady=10)

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(pady=10)

        tk.Label(frame, text="Task:", bg=BG, fg=FG).grid(row=0, column=0)
        self.task_entry = tk.Entry(frame, width=25)
        self.task_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Date (DD-MM-YY):", bg=BG, fg=FG).grid(row=0, column=2)
        self.date_entry = tk.Entry(frame, width=10)
        self.date_entry.grid(row=0, column=3, padx=5)

        tk.Label(frame, text="Time (HH:MM):", bg=BG, fg=FG).grid(row=0, column=4)
        self.time_entry = tk.Entry(frame, width=8)
        self.time_entry.grid(row=0, column=5, padx=5)

        tk.Label(frame, text="AM/PM:", bg=BG, fg=FG).grid(row=0, column=6)
        self.ampm_entry = tk.Entry(frame, width=5)
        self.ampm_entry.grid(row=0, column=7, padx=5)

        tk.Button(frame, text="Add Task", bg=BTN_BG, fg=BTN_FG, command=self.add_task).grid(row=0, column=8, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("Title", "DateTime", "Status"), show="headings", height=12)
        self.tree.pack(pady=20, fill="x")
        for col in ("Title", "DateTime", "Status"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Mark Done", bg=BTN_BG, fg=BTN_FG, command=self.mark_done_selected).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Task", bg=BTN_BG, fg=BTN_FG, command=self.update_task).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", bg=BTN_BG, fg=BTN_FG, command=self.delete_task).grid(row=0, column=2, padx=5)

    def load_tasks(self):
        if os.path.exists(FILE):
            with open(FILE, "r") as f:
                self.tasks = json.load(f)

    def save_tasks(self):
        with open(FILE, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self):
        title = self.task_entry.get().strip()
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        ampm = self.ampm_entry.get().strip().upper()

        if not title or not date or not time or ampm not in ("AM", "PM"):
            messagebox.showerror("Error", "Enter valid task details!")
            return

        dt_str = f"{date} {time} {ampm}"
        try:
            datetime.strptime(dt_str, DATE_FORMAT)
        except:
            messagebox.showerror("Error", "Invalid date/time format!")
            return

        task = {
            "id": str(datetime.now().timestamp()),
            "title": title,
            "dt_str": dt_str,
            "completed": False
        }
        self.tasks.append(task)
        self.save_tasks()
        self.refresh_list()
        self.clear_entries()

    def clear_entries(self):
        self.task_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.ampm_entry.delete(0, tk.END)

    def refresh_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for task in self.tasks:
            status = "Done" if task.get("completed") else "Pending"
            self.tree.insert("", tk.END, iid=task["id"], values=(task["title"], task["dt_str"], status))

    def mark_done(self, task, popup=None):
        task["completed"] = True
        self.save_tasks()
        self.refresh_list()
        if popup:
            popup.destroy()
        if task["id"] in self.popups:
            del self.popups[task["id"]]

    def mark_done_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Select a task to mark as done.")
            return
        tid = sel[0]
        for task in self.tasks:
            if task["id"] == tid:
                self.mark_done(task)
                break

    def delete_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Delete", "Select a task to delete.")
            return
        tid = sel[0]
        self.tasks = [t for t in self.tasks if t["id"] != tid]
        self.save_tasks()
        self.refresh_list()

    def update_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Update", "Select a task to update.")
            return

        tid = sel[0]
        task = next((x for x in self.tasks if x["id"] == tid), None)
        if not task: return

        popup = tk.Toplevel(self.root)
        popup.title("Update Task")
        popup.geometry("300x220")
        popup.configure(bg=BG)
        popup.attributes("-topmost", True)
        popup.lift()
        popup.focus_force()

        tk.Label(popup, text="Edit Task Details", bg=BG, fg=FG, font=("Segoe UI", 12, "bold")).pack(pady=10)
        tk.Label(popup, text="Title:", bg=BG, fg=FG).pack()
        title_entry = tk.Entry(popup, width=30)
        title_entry.insert(0, task["title"])
        title_entry.pack(pady=3)

        tk.Label(popup, text="Date (DD-MM-YY):", bg=BG, fg=FG).pack()
        date_entry = tk.Entry(popup, width=15)
        date_entry.insert(0, task["dt_str"].split()[0])
        date_entry.pack(pady=3)

        tk.Label(popup, text="Time (HH:MM):", bg=BG, fg=FG).pack()
        time_entry = tk.Entry(popup, width=10)
        time_entry.insert(0, task["dt_str"].split()[1])
        time_entry.pack(pady=3)

        tk.Label(popup, text="AM/PM:", bg=BG, fg=FG).pack()
        ampm_entry = tk.Entry(popup, width=5)
        ampm_entry.insert(0, task["dt_str"].split()[2])
        ampm_entry.pack(pady=3)

        def save_update():
            new_title = title_entry.get().strip()
            new_date = date_entry.get().strip()
            new_time = time_entry.get().strip()
            new_ampm = ampm_entry.get().strip().upper()
            dt_str = f"{new_date} {new_time} {new_ampm}"

            try:
                datetime.strptime(dt_str, DATE_FORMAT)
            except:
                messagebox.showerror("Error", "Invalid date/time format!")
                return

            task["title"] = new_title
            task["dt_str"] = dt_str
            task["completed"] = False  
            self.save_tasks()
            self.refresh_list()
            popup.destroy()

        tk.Button(popup, text="Save", bg=BTN_BG, fg=BTN_FG, command=save_update).pack(pady=10)

    def show_popup(self, task):
        if task["id"] in self.popups and self.popups[task["id"]].winfo_exists():
            self.popups[task["id"]].lift()
            self.popups[task["id"]].focus_force()
            return

        popup = tk.Toplevel(self.root)
        popup.title("Reminder")
        popup.geometry("300x150")
        popup.attributes("-topmost", True)
        popup.lift()
        popup.focus_force()
        self.popups[task["id"]] = popup

        tk.Label(popup, text=f"Reminder:\n{task['title']}", font=("Segoe UI", 12, "bold")).pack(pady=10)
        tk.Label(popup, text=f"Scheduled: {task['dt_str']}").pack()
        tk.Button(popup, text="Mark Complete", bg=BTN_BG, fg=BTN_FG,
                  command=lambda: self.mark_done(task, popup)).pack(pady=5)

    def update_clock(self):
        now = datetime.now()
        for task in self.tasks:
            if not task.get("completed"):
                dt = datetime.strptime(task["dt_str"], DATE_FORMAT)
                if now >= dt:
                    self.show_popup(task)
        self.root.after(5000, self.update_clock)

root = tk.Tk()
app = ToDoApp(root)
root.mainloop()