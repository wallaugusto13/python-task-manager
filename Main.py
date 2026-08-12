import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("tasks.json")


def load_tasks():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

    except (json.JSONDecodeError, OSError):
        print("Could not load saved tasks.")

    return []


def save_tasks():
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)

    except OSError:
        print("Could not save tasks.")


tasks = load_tasks()


def show_tasks():
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n========== TASKS ==========")

    for index, task in enumerate(tasks, start=1):
        status = "✓" if task.get("completed", False) else " "

        priority = task.get("priority", "Medium")
        due_date = task.get("due_date", "No date")

        print(
            f"{index}. [{status}] {task['name']} "
            f"| Priority: {priority} "
            f"| Due: {due_date}"
        )


def choose_priority():
    print("\nChoose the priority:")
    print("1 - Low")
    print("2 - Medium")
    print("3 - High")

    option = input("Priority: ").strip()

    priorities = {
        "1": "Low",
        "2": "Medium",
        "3": "High"
    }

    return priorities.get(option, "Medium")


def get_due_date():
    while True:
        due_date = input(
            "Due date (DD/MM/YYYY) or press Enter for no date: "
        ).strip()

        if not due_date:
            return "No date"

        try:
            datetime.strptime(due_date, "%d/%m/%Y")
            return due_date

        except ValueError:
            print("Invalid date. Use DD/MM/YYYY.")


def add_task():
    task_name = input("\nEnter the task name: ").strip()

    if not task_name:
        print("Task name cannot be empty.")
        return

    priority = choose_priority()
    due_date = get_due_date()

    tasks.append({
        "name": task_name,
        "completed": False,
        "priority": priority,
        "due_date": due_date
    })

    save_tasks()

    print("\nTask added successfully!")


def complete_task():
    show_tasks()

    if not tasks:
        return

    try:
        task_number = int(
            input("\nWhich task did you complete? ")
        )

        if task_number < 1 or task_number > len(tasks):
            raise IndexError

        tasks[task_number - 1]["completed"] = True

        save_tasks()

        print("Task completed successfully!")

    except (ValueError, IndexError):
        print("Invalid task number.")


def delete_task():
    show_tasks()

    if not tasks:
        return

    try:
        task_number = int(
            input("\nWhich task do you want to delete? ")
        )

        if task_number < 1 or task_number > len(tasks):
            raise IndexError

        removed_task = tasks.pop(task_number - 1)

        save_tasks()

        print(f"Task '{removed_task['name']}' deleted!")

    except (ValueError, IndexError):
        print("Invalid task number.")


def show_high_priority_tasks():
    high_priority_tasks = [
        task for task in tasks
        if task.get("priority") == "High"
        and not task.get("completed", False)
    ]

    if not high_priority_tasks:
        print("\nNo pending high priority tasks.")
        return

    print("\n===== HIGH PRIORITY =====")

    for task in high_priority_tasks:
        due_date = task.get("due_date", "No date")

        print(
            f"- {task['name']} "
            f"| Due: {due_date}"
        )


def main():
    while True:

        print("\n========================")
        print("      TASK MANAGER")
        print("========================")

        print("1 - Add task")
        print("2 - Show tasks")
        print("3 - Complete task")
        print("4 - Delete task")
        print("5 - Show high priority tasks")
        print("6 - Exit")

        option = input("\nChoose an option: ").strip()

        if option == "1":
            add_task()

        elif option == "2":
            show_tasks()

        elif option == "3":
            complete_task()

        elif option == "4":
            delete_task()

        elif option == "5":
            show_high_priority_tasks()

        elif option == "6":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid option. Try again.")


if __name__ == "__main__":
    main()
