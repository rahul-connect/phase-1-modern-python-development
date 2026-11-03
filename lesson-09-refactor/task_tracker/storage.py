"""JSON persistence for the task tracker."""

import json
from pathlib import Path
from pydantic import ValidationError

from task_tracker.models import Task

def load_tasks(file_path: Path) -> list[Task]:
    """Load tasks from a JSON file.
    
    Returns an empty list if the file doesn't exist or is corrupted.
    """
    try:
        content = file_path.read_text()
        data = json.loads(content)
        tasks = []
        for item in data:
             tasks.append(Task(**item))
        return tasks

    except FileNotFoundError:
            return []

    except json.JSONDecodeError:
         print("File is corrupted or malformed. Starting a fresh list")
         return []

    except ValidationError:
         print("JSON parses but doesn't match Task shape. Starting a fresh list")
         return []



def save_tasks(tasks: list[Task], file_path: Path) -> None:
    """Save tasks to a JSON file, overwriting any existing content."""
    # your code here
    try:
         list_of_dicts = []
         for task in tasks:             
              list_of_dicts.append(task.model_dump())
         file_path.write_text(json.dumps(list_of_dicts, indent=2))
    except OSError:
         print("OS ERROR:Something went wrong.")