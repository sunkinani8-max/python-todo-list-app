
import json
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# ---------- SETTINGS ----------
DATA_FILE = Path(__file__).with_name("tasks.json")

BG = "#F3F6FB"
WHITE = "#FFFFFF"
NAVY = "#18243A"
BLUE = "#4169E1"
GREEN = "#16A085"
RED = "#E25555"
GRAY = "#738096"


# ---------- TASK STORAGE ----------
def load_tasks():
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, OSError):
            messagebox.showwarning(
                "Storage warning",
                "Saved tasks could not be loaded. Starting with an empty list."
            )
    return []


tasks = load_tasks()


def save_tasks():
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except OSError as error:
        messagebox.showerror("Save error", str(error))


# ---------- TASK FUNCTIONS ----------
def refresh_tasks():
    task_list.delete(0, tk.END)

    for task in tasks:
        if task["completed"]:
            text = f"✓  {task['task']}  — Completed"
        else:
            text = f"○  {task['task']}  — Pending"

        task_list.insert(tk.END, text)

    completed = sum(task["completed"] for task in tasks)
    total_label.config(
        text=f"{completed} of {len(tasks)} tasks completed"
    )


def add_task():
    task_text = task_entry.get().strip()

    if not task_text:
        messagebox.showwarning(
            "Missing task", "Please enter a task first."
        )
        return

    tasks.append({"task": task_text, "completed": False})
    save_tasks()
    refresh_tasks()

    task_entry.delete(0, tk.END)
    task_entry.focus_set()


def complete_task():
    selection = task_list.curselection()

    if not selection:
        messagebox.showinfo(
            "Select a task", "Select a task from the list first."
        )
        return

    index = selection[0]
    tasks[index]["completed"] = not tasks[index]["completed"]

    save_tasks()
    refresh_tasks()


def delete_task():
    selection = task_list.curselection()

    if not selection:
        messagebox.showinfo(
            "Select a task", "Select a task to delete."
        )
        return

    index = selection[0]
    task_name = tasks[index]["task"]

    confirm = messagebox.askyesno(
        "Delete task",
        f"Do you want to delete '{task_name}'?"
    )

    if confirm:
        tasks.pop(index)
        save_tasks()
        refresh_tasks()


# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("My To-Do List")
root.geometry("650x600")
root.minsize(500, 480)
root.configure(bg=BG)

# Header
header = tk.Frame(root, bg=NAVY, padx=28, pady=24)
header.pack(fill="x")

tk.Label(
    header,
    text="MY TO-DO LIST",
    font=("Segoe UI", 23, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(anchor="w")

tk.Label(
    header,
    text="Plan your day. Get things done.",
    font=("Segoe UI", 11),
    bg=NAVY,
    fg="#CBD5E8"
).pack(anchor="w", pady=(5, 0))

# Main content
content = tk.Frame(root, bg=BG, padx=28, pady=24)
content.pack(fill="both", expand=True)

tk.Label(
    content,
    text="Add a new task",
    font=("Segoe UI", 12, "bold"),
    bg=BG,
    fg=NAVY
).pack(anchor="w", pady=(0, 8))

entry_row = tk.Frame(content, bg=BG)
entry_row.pack(fill="x", pady=(0, 20))

task_entry = tk.Entry(
    entry_row,
    font=("Segoe UI", 12),
    relief="solid",
    bd=1
)
task_entry.pack(side="left", fill="x", expand=True, ipady=10)
task_entry.bind("<Return>", lambda event: add_task())

tk.Button(
    entry_row,
    text=" + Add ",
    command=add_task,
    bg=BLUE,
    fg=WHITE,
    activebackground="#3154BD",
    activeforeground=WHITE,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=14,
    pady=9,
    cursor="hand2"
).pack(side="left", padx=(10, 0))

# Task list heading
tk.Label(
    content,
    text="YOUR TASKS",
    font=("Segoe UI", 11, "bold"),
    bg=BG,
    fg=NAVY
).pack(anchor="w", pady=(0, 8))

# List and scrollbar
list_frame = tk.Frame(content, bg=WHITE)
list_frame.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

task_list = tk.Listbox(
    list_frame,
    font=("Segoe UI", 11),
    bg=WHITE,
    fg=NAVY,
    selectbackground=BLUE,
    selectforeground=WHITE,
    activestyle="none",
    relief="flat",
    bd=0,
    highlightthickness=0,
    yscrollcommand=scrollbar.set
)
task_list.pack(side="left", fill="both", expand=True, padx=10, pady=10)
scrollbar.config(command=task_list.yview)

# Action buttons
button_row = tk.Frame(content, bg=BG)
button_row.pack(fill="x", pady=(16, 8))

tk.Button(
    button_row,
    text="✓  Complete / Undo",
    command=complete_task,
    bg=GREEN,
    fg=WHITE,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=12,
    pady=10,
    cursor="hand2"
).pack(side="left")

tk.Button(
    button_row,
    text="Delete Task",
    command=delete_task,
    bg=RED,
    fg=WHITE,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=12,
    pady=10,
    cursor="hand2"
).pack(side="right")

total_label = tk.Label(
    content,
    text="0 of 0 tasks completed",
    font=("Segoe UI", 10),
    bg=BG,
    fg=GRAY
)
total_label.pack(anchor="w", pady=(8, 0))

# Load existing tasks and start the app
refresh_tasks()
task_entry.focus_set()
root.mainloop()
