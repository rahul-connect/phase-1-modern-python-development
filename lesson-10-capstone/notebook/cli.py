from notebook.models import Note, Category
from pathlib import Path

from notebook.notebook import Notebook

def get_required_input(prompt: str) -> str:
    """Ask until the user enters non-empty text."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("Field cannot be empty")


def get_menu_choice() -> int:
    """Ask until the user enters a valid menu choice from 1 to 12."""
    while True:
        try:
            choice = int(
                input("What do you want to do? ").strip()
            )

            if 1 <= choice <= 12:
                return choice

            print("Please enter a number between 1 and 12")

        except ValueError:
            print("Please enter only a numeric value")

def get_category(prompt: str) -> Category:
    """Ask until the user enters a valid note category."""
    while True:
        value = input(prompt).strip().lower()

        try:
            return Category(value)

        except ValueError:
            print(
                f"Invalid category. Choose: "
                f"{[category.value for category in Category]}"
            )


def get_note_id(prompt: str) -> int:
    """Ask until the user enters a positive integer note id."""
    while True:
        try:
            note_id = int(input(prompt).strip())

            if note_id > 0:
                return note_id

            print("Note id must be greater than 0")

        except ValueError:
            print("Please enter a valid numeric note id")


def preview(text: str, max_length: int = 100) -> str:
    """Return the text truncated to the requested preview length."""
    if len(text) <= max_length:
        return text

    shortened_text = text[:max_length]

    return shortened_text + "..."


def print_note(note: Note) -> None:
    """Print one note in a human-readable format."""

    if note.is_pinned:
        pin_text = "📌 "
        pinned_status = " | Pinned"
    else:
        pin_text = ""
        pinned_status = ""

    body_preview = preview(note.body)

    print(f"[id {note.id}] {pin_text}{note.title}")

    print(
        f"   Category: {note.category.value} "
        f"| {note.word_count} words"
        f"{pinned_status}"
    )

    print(f"   Created: {note.created_date}")
    print(f"   Body: {body_preview}")


def print_menu() -> None:
    """Print the twelve available notebook menu options."""
    print("1. Add note")
    print("2. List all notes")
    print("3. Update note title")
    print("4. Update note body")
    print("5. Toggle pin on a note")
    print("6. Filter by category")
    print("7. Search by title")
    print("8. Search by body")
    print("9. Notes in a date range")
    print("10. Delete note")
    print("11. Show statistics")
    print("12. Quit")


def main() -> None:
    """Initialize the notebook and run the interactive menu loop."""
    file_path = Path(__file__).parent.parent / "notes.json"
    notebook = Notebook(file_path)

    while True:
        print_menu()
        choice = get_menu_choice()

        if choice == 1:
            title = get_required_input("Enter title: ")
            body = get_required_input("Enter body: ")
            category = get_category(
                "Enter category (personal, work, learning, idea): "
            )
            created_date = get_required_input(
                "Enter created date (YYYY-MM-DD): "
            )

            pin_input = input(
                "Pin this note? (y/n): "
            ).strip().lower()

            is_pinned = pin_input == "y"

            note = notebook.add(
                title,
                body,
                category,
                created_date,
                is_pinned,
            )

            print(f"Added note [id {note.id}]")

        elif choice == 2:
            notes = notebook.list_all()

            if not notes:
                print("No notes yet")
            else:
                for note in notes:
                    print_note(note)
                    print()

        elif choice == 3:
            note_id = get_note_id(
                "Enter id of the note to update: "
            )

            new_title = get_required_input(
                "Enter new title: "
            )

            updated = notebook.update_title(
                note_id,
                new_title,
            )

            if updated:
                print(f"Note [id {note_id}] title updated")
            else:
                print(f"Note with id {note_id} not found")
        elif choice == 4:
            note_id = get_note_id(
                "Enter id of the note to update: "
            )

            new_body = get_required_input(
                "Enter new body: "
            )

            updated = notebook.update_body(
                note_id,
                new_body,
            )

            if updated:
                print(f"Note [id {note_id}] body updated")
            else:
                print(f"Note with id {note_id} not found")
        elif choice == 5:
            note_id = get_note_id(
                "Enter id of the note to toggle pin: "
            )

            toggled = notebook.toggle_pin(note_id)

            if toggled:
                print(f"Note [id {note_id}] pin status changed")
            else:
                print(f"Note with id {note_id} not found")
        elif choice == 6:
            category = get_category(
                "Enter category (personal, work, learning, idea): "
            )

            notes = notebook.filter_by_category(category)

            if not notes:
                print("No matches")
            else:
                for note in notes:
                    print_note(note)
        elif choice == 7:
            term = get_required_input(
                "Enter title search term: "
            )

            notes = notebook.search_by_title(term)

            if not notes:
                print("No matches")
            else:
                for note in notes:
                    print_note(note)
        elif choice == 8:
            term = get_required_input(
                "Enter body search term: "
            )

            notes = notebook.search_by_body(term)

            if not notes:
                print("No matches")
            else:
                for note in notes:
                    print_note(note)
        elif choice == 9:
            start_date = get_required_input(
                "Enter start date (YYYY-MM-DD): "
            )

            end_date = get_required_input(
                "Enter end date (YYYY-MM-DD): "
            )

            notes = notebook.notes_by_date_range(
                start_date,
                end_date,
            )

            if not notes:
                print("No matches")
            else:
                for note in notes:
                    print_note(note)
        elif choice == 10:
            note_id = get_note_id(
                "Enter id of the note to delete: "
            )

            note = notebook.find_by_id(note_id)

            if note is None:
                print(f"Note with id {note_id} not found")
                continue

            print_note(note)

            confirmation = input(
                "Delete this note? (y/n): "
            ).strip().lower()

            if confirmation == "y":
                deleted = notebook.delete(note_id)

                if deleted:
                    print(f"Note [id {note_id}] deleted")
                else:
                    print(f"Note [id {note_id}] not found (someone deleted it between check and delete?)")
            else:
                print("Delete cancelled")
        elif choice == 11:
            stats = notebook.stats()

            print(f"Total notes: {stats['total']}")
            print(f"Pinned notes: {stats['pinned_count']}")
            print(f"By category: {stats['by_category']}")
            print(f"Total words: {stats['total_words']}")
            print(f"Average words: {stats['average_words']:.2f}")
            print(f"Longest note id: {stats['longest_note_id']}")
        elif choice == 12:
            print("Goodbye")
            break
                    