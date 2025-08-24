import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database setup
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (title TEXT)")
conn.commit()

tasks = []

# Load tasks from database
def load_tasks():
    tasks.clear()
    cursor.execute("SELECT title FROM tasks")
    for row in cursor.fetchall():
        tasks.append(row[0])
    update_listbox()

# Update listbox display
def update_listbox():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)

# Add a task
def add_task():
    task = task_entry.get().strip()
    if not task:
        messagebox.showwarning("Input Error", "Please enter a task.")
        return
    tasks.append(task)
    cursor.execute("INSERT INTO tasks VALUES (?)", (task,))
    conn.commit()
    update_listbox()
    task_entry.delete(0, tk.END)

# Delete selected task
def delete_task():
    try:
        index = task_listbox.curselection()[0]
        task = task_listbox.get(index)
        tasks.remove(task)
        cursor.execute("DELETE FROM tasks WHERE title = ?", (task,))
        conn.commit()
        update_listbox()
    except IndexError:
        messagebox.showwarning("Selection Error", "No task selected.")

# Delete all tasks
def delete_all_tasks():
    if messagebox.askyesno("Delete All", "Are you sure you want to delete all tasks?"):
        tasks.clear()
        cursor.execute("DELETE FROM tasks")
        conn.commit()
        update_listbox()

# Exit app safely
def on_exit():
    conn.commit()
    cursor.close()
    conn.close()
    root.destroy()

# UI setup
root = tk.Tk()
root.title("📝 To-Do List")
root.geometry("500x400")
root.configure(bg="lightblue")

# Title label
tk.Label(root, text="📝 TO-DO LIST", font=("Segoe UI", 16, "bold"), bg="lightblue").pack(pady=10)

# Task entry box
task_entry = tk.Entry(root, font=("Segoe UI", 12), width=30)
task_entry.pack(pady=5)

# Buttons
tk.Button(root, text="Add Task", command=add_task, width=12, bg="green", fg="white").pack(pady=2)
tk.Button(root, text="Remove Task", command=delete_task, width=12, bg="orange", fg="white").pack(pady=2)
tk.Button(root, text="Delete All", command=delete_all_tasks, width=12, bg="red", fg="white").pack(pady=2)
tk.Button(root, text="Exit", command=on_exit, width=12, bg="gray", fg="white").pack(pady=2)

# Task listbox
task_listbox = tk.Listbox(root, font=("Segoe UI", 12), width=40, height=10)
task_listbox.pack(pady=10)

# Run the app
load_tasks()
root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()
