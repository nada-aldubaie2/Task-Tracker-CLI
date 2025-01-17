import json
import os
from pathlib import Path
import sys
from datetime import date, datetime


TASKS_FILE = "tasks.json"

def load_tasks():
    if Path(TASKS_FILE).exists():
        with open(TASKS_FILE, 'r', encoding='utf-8')as file:
          # data = list(json.load(file))
          # print(data)
          # try:
          #    data = json.load(file)
          #    if isinstance(data, list):
          #      return data
          # except json.JSONDecodeError:
            #  return []

            return json.load(file)
    return []


def save_tasks(task):
    with open(TASKS_FILE, 'w', encoding='utf-8') as file:
        json.dump(task, file, indent=8)

# -----------------------------------------------------------
# ============ C R U D Functions=======================
# -----------------------------------------------------------


def add_task(description, status):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    new_task = {
        "id": task_id,
        "description": description,
        "status": status,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"The new task {task_id} has added successfully")


def update_task(task_id, new_description, new_status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["status"] = new_status
            task["updated_at"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"The task {task_id} has updated successfully")
            return
        print(f"Task with ID {task_id} not found.")


def delete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"The task {task_id} has deleted successfully")
            return
    print(f"Task with ID {task_id} not found.")
# -----------------------------------------------------------


def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        # new_list = [expression for item in iterable if condition] | called=<List Comprehension> =>2 create new list depend on condition
        tasks = [task for task in tasks if task["status"] == status]
    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {
              task['status']}, Created: {task['created_at']}, Updated: {task['updated_at']}", sep=" |  ")
        

def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}.")
            return
    print(f"Task with ID {task_id} not found.")


def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        print("Available commands:")
        print("  add <description><status>      - Add a new task")
        print("  update <task_id> <new_description><status>      - update a task")
        print("  delete <task_id>       - Delete a task")
        print("  list [status]          - List tasks (optional: done, not-done, in-progress)")
        return

    command = sys.argv[1]
    if command == "add":
        if len(sys.argv) < 4:
            print("Usage: task-cli add <description> <status>")
            return
        description = sys.argv[2]
        status = sys.argv[3]
        add_task(description, status)

    elif command == "update":
        if len(sys.argv) < 5:
            print("Usage: task-cli update <task_id> <new_description>")
            return
        task_id = int(sys.argv[2])
        new_description = sys.argv[3]
        status = sys.argv[4]
        update_task(task_id, new_description, status)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: task-cli delete <task_id>")
            return
        task_id = int(sys.argv[2])
        delete_task(task_id)

    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-in-progress <task_id>")
            return
        task_id = int(sys.argv[2])
        mark_task(task_id, "in-progress")

    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-done <task_id>")
            return
        task_id = int(sys.argv[2])
        mark_task(task_id, "done")
        
    elif command == "mark-not-done":
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-not-done <task_id>")
            return
        task_id = int(sys.argv[2])
        mark_task(task_id, "not-done")

    elif command == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status)

    else:
        print("Invalid command.")


if __name__ == "__main__":
    main()
