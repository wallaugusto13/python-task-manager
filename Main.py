import json
from pathlib import Path
from datetime import datetime, date

DATA_FILE = Path("tasks.json")

PRIORITY_ORDER = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}


# =========================
# LOAD AND SAVE
# =========================

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
            json.dump(
                tasks,
                file,
                indent=4,
                ensure_ascii=False
            )

    except OSError:
        print("Could not save tasks.")


tasks = load_tasks()


# =========================
# DATE FUNCTIONS
# =========================

def parse_date(date_text):
    if not date_text or date_text == "No date":
        return None

    try:
        return datetime.strptime(
            date_text,
            "%d/%m/%Y"
        ).date()

    except ValueError:
        return None


def is_overdue(task):
    if task.get("completed", False):
        return False

    due_date = parse_date(
        task.get("due_date", "No date")
    )

    if due_date is None:
        return False

    return due_date < date.today()


# =========================
# SHOW TASKS
# =========================

def show_tasks(task_list=None):
    if task_list is None:
        task_list = tasks

    if not task_list:
        print("\nNo tasks found.")
        return

    print("\n========== TASKS ==========")

    for index, task in enumerate(task_list, start=1):

        completed = task.get(
            "completed",
            False
        )

        status = "✓" if completed else " "

        priority = task.get(
            "priority",
            "Medium"
        )

        category = task.get(
            "category",
            "General"
        )

        due_date = task.get(
            "due_date",
            "No date"
        )

        overdue = ""

        if is_overdue(task):
            overdue = " | OVERDUE!"

        print(
            f"{index}. [{status}] "
            f"{task['name']} "
            f"| Priority: {priority} "
            f"| Category: {category} "
            f"| Due: {due_date}"
            f"{overdue}"
        )


# =========================
# PRIORITY
# =========================

def choose_priority(current=None):
    print("\nChoose the priority:")
    print("1 - Low")
    print("2 - Medium")
    print("3 - High")

    if current:
        option = input(
            f"Priority [{current}]: "
        ).strip()

        if not option:
            return current

    else:
        option = input(
            "Priority: "
        ).strip()

    priorities = {
        "1": "Low",
        "2": "Medium",
        "3": "High"
    }

    return priorities.get(
        option,
        current or "Medium"
    )


# =========================
# CATEGORY
# =========================

def choose_category(current=None):
    print("\nChoose the category:")
    print("1 - Work")
    print("2 - Study")
    print("3 - Personal")
    print("4 - Other")

    if current:
        option = input(
            f"Category [{current}]: "
        ).strip()

        if not option:
            return current

    else:
        option = input(
            "Category: "
        ).strip()

    categories = {
        "1": "Work",
        "2": "Study",
        "3": "Personal",
        "4": "Other"
    }

    return categories.get(
        option,
        current or "Other"
    )


# =========================
# DUE DATE
# =========================

def get_due_date():
    while True:

        due_date = input(
            "Due date (DD/MM/YYYY) "
            "or press Enter for no date: "
        ).strip()

        if not due_date:
            return "No date"

        try:
            datetime.strptime(
                due_date,
                "%d/%m/%Y"
            )

            return due_date

        except ValueError:
            print(
                "Invalid date. Use DD/MM/YYYY."
            )


def edit_due_date(current):
    while True:

        print(
            "\nCurrent due date:",
            current
        )

        due_date = input(
            "New date (DD/MM/YYYY), "
            "Enter to keep or 0 to remove: "
        ).strip()

        if not due_date:
            return current

        if due_date == "0":
            return "No date"

        try:
            datetime.strptime(
                due_date,
                "%d/%m/%Y"
            )

            return due_date

        except ValueError:
            print(
                "Invalid date. Use DD/MM/YYYY."
            )


# =========================
# ADD TASK
# =========================

def add_task():
    task_name = input(
        "\nEnter the task name: "
    ).strip()

    if not task_name:
        print(
            "Task name cannot be empty."
        )
        return

    priority = choose_priority()

    category = choose_category()

    due_date = get_due_date()

    tasks.append({
        "name": task_name,
        "completed": False,
        "priority": priority,
        "category": category,
        "due_date": due_date
    })

    save_tasks()

    print(
        "\nTask added successfully!"
    )


# =========================
# COMPLETE TASK
# =========================

def complete_task():
    show_tasks()

    if not tasks:
        return

    try:
        task_number = int(
            input(
                "\nWhich task did you complete? "
            )
        )

        if (
            task_number < 1
            or task_number > len(tasks)
        ):
            raise IndexError

        tasks[
            task_number - 1
        ]["completed"] = True

        save_tasks()

        print(
            "Task completed successfully!"
        )

    except (ValueError, IndexError):
        print("Invalid task number.")


# =========================
# EDIT TASK
# =========================

def edit_task():
    show_tasks()

    if not tasks:
        return

    try:
        task_number = int(
            input(
                "\nWhich task do you want to edit? "
            )
        )

        if (
            task_number < 1
            or task_number > len(tasks)
        ):
            raise IndexError

        task = tasks[
            task_number - 1
        ]

        print(
            f"\nEditing: {task['name']}"
        )

        new_name = input(
            f"New name [{task['name']}]: "
        ).strip()

        if new_name:
            task["name"] = new_name

        task["priority"] = choose_priority(
            task.get(
                "priority",
                "Medium"
            )
        )

        task["category"] = choose_category(
            task.get(
                "category",
                "General"
            )
        )

        task["due_date"] = edit_due_date(
            task.get(
                "due_date",
                "No date"
            )
        )

        save_tasks()

        print(
            "\nTask updated successfully!"
        )

    except (ValueError, IndexError):
        print("Invalid task number.")


# =========================
# DELETE TASK
# =========================

def delete_task():
    show_tasks()

    if not tasks:
        return

    try:
        task_number = int(
            input(
                "\nWhich task do you want to delete? "
            )
        )

        if (
            task_number < 1
            or task_number > len(tasks)
        ):
            raise IndexError

        removed_task = tasks.pop(
            task_number - 1
        )

        save_tasks()

        print(
            f"Task '{removed_task['name']}' deleted!"
        )

    except (ValueError, IndexError):
        print("Invalid task number.")


# =========================
# HIGH PRIORITY
# =========================

def show_high_priority_tasks():
    high_priority = [
        task
        for task in tasks
        if task.get(
            "priority"
        ) == "High"
        and not task.get(
            "completed",
            False
        )
    ]

    if not high_priority:
        print(
            "\nNo pending high priority tasks."
        )
        return

    print(
        "\n===== HIGH PRIORITY ====="
    )

    show_tasks(high_priority)


# =========================
# OVERDUE TASKS
# =========================

def show_overdue_tasks():
    overdue_tasks = [
        task
        for task in tasks
        if is_overdue(task)
    ]

    if not overdue_tasks:
        print(
            "\nNo overdue tasks. Great job!"
        )
        return

    print(
        "\n===== OVERDUE TASKS ====="
    )

    show_tasks(overdue_tasks)


# =========================
# SORT TASKS
# =========================

def sort_tasks():
    tasks.sort(
        key=lambda task: (
            task.get(
                "completed",
                False
            ),
            PRIORITY_ORDER.get(
                task.get(
                    "priority",
                    "Medium"
                ),
                2
            )
        )
    )

    save_tasks()

    print(
        "\nTasks sorted by priority!"
    )

    show_tasks()


# =========================
# SEARCH
# =========================

def search_tasks():
    if not tasks:
        print("\nNo tasks found.")
        return

    search_term = input(
        "\nSearch task: "
    ).strip().lower()

    if not search_term:
        print(
            "Search cannot be empty."
        )
        return

    results = [
        task
        for task in tasks
        if search_term in task.get(
            "name",
            ""
        ).lower()
        or search_term in task.get(
            "category",
            ""
        ).lower()
    ]

    if not results:
        print(
            "\nNo matching tasks found."
        )
        return

    print(
        f"\nFound {len(results)} task(s):"
    )

    show_tasks(results)


# =========================
# STATISTICS
# =========================

def show_statistics():
    total = len(tasks)

    if total == 0:
        print(
            "\nNo tasks available."
        )
        return

    completed = sum(
        1
        for task in tasks
        if task.get(
            "completed",
            False
        )
    )

    pending = total - completed

    overdue = sum(
        1
        for task in tasks
        if is_overdue(task)
    )

    high_priority = sum(
        1
        for task in tasks
        if task.get(
            "priority"
        ) == "High"
        and not task.get(
            "completed",
            False
        )
    )

    completion_rate = (
        completed / total
    ) * 100

    print(
        "\n===== STATISTICS ====="
    )

    print(
        f"Total tasks: {total}"
    )

    print(
        f"Completed: {completed}"
    )

    print(
        f"Pending: {pending}"
    )

    print(
        f"Overdue: {overdue}"
    )

    print(
        f"High priority pending: "
        f"{high_priority}"
    )

    print(
        f"Completion rate: "
        f"{completion_rate:.1f}%"
    )


# =========================
# MAIN MENU
# =========================

def main():

    while True:

        print(
            "\n=========================="
        )

        print(
            "       TASK MANAGER"
        )

        print(
            "=========================="
        )

        print("1 - Add task")
        print("2 - Show tasks")
        print("3 - Complete task")
        print("4 - Edit task")
        print("5 - Delete task")

        print(
            "6 - Show high priority tasks"
        )

        print(
            "7 - Show overdue tasks"
        )

        print(
            "8 - Sort tasks by priority"
        )

        print(
            "9 - Search tasks"
        )

        print(
            "10 - Statistics"
        )

        print(
            "11 - Exit"
        )

        option = input(
            "\nChoose an option: "
        ).strip()

        if option == "1":
            add_task()

        elif option == "2":
            show_tasks()

        elif option == "3":
            complete_task()

        elif option == "4":
            edit_task()

        elif option == "5":
            delete_task()

        elif option == "6":
            show_high_priority_tasks()

        elif option == "7":
            show_overdue_tasks()

        elif option == "8":
            sort_tasks()

        elif option == "9":
            search_tasks()

        elif option == "10":
            show_statistics()

        elif option == "11":
            print(
                "\nGoodbye!"
            )
            break

        else:
            print(
                "\nInvalid option. Try again."
            )


if __name__ == "__main__":
    main()
               
