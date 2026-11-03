"""User-facing CLI for the task tracker."""

from pathlib import Path

from task_tracker.models import Priority, Status, Task
from task_tracker.tracker import TaskTracker


def get_required_input(prompt: str) -> str:
    """Ask for input repeatedly until the user enters a non-empty value."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("Field cannot be empty")


def get_menu_choice() -> int:
    """Ask for a menu choice repeatedly until a valid integer from 1 to 11 is entered."""
    while True:
        try:
            choice = int(input("What do you want to do? ").strip())

            if 1 <= choice <= 11:
                return choice

            print("Please enter a number between 1 and 11")

        except ValueError:
            print("Please enter only a numeric value")


def get_priority(prompt: str) -> Priority:
    """Ask for a priority repeatedly until a valid Priority enum value is entered."""
    while True:
        value = input(prompt).strip().lower()

        try:
            return Priority(value)

        except ValueError:
            print(
                f"Invalid priority. Choose: "
                f"{[priority.value for priority in Priority]}"
            )


def get_status(prompt: str) -> Status:
    """Ask for a status repeatedly until a valid Status enum value is entered."""
    while True:
        value = input(prompt).strip().lower()

        try:
            return Status(value)

        except ValueError:
            print(
                f"Invalid status. Choose: "
                f"{[status.value for status in Status]}"
            )


def get_task_id(prompt: str) -> int:
    """Ask for a task id repeatedly until a positive integer is entered."""
    while True:
        try:
            task_id = int(input(prompt).strip())

            if task_id > 0:
                return task_id

            print("Task id must be greater than 0")

        except ValueError:
            print("Please enter a valid numeric task id")


def print_task(task: Task, prefix: str = "") -> None:
    """Print one task in a clean human-readable format."""
    if task.tags:
        tags_text = ", ".join(task.tags)
    else:
        tags_text = "(none)"

    print(f"{prefix}[id {task.id}] {task.title}")
    print(
        f"{prefix}   Priority: {task.priority.value} "
        f"| Status: {task.status.value}"
    )
    print(f"{prefix}   Created: {task.created_date}")
    print(f"{prefix}   Tags: {tags_text}")


def print_menu() -> None:
    """Print the eleven available task tracker menu options."""
    print("1. Add task")
    print("2. List all tasks")
    print("3. Update task status")
    print("4. Update task priority")
    print("5. Filter by status")
    print("6. Filter by priority")
    print("7. Search by title")
    print("8. Filter by tag")
    print("9. Show statistics")
    print("10. Delete task")
    print("11. Quit")


def main() -> None:
    """Initialize the task tracker and run the interactive menu loop."""
    file_path = Path(__file__).parent.parent / "tasks.json"
    tracker = TaskTracker(file_path)

    while True:
        print_menu()
        choice = get_menu_choice()

        if choice == 1:
            title = get_required_input("Enter title: ")

            priority = get_priority(
                "Enter priority (low, medium, high): "
            )

            created_date = get_required_input(
                "Enter date (YYYY-MM-DD): "
            )

            tags_input = input(
                "Enter tags (comma-separated, or leave empty): "
            ).strip()

            tags = [
                tag.strip()
                for tag in tags_input.split(",")
                if tag.strip()
            ]

            task = tracker.add(
                title,
                priority,
                created_date,
                tags
            )

            print(f"Added task [id {task.id}]")

        elif choice == 2:
            tasks = tracker.list_all()

            if not tasks:
                print("No tasks yet")
            else:
                for task in tasks:
                    print_task(task)
                    print()

        elif choice == 3:
            tasks = tracker.list_all()

            if not tasks:
                print("No tasks to update")
                continue

            for task in tasks:
                print_task(task)
                print()

            task_id = get_task_id(
                "Enter id of the task to update: "
            )

            new_status = get_status(
                "Enter new status (todo, in_progress, done): "
            )

            updated = tracker.update_status(
                task_id,
                new_status
            )

            if updated:
                print(
                    f"Task [id {task_id}] status updated "
                    f"to {new_status.value}"
                )
            else:
                print(f"Task with id {task_id} not found")

        elif choice == 4:
            tasks = tracker.list_all()

            if not tasks:
                print("No tasks to update")
                continue

            for task in tasks:
                print_task(task)
                print()

            task_id = get_task_id(
                "Enter id of the task to update: "
            )

            new_priority = get_priority(
                "Enter new priority (low, medium, high): "
            )

            updated = tracker.update_priority(
                task_id,
                new_priority
            )

            if updated:
                print(
                    f"Task [id {task_id}] priority updated "
                    f"to {new_priority.value}"
                )
            else:
                print(f"Task with id {task_id} not found")

        elif choice == 5:
            status = get_status(
                "Enter status to filter by "
                "(todo, in_progress, done): "
            )

            tasks = tracker.filter_by_status(status)

            if not tasks:
                print("No matches")
            else:
                for task in tasks:
                    print_task(task)
                    print()

        elif choice == 6:
            priority = get_priority(
                "Enter priority to filter by "
                "(low, medium, high): "
            )

            tasks = tracker.filter_by_priority(priority)

            if not tasks:
                print("No matches")
            else:
                for task in tasks:
                    print_task(task)
                    print()

        elif choice == 7:
            term = get_required_input(
                "Enter title to search for: "
            )

            tasks = tracker.search_by_title(term)

            if not tasks:
                print("No matches")
            else:
                for task in tasks:
                    print_task(task)
                    print()

        elif choice == 8:
            tag = get_required_input(
                "Enter tag to filter by: "
            )

            tasks = tracker.filter_by_tag(tag)

            if not tasks:
                print("No matches")
            else:
                for task in tasks:
                    print_task(task)
                    print()

        elif choice == 9:
            statistics = tracker.stats()

            print(f"Total tasks: {statistics['total']}")
            print(f"By status: {statistics['by_status']}")
            print(f"By priority: {statistics['by_priority']}")
            print(
                f"Percent done: "
                f"{statistics['percent_done']:.2f}%"
            )
            print(
                f"Unique tags: "
                f"{statistics['unique_tags']}"
            )

        elif choice == 10:
            tasks = tracker.list_all()

            if not tasks:
                print("No tasks to delete")
                continue

            for task in tasks:
                print_task(task)
                print()

            task_id = get_task_id(
                "Enter id of the task to delete: "
            )

            task = tracker.find_by_id(task_id)

            if task is None:
                print(f"Task with id {task_id} not found")
                continue

            print_task(task)

            confirmation = input(
                "Delete this task? (y/n): "
            ).strip().lower()

            if confirmation == "y":
                deleted = tracker.delete(task_id)

                if deleted:
                    print(f"Task [id {task_id}] deleted")
                else:
                    print(f"Task with id {task_id} not found")
            else:
                print("Delete cancelled")

        elif choice == 11:
            print("Goodbye")
            break

