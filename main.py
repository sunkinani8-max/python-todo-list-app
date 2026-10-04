
import json
from pathlib import Path

FILE = Path("tasks.json")


def load_tasks():
    if FILE.exists():
        try:
            with FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            print("Could not read saved tasks. Starting with an empty list.")
    return []


tasks = load_tasks()


def save_tasks():
    with FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)


def add_task():
    task = input("Enter your task: ").strip()

    if not task:
        print("Task cannot be empty.")
        return

    tasks.append({"task": task, "completed": False})
    save_tasks()
    print("Task added and saved!")


def view_tasks():
    if not tasks:
        print("No tasks available.")
        return

    print("\n--- YOUR TASKS ---")
    for i, task in enumerate(tasks, start=1):
        status = "Completed" if task["completed"] else "Pending"
        print(f"{i}. {task['task']} - {status}")


def complete_task():
    view_tasks()
    if not tasks:
        return

    try:
        number = int(input("Enter task number to complete: "))
        if 1 <= number <= len(tasks):
            tasks[number - 1]["completed"] = True
            save_tasks()
            print("Task completed and saved!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def delete_task():
    view_tasks()
    if not tasks:
        return

    try:
        number = int(input("Enter task number to delete: "))
        if 1 <= number <= len(tasks):
            removed = tasks.pop(number - 1)
            save_tasks()
            print(f"Deleted: {removed['task']}")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


while True:
    print("\n===== MY TO-DO LIST =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        complete_task()
    elif choice == "4":
        delete_task()
    elif choice == "5":
        print("Thank you for using My To-Do List!")
        break
    else:
        print("Invalid choice. Please try again.")
