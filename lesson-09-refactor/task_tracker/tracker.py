"""TaskTracker: the main business logic layer."""

from pathlib import Path

from task_tracker.models import Task, Priority, Status
from task_tracker.storage import load_tasks, save_tasks


PRIORITY_ORDER = {
    Priority.HIGH: 0,
    Priority.MEDIUM: 1,
    Priority.LOW: 2,
}


class TaskTracker:
    """Manages a collection of tasks with automatic persistence to JSON."""
    
    def __init__(self, file_path: Path) -> None:
        """Initialize by loading tasks from the given file path."""
        self.file_path = file_path
        self.tasks: list[Task] = load_tasks(file_path)
    
    def next_id(self) -> int:
        """Return the next unique task id."""
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1
    
    def add(self, title: str, priority: Priority, created_date: str, tags: list[str] | None = None) -> Task:
        """Create and add a new task. Returns the created Task."""
        if tags is None:
            tags = []
        new_id = self.next_id()
        task_data = {
                "id": new_id,
                "title": title,
                "priority": priority,
                "created_date": created_date,
                "tags": tags
            }
        new_task = Task(**task_data)
        self.tasks.append(new_task)
        save_tasks(self.tasks,self.file_path)
        return new_task
    
    def list_all(self) -> list[Task]:
        """Return all tasks, sorted by priority (high first) then by id ascending."""
        if not self.tasks:
            return []
        sorted_tasks = sorted(self.tasks, key=self.get_sort_value)
        return sorted_tasks
    
    def get_sort_value(self, task: Task) -> tuple[int, int]:
        """Return (priority_rank, task_id) for sorting. High priority first, then lowest id."""
        return (PRIORITY_ORDER[task.priority], task.id)

    def find_by_id(self, task_id: int) -> Task | None:
        """Return the task with the given id, or None if not found."""
        # Loop through self.tasks. Return the one where task.id == task_id.
        # If no match, return None.
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_status(self, task_id: int, new_status: Status) -> bool:
        """Update a task's status. Returns True on success, False if id not found."""
        task = self.find_by_id(task_id)
        if task is None:
            return False
        task.status = new_status
        save_tasks(self.tasks,self.file_path)
        return True

    def update_priority(self, task_id: int, new_priority: Priority) -> bool:
        """Update a task's priority. Returns True on success, False if id not found."""
        task = self.find_by_id(task_id)
        if task is None:
            return False
        task.priority = new_priority
        save_tasks(self.tasks,self.file_path)
        return True

    def delete(self, task_id: int) -> bool:
        """Delete a task by id. Returns True if deleted, False if not found."""
        task = self.find_by_id(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        save_tasks(self.tasks,self.file_path)
        return True

    def filter_by_status(self, status: Status) -> list[Task]:
        """Return tasks matching the given status."""
        return [task for task in self.tasks if task.status == status]

    def filter_by_priority(self, priority: Priority) -> list[Task]:
        """Return tasks matching the given priority."""
        return [task for task in self.tasks if task.priority == priority]

    def search_by_title(self, term: str) -> list[Task]:
        """Return tasks whose title contains the term (case-insensitive)."""
        term_lower = term.lower()
        searched_list = []
        for task in self.tasks:
            if term_lower in task.title.lower():
                searched_list.append(task)
        return searched_list

    def filter_by_tag(self, tag: str) -> list[Task]:
        """Return tasks that have the given tag (case-insensitive)."""
        tag_lower = tag.lower()
        results = []
        for task in self.tasks:
            lowered_tags = [t.lower() for t in task.tags]
            if tag_lower in lowered_tags:
                results.append(task)
        return results
    
    def stats(self) -> dict:
        """Return statistics: total, by_status counts, by_priority counts, percent_done, unique_tags."""
        total = len(self.tasks)
        by_status = {status.value:0 for status in Status}
        by_priority = {priority.value:0 for priority in Priority}
        unique_tags = set()
        for task in self.tasks:
            by_status[task.status.value] += 1
            by_priority[task.priority.value] += 1

            for tag in task.tags:
                unique_tags.add(tag.lower())

        if total == 0:
            percent_done = 0.00
        else:
            percent_done = (by_status[Status.DONE.value] / total) * 100

        return {
            "total": total,
            "by_status": by_status,
            "by_priority": by_priority,
            "percent_done": round(percent_done, 2),
            "unique_tags": len(unique_tags),
        }
