# Python To-Do List App

A simple desktop To-Do List application built using Python and Tkinter. It helps users organize daily tasks through a graphical user interface.

## Features

- Add new tasks
- Mark tasks as completed and undo completion
- Delete tasks with confirmation
- Search tasks by name
- Set task priority: High, Medium, or Low
- Add optional due dates
- Track progress with a progress bar and completion counter
- Save tasks automatically in a JSON file
- Load saved tasks when the application starts
- Dark-themed user interface

## Technologies Used

- Python
- Tkinter — graphical user interface
- JSON — task data storage
- VS Code — development environment

## Project Structure

```text
Todo_List_Project/
├── todo_gui.py
├── main.py
├── tasks.json
└── README.md
```

- `todo_gui.py` — main graphical application
- `main.py` — original terminal-based version
- `tasks.json` — stores saved tasks
- `README.md` — project documentation

## Requirements

- Python 3
- Tkinter (usually included with standard Python installations)

## How to Run

1. Download or clone the project.
2. Open the project folder in VS Code.
3. Open the terminal in VS Code.
4. Run the following command:

```bash
python todo_gui.py
```

If your system uses the Python launcher, try:

```bash
py todo_gui.py
```

## Data Storage

Tasks are saved in `tasks.json`, allowing them to remain available when the application is closed and reopened.

## Learning Outcomes

This project helped me practice:

- Python programming
- GUI development with Tkinter
- Functions and event handling
- Reading and writing JSON files
- Input validation and error handling
- Building and testing a desktop application

## Future Improvements

- Add task editing
- Add task categories
- Add reminders and notifications
- Add sorting and filtering options
- Improve the user interface

## Author

**Charan**

Built as a Python learning project.