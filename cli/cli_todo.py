import argparse
import sqlite3
import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

DB_FILE = "tasks.db"
CONFIG_FILE = "config.json"


def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT NOT NULL DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()


def load_tasks_json():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_tasks_json(tasks):
    with open(DB_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def add_task(title, description=None, due_date=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, due_date, status) VALUES (?, ?, ?, ?)",
                   (title, description, due_date, 'pending'))
    conn.commit()
    conn.close()


def list_tasks(filter_status=None, filter_date=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = "SELECT * FROM tasks"
    conditions = []
    params = []

    if filter_status:
        conditions.append("status = ?")
        params.append(filter_status)

    if filter_date:
        conditions.append("due_date = ?")
        params.append(filter_date)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()

    return tasks


def update_task(task_id, title=None, description=None, due_date=None, status=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = "UPDATE tasks SET "
    updates = []
    params = []

    if title:
        updates.append("title = ?")
        params.append(title)
    if description:
        updates.append("description = ?")
        params.append(description)
    if due_date:
        updates.append("due_date = ?")
        params.append(due_date)
    if status:
        updates.append("status = ?")
        params.append(status)

    query += ", ".join(updates) + " WHERE id = ?"
    params.append(task_id)

    cursor.execute(query, params)
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def main():
    create_table()

    console = Console()

    parser = argparse.ArgumentParser(description="Manage your to-do list.")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task.")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("-d", "--description", help="Task description")
    add_parser.add_argument("-due", "--due_date", help="Due date (YYYY-MM-DD)")

    list_parser = subparsers.add_parser("list", help="List all tasks.")
    list_parser.add_argument("-s", "--status", help="Filter by status (pending/completed)")
    list_parser.add_argument("-due", "--due_date", help="Filter by due date (YYYY-MM-DD)")

    update_parser = subparsers.add_parser("update", help="Update an existing task.")
    update_parser.add_argument("task_id", type=int, help="ID of the task to update")
    update_parser.add_argument("-t", "--title", help="New title")
    update_parser.add_argument("-d", "--description", help="New description")
    update_parser.add_argument("-due", "--due_date", help="New due date (YYYY-MM-DD)")
    update_parser.add_argument("-s", "--status", help="New status (pending/completed)")

    delete_parser = subparsers.add_parser("delete", help="Delete a task.")
    delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title, args.description, args.due_date)
        console.print("[green]Task added![/green]")

    elif args.command == "list":
        tasks = list_tasks(args.status, args.due_date)
        table = Table(title="To-Do List")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Description")
        table.add_column("Due Date")
        table.add_column("Status")

        for i, task in enumerate(tasks):
            table.add_row(str(i + 1), task[1], task[2] or "", task[3] or "", task[4])  # Access by index

        console.print(table)

    elif args.command == "update":
        update_task(args.task_id, args.title, args.description, args.due_date, args.status)
        console.print("[green]Task updated![/green]")

    elif args.command == "delete":
        delete_task(args.task_id)
        console.print("[green]Task deleted![/green]")


if __name__ == "__main__":
    main()
