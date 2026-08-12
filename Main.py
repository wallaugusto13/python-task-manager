import json
from pathlib import Path

DATA_FILE = Path("tasks.json")


def load_tasks():
    """Load saved tasks from the JSON file."""
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
    """Save all tasks to the JSON file."""
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

    print("\n===== TASKS =====")

    for index, task in enumerate(tasks, start=1):
        status = "✓" if task["completed"] else " "
        print(f"{index}. [{status}] {task['name']}")


def add_task():
    task_name = input("\nEnter the task name: ").strip()

    if not task_name:
        print("Task name cannot be empty.")
        return

    tasks.append({
        "name": task_name,
        "completed": False
    })

    save_tasks()

    print("Task added successfully!")


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


def main():

    while True:

        print("\n========================")
        print("      TASK MANAGER")
        print("========================")

        print("1 - Add task")
        print("2 - Show tasks")
        print("3 - Complete task")
        print("4 - Delete task")
        print("5 - Exit")

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
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid option. Try again.")


if __name__ == "__main__":
    main()
