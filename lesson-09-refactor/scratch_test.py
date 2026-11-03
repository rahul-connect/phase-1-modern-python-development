from pathlib import Path
from task_tracker.models import Priority, Status
from task_tracker.tracker import TaskTracker

path = Path("step3d_test.json")
if path.exists():
    path.unlink()

tracker = TaskTracker(path)

# Empty stats
print("Stats when empty:")
print(tracker.stats())

# Add tasks
tracker.add("Write API docs", Priority.HIGH, "2026-08-13", ["docs", "api"])
tracker.add("Review Pull Request", Priority.MEDIUM, "2026-08-13", ["review"])
tracker.add("Fix login bug", Priority.HIGH, "2026-08-14", ["bug", "urgent"])
tracker.add("Update dependencies", Priority.LOW, "2026-08-15", ["maintenance"])
tracker.add("Deploy to staging", Priority.MEDIUM, "2026-08-15", ["deploy", "urgent"])

# Change some statuses  
tracker.update_status(1, Status.DONE)
tracker.update_status(3, Status.IN_PROGRESS)

print("\nStats after 5 tasks:")
print(tracker.stats())