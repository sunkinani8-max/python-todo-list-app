
import json
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import date

# ---------------- CONFIGURATION ----------------
DATA_FILE = Path(__file__).with_name("tasks.json")

BG = "#111827"
PANEL = "#1F2937"
INPUT_BG = "#273449"
WHITE = "#F9FAFB"
MUTED = "#9CA3AF"
BLUE = "#6366F1"
GREEN = "#10B981"
RED = "#EF4444"
BORDER = "#374151"

PRIORITIES = ["High", "Medium", "Low"]

root = tk.Tk()
root.title("TaskFlow | To-Do List Pro")
root.geometry("850x720")
root.minsize(650, 600)
root.configure(bg=BG)

# ---------------- STORAGE ----------------
def load_tasks():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("The saved task data must be a list.")

        result = []
        for item in data:
            if not isinstance(item, dict) or not isinstance(item.get("task"), str):
                continue

            result.append({
                "task": item["task"],
                "completed": bool(item.get("completed", False)),
                "priority": item.get("priority", "Medium")
                    if item.get("priority") in PRIORITIES else "Medium",
                "due": item.get("due", "")
                    if isinstance(item.get("due", ""), str) else "",
            })

        return result

    except (OSError, json.JSONDecodeError, ValueError) as error:
        messagebox.showerror(
            "Loading error",
            f"Could not load tasks.json:\n{error}"
        )
        return []


tasks = load_tasks()
visible_indices = []


def save_tasks():
    try:
        temp_file = DATA_FILE.with_suffix(".tmp")
        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
        temp_file.replace(DATA_FILE)
        return True
    except OSError as error:
        messagebox.showerror("Save error", str(error))
        return False


# ---------------- HELPERS ----------------
def validate_due_date(value):
    if not value:
        return True

    try:
        date.fromisoformat(value)
        return len(value) == 10
    except ValueError:
        return False


def selected_task_index():
    selected = task_list.curselection()
    if not selected:
        messagebox.showinfo(
            "Select a task", "Select a task from the list first."
        )
        return None

    return visible_indices[selected[0]]


def refresh_tasks():
    global visible_indices

    task_list.delete(0, tk.END)
    visible_indices = []

    query = search_var.get().strip().casefold()

    for index, task in enumerate(tasks):
        if query and query not in task["task"].casefold():
            continue

        visible_indices.append(index)

        status = "✓ DONE" if task["completed"] else "○ TODO"
        due_text = f" | Due: {task['due']}" if task["due"] else ""
        line = (
            f"{status}   {task['task']}   "
            f"| {task['priority'].upper()}{due_text}"
        )

        task_list.insert(tk.END, line)

        if task["completed"]:
            task_list.itemconfig(index=len(visible_indices) - 1, fg=GREEN)
        elif task["priority"] == "High":
            task_list.itemconfig(index=len(visible_indices) - 1, fg="#FCA5A5")
        elif task["priority"] == "Medium":
            task_list.itemconfig(index=len(visible_indices) - 1, fg="#FCD34D")
        else:
            task_list.itemconfig(index=len(visible_indices) - 1, fg=WHITE)

    total = len(tasks)
    completed = sum(1 for task in tasks if task["completed"])
    percent = int(completed / total * 100) if total else 0

    progress_label.config(
        text=f"{completed} of {total} completed  •  {percent}%"
    )
    progress_bar["maximum"] = max(total, 1)
    progress_bar["value"] = completed


# ---------------- TASK ACTIONS ----------------
def add_task(event=None):
    name = task_entry.get().strip()
    priority = priority_var.get()
    due = due_entry.get().strip()

    if not name:
        messagebox.showwarning("Missing task", "Enter a task name.")
        return

    if not validate_due_date(due):
        messagebox.showwarning(
            "Invalid date",
            "Use a valid date in YYYY-MM-DD format, for example 2026-10-25."
        )
        return

    tasks.append({
        "task": name,
        "completed": False,
        "priority": priority,
        "due": due,
    })

    if save_tasks():
        task_entry.delete(0, tk.END)
        due_entry.delete(0, tk.END)
        search_var.set("")
        refresh_tasks()
        task_entry.focus_set()
    else:
        tasks.pop()


def complete_task():
    index = selected_task_index()
    if index is None:
        return

    tasks[index]["completed"] = not tasks[index]["completed"]
    if save_tasks():
        refresh_tasks()


def delete_task():
    index = selected_task_index()
    if index is None:
        return

    name = tasks[index]["task"]
    if messagebox.askyesno("Delete task", f"Delete '{name}'?"):
        removed = tasks.pop(index)
        if not save_tasks():
            tasks.insert(index, removed)
        refresh_tasks()


# ---------------- STYLING ----------------
style = ttk.Style(root)
style.theme_use("clam")
style.configure(
    "Dark.Horizontal.TProgressbar",
    troughcolor=INPUT_BG,
    background=GREEN,
    bordercolor=INPUT_BG,
    lightcolor=GREEN,
    darkcolor=GREEN,
)
style.configure(
    "Dark.TCombobox",
    fieldbackground=INPUT_BG,
    background=INPUT_BG,
    foreground=WHITE,
    arrowcolor=WHITE,
)
style.map(
    "Dark.TCombobox",
    fieldbackground=[("readonly", INPUT_BG)],
    foreground=[("readonly", WHITE)],
)

# ---------------- HEADER ----------------
header = tk.Frame(root, bg=PANEL, padx=28, pady=22)
header.pack(fill="x")

tk.Label(
    header,
    text="TASKFLOW",
    font=("Segoe UI", 24, "bold"),
    bg=PANEL,
    fg=WHITE,
).pack(anchor="w")

tk.Label(
    header,
    text="Organize your day. Focus on what matters.",
    font=("Segoe UI", 11),
    bg=PANEL,
    fg=MUTED,
).pack(anchor="w", pady=(4, 0))

# ---------------- MAIN CONTENT ----------------
content = tk.Frame(root, bg=BG, padx=28, pady=22)
content.pack(fill="both", expand=True)

tk.Label(
    content,
    text="ADD A TASK",
    font=("Segoe UI", 10, "bold"),
    bg=BG,
    fg=MUTED,
).pack(anchor="w", pady=(0, 8))

task_entry = tk.Entry(
    content,
    font=("Segoe UI", 12),
    bg=INPUT_BG,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
)
task_entry.pack(fill="x", ipady=10, pady=(0, 12))

options = tk.Frame(content, bg=BG)
options.pack(fill="x", pady=(0, 14))

tk.Label(
    options, text="Priority", bg=BG, fg=MUTED,
    font=("Segoe UI", 10)
).pack(side="left", padx=(0, 8))

priority_var = tk.StringVar(value="Medium")
priority_box = ttk.Combobox(
    options,
    textvariable=priority_var,
    values=PRIORITIES,
    state="readonly",
    width=10,
    style="Dark.TCombobox",
)
priority_box.pack(side="left", ipady=4)

tk.Label(
    options, text="Due date", bg=BG, fg=MUTED,
    font=("Segoe UI", 10)
).pack(side="left", padx=(18, 8))

due_entry = tk.Entry(
    options,
    font=("Segoe UI", 10),
    bg=INPUT_BG,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    width=15,
)
due_entry.pack(side="left", ipady=7)
due_entry.insert(0, "")

tk.Label(
    options, text="YYYY-MM-DD (optional)",
    bg=BG, fg=MUTED, font=("Segoe UI", 8)
).pack(side="left", padx=(8, 0))

def make_button(parent, text, command, color):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padx=14,
        pady=10,
        cursor="hand2",
    )


make_button(content, "+  Add Task", add_task, BLUE).pack(
    fill="x", pady=(0, 20)
)
root.bind("<Control-Return>", add_task)

# ---------------- PROGRESS ----------------
progress_panel = tk.Frame(content, bg=PANEL, padx=16, pady=13)
progress_panel.pack(fill="x", pady=(0, 18))

progress_label = tk.Label(
    progress_panel,
    text="0 of 0 completed  •  0%",
    bg=PANEL,
    fg=WHITE,
    font=("Segoe UI", 11, "bold"),
)
progress_label.pack(anchor="w", pady=(0, 8))

progress_bar = ttk.Progressbar(
    progress_panel,
    style="Dark.Horizontal.TProgressbar",
    mode="determinate",
    maximum=1,
)
progress_bar.pack(fill="x")

# ---------------- SEARCH AND LIST ----------------
list_heading = tk.Frame(content, bg=BG)
list_heading.pack(fill="x", pady=(0, 8))

tk.Label(
    list_heading,
    text="YOUR TASKS",
    font=("Segoe UI", 10, "bold"),
    bg=BG,
    fg=MUTED,
).pack(side="left")

search_var = tk.StringVar()
search_entry = tk.Entry(
    list_heading,
    textvariable=search_var,
    font=("Segoe UI", 10),
    bg=INPUT_BG,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    width=24,
)
search_entry.pack(side="right", ipady=6)
search_entry.insert(0, "")

task_frame = tk.Frame(content, bg=PANEL)
task_frame.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(task_frame)
scrollbar.pack(side="right", fill="y")

task_list = tk.Listbox(
    task_frame,
    font=("Segoe UI", 11),
    bg=PANEL,
    fg=WHITE,
    selectbackground=BLUE,
    selectforeground=WHITE,
    activestyle="none",
    relief="flat",
    bd=0,
    highlightthickness=0,
    yscrollcommand=scrollbar.set,
    selectmode=tk.SINGLE,
)
task_list.pack(side="left", fill="both", expand=True, padx=12, pady=12)
scrollbar.config(command=task_list.yview)

search_var.trace_add("write", lambda *_: refresh_tasks())

# ---------------- ACTION BUTTONS ----------------
actions = tk.Frame(content, bg=BG)
actions.pack(fill="x", pady=(14, 0))

make_button(
    actions, "✓  Complete / Undo", complete_task, GREEN
).pack(side="left")

make_button(
    actions, "Delete Task", delete_task, RED
).pack(side="right")

# ---------------- START ----------------
refresh_tasks()
task_entry.focus_set()
root.mainloop()
