tasks = []


def show_tasks():
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n--- TASKS ---")

    for index, task in enumerate(tasks, start=1):
        status = "✓" if task["completed"] else " "
        print(f"{index}. [{status}] {task['name']}")


def add_task():
    task_name = input("\nEnter the task name: ")

    tasks.append({
        "name": task_name,
        "completed": False
    })

    print("Task added successfully!")


def complete_task():
    show_tasks()

    if not tasks:
        return

    try:
        task_number = int(input("\nWhich task did you complete? "))

        tasks[task_number - 1]["completed"] = True

        print("Task completed!")

    except (ValueError, IndexError):
        print("Invalid task number.")


def delete_task():
    show_tasks()

    if not tasks:
        return

    try:
        task_number = int(input("\nWhich task do you want to delete? "))

        removed_task = tasks.pop(task_number - 1)

        print(f"Task '{removed_task['name']}' deleted!")

    except (ValueError, IndexError):
        print("Invalid task number.")


def main():
    while True:
        print("\n===== TASK MANAGER =====")
        print("1 - Add task")
        print("2 - Show tasks")
        print("3 - Complete task")
        print("4 - Delete task")
        print("5 - Exit")

        option = input("\nChoose an option: ")

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
