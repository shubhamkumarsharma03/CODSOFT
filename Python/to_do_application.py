import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
import json
import os

TASK_FILE = "tasks.json"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serene To-Do List")
        self.root.geometry("800x600")
        self.root.configure(bg="#e6f2ff")  # Light calm blue
        self.dark_mode = False
        self.tasks = []

        self.create_widgets()
        self.load_tasks()
        self.refresh_tasks()

    def create_widgets(self):
        self.style = ttk.Style(self.root)
        self.style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#a3c2c2", foreground="black")
        self.style.configure("Treeview", font=('Arial', 10), rowheight=25)

        self.main_frame = tk.Frame(self.root, bg="#e6f2ff")
        self.main_frame.pack(padx=20, pady=20)

        tk.Label(self.main_frame, text="Task:", bg="#e6f2ff", font=('Arial', 12)).grid(row=0, column=0, sticky="e")
        self.task_entry = tk.Entry(self.main_frame, width=40, font=('Arial', 11))
        self.task_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.main_frame, text="Due Date:", bg="#e6f2ff", font=('Arial', 12)).grid(row=1, column=0, sticky="e")
        self.due_entry = DateEntry(self.main_frame, date_pattern='yyyy-mm-dd', font=('Arial', 11))
        self.due_entry.grid(row=1, column=1)

        tk.Label(self.main_frame, text="Priority:", bg="#e6f2ff", font=('Arial', 12)).grid(row=2, column=0, sticky="e")
        self.priority_combo = ttk.Combobox(self.main_frame, values=["Low", "Medium", "High"], font=('Arial', 11))
        self.priority_combo.set("Medium")
        self.priority_combo.grid(row=2, column=1)

        tk.Button(self.main_frame, text="Add Task", command=self.add_task, font=('Arial', 11), bg="#99ccff").grid(row=3, column=0, columnspan=2, pady=10)

        tk.Label(self.main_frame, text="Search:", bg="#e6f2ff", font=('Arial', 12)).grid(row=4, column=0, sticky="e")
        self.search_entry = tk.Entry(self.main_frame, font=('Arial', 11))
        self.search_entry.grid(row=4, column=1)
        self.search_entry.bind("<KeyRelease>", self.filter_tasks)

        self.tree = ttk.Treeview(self.root, columns=("Task", "Due", "Priority", "Status"), show="headings", selectmode="browse")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor='center')
        self.tree.pack(pady=10, padx=10, fill="x")

        btn_frame = tk.Frame(self.root, bg="#e6f2ff")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Delete", command=self.delete_task, font=('Arial', 11), bg="#ff9999").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Mark Done", command=self.mark_done, font=('Arial', 11), bg="#b3ffb3").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Edit", command=self.edit_task, font=('Arial', 11), bg="#ffffb3").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Dark Mode", command=self.toggle_dark_mode, font=('Arial', 11), bg="#ccccff").grid(row=0, column=3, padx=5)

    def add_task(self):
        task = self.task_entry.get().strip()
        due = self.due_entry.get()
        priority = self.priority_combo.get()
        if not task:
            messagebox.showerror("Error", "Task cannot be empty")
            return
        task_data = {"task": task, "due": due, "priority": priority, "status": "Pending"}
        self.tasks.append(task_data)
        self.save_tasks()
        self.refresh_tasks()
        self.clear_inputs()

    def refresh_tasks(self, tasks=None):
        self.tree.delete(*self.tree.get_children())
        data = tasks if tasks is not None else self.tasks
        for task in data:
            self.tree.insert("", "end", values=(task["task"], task["due"], task["priority"], task["status"]))

    def delete_task(self):
        selected = self.tree.selection()
        if not selected: return
        index = self.tree.index(selected)
        del self.tasks[index]
        self.save_tasks()
        self.refresh_tasks()

    def mark_done(self):
        selected = self.tree.selection()
        if not selected: return
        index = self.tree.index(selected)
        self.tasks[index]['status'] = "Completed"
        self.save_tasks()
        self.refresh_tasks()

    def edit_task(self):
        selected = self.tree.selection()
        if not selected: return
        index = self.tree.index(selected)
        task = self.tasks[index]
        new_task = simpledialog.askstring("Edit Task", "Update task:", initialvalue=task["task"])
        if new_task:
            task["task"] = new_task
            self.save_tasks()
            self.refresh_tasks()

    def filter_tasks(self, event=None):
        keyword = self.search_entry.get().lower()
        filtered = [task for task in self.tasks if keyword in task["task"].lower()]
        self.refresh_tasks(filtered)

    def clear_inputs(self):
        self.task_entry.delete(0, tk.END)
        self.priority_combo.set("Medium")
        self.due_entry.set_date("")

    def load_tasks(self):
        if os.path.exists(TASK_FILE):
            with open(TASK_FILE, "r") as f:
                self.tasks = json.load(f)

    def save_tasks(self):
        with open(TASK_FILE, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg = "#2b2b2b" if self.dark_mode else "#e6f2ff"
        fg = "white" if self.dark_mode else "black"
        self.root.configure(bg=bg)
        self.main_frame.configure(bg=bg)
        for widget in self.main_frame.winfo_children():
            try:
                widget.configure(bg=bg, fg=fg)
            except:
                pass
        for child in self.root.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=bg)


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
