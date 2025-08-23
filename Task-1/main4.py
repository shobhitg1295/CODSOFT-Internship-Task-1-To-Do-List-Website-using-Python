import sqlite3
import tkinter as tk
from tkinter import messagebox

# ========== Database Setup ==========
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (title TEXT)")
conn.commit()

# ========== Functions ==========

def load_tasks():
    tasks.clear()
    cursor.execute("SELECT title FROM tasks")
    for row in cursor.fetchall():
        tasks.append(row[0])
    update_listbox()

def update_listbox():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)

def add_task():
    task = task_entry.get().strip()
    if not task:
        messagebox.showwarning("Input Error", "Please enter a task.")
        return
    tasks.append(task)
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (task,))
    conn.commit()
    update_listbox()
    task_entry.delete(0, tk.END)

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

def delete_all_tasks():
    if messagebox.askyesno("Delete All", "Are you sure you want to delete all tasks?"):
        tasks.clear()
        cursor.execute("DELETE FROM tasks")
        conn.commit()
        update_listbox()

def on_exit():
    conn.commit()
    cursor.close()
    conn.close()
    root.destroy()

# ========== UI Design ==========

root = tk.Tk()
root.title("📝 To-Do List")
root.geometry("600x500")
root.resizable(False, False)
root.configure(bg="#87CEEB")  # Sky blue background

tasks = []

# ---------- Styling ----------
main_font = ("Segoe UI", 12)
title_font = ("Segoe UI", 18, "bold")
button_font = ("Segoe UI", 11, "bold")

entry_bg = "#ffffff"
button_bg = "#4CAF50"
button_fg = "#ffffff"
button_hover = "#45a049"
danger_button_bg = "#e74c3c"

# ---------- Frames ----------
main_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, bd=2, relief=tk.RIDGE)
main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

title_label = tk.Label(main_frame, text="📝 TO-DO LIST", font=title_font, bg="#ffffff", fg="#333333")
title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

# Task Entry
task_entry = tk.Entry(main_frame, font=main_font, width=40, bd=2, bg=entry_bg, relief=tk.GROOVE)
task_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="w")

add_btn = tk.Button(main_frame, text="Add Task", font=button_font, bg=button_bg, fg=button_fg,
                    width=12, command=add_task)
add_btn.grid(row=1, column=2, padx=5)

# Task Listbox
task_listbox = tk.Listbox(main_frame, font=main_font, width=55, height=10, bd=2, relief=tk.GROOVE,
                          selectbackground="#ffa500", activestyle="none")
task_listbox.grid(row=2, column=0, columnspan=3, pady=10)

# Buttons
button_frame = tk.Frame(main_frame, bg="#ffffff")
button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))

remove_btn = tk.Button(button_frame, text="Remove Task", font=button_font, bg="#f39c12", fg="#ffffff",
                       width=15, command=delete_task)
remove_btn.grid(row=0, column=0, padx=5)

delete_all_btn = tk.Button(button_frame, text="Delete All", font=button_font, bg=danger_button_bg, fg="#ffffff",
                           width=15, command=delete_all_tasks)
delete_all_btn.grid(row=0, column=1, padx=5)

exit_btn = tk.Button(button_frame, text="Exit", font=button_font, bg="#34495e", fg="#ffffff",
                     width=15, command=on_exit)
exit_btn.grid(row=0, column=2, padx=5)

# ---------- Hover Effects ----------
def on_enter(e, btn, color): btn.config(bg=color)
def on_leave(e, btn, color): btn.config(bg=color)

for btn, normal, hover in [
    (add_btn, button_bg, button_hover),
    (remove_btn, "#f39c12", "#e67e22"),
    (delete_all_btn, danger_button_bg, "#c0392b"),
    (exit_btn, "#34495e", "#2c3e50")
]:
    btn.bind("<Enter>", lambda e, b=btn, h=hover: on_enter(e, b, h))
    btn.bind("<Leave>", lambda e, b=btn, n=normal: on_leave(e, b, n))

# ========== Run ==========
load_tasks()
root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()
