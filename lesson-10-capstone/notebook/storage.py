"""Functions for loading and saving notes."""

import json
from pathlib import Path

from pydantic import ValidationError
from notebook.models import Note

def load_notes(file_path: Path) -> list[Note]:
    """Load notes from a JSON file."""

    try:
        with open(file_path,"r") as file:
            data = json.load(file)

        notes = []

        for note_data in data:
            note = Note(**note_data)
            notes.append(note)

        return notes
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(
            f"Warning: {file_path.name} is corrupted. "
            "Starting with an empty notebook."
        )
        return []
    except ValidationError:
        print(
        f"Warning: {file_path} contains invalid note data. "
        "Starting with empty notebook."
        )
        return []



def save_notes(notes: list[Note], file_path: Path) -> None:
    """Save notes to a JSON file."""

    data = []

    for note in notes:
        data.append(note.model_dump())

    with open(file_path,"w") as file:
        json.dump(data, file, indent=2)