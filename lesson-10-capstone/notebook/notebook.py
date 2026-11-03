from pathlib import Path
from notebook.storage import load_notes, save_notes
from notebook.models import Note, Category

class Notebook:
    """Manage notes and persist them to JSON."""

    def __init__(self, file_path:Path) -> None:
        """Initialize the notebook by loading notes from the given file."""
        self.file_path = file_path
        self.notes: list[Note] = load_notes(file_path)


    def next_id(self) -> int:
        """Return the next unique persistent note id."""
        if not self.notes:
            return 1

        return max(note.id for note in self.notes) + 1

    def add(self, title:str, body:str, category:Category, created_date:str, is_pinned: bool=False) -> Note:
        """Create, save, and return a new note."""
        new_id = self.next_id()

        words = body.split()
        word_count = len(words)

        new_note = Note(
            id=new_id,
            title=title,
            body=body,
            category=category,
            is_pinned=is_pinned,
            created_date=created_date,
            word_count=word_count
        )

        self.notes.append(new_note)
        save_notes(self.notes,self.file_path)
        return new_note

    def get_sort_value(self, note: Note) -> tuple[bool, int, int]:
        """Return the values used to sort notes."""

        pinned_value = not note.is_pinned

        date_number = int(
            note.created_date.replace("-", "")
        )

        descending_date_value = -date_number

        note_id = note.id

        # Here Using 'not' flips True -> False and False -> True so pinned notes
        # come first when Python sorts in ascending order.

        return (
            pinned_value,
            descending_date_value,
            note_id,
        )

    def list_all(self) -> list[Note]:
        """Return all notes sorted by pin status, date, and id."""
        return sorted(
            self.notes,
            key=self.get_sort_value,
        )

    def find_by_id(self, note_id: int) -> Note | None:
        """Return the note with the given id, or None if not found."""

        for note in self.notes:
            if note.id == note_id:
                return note

        return None

    def update_title(
    self,
    note_id: int,
    new_title: str,
    ) -> bool:
        """Update a note's title."""

        note = self.find_by_id(note_id)

        if note is None:
            return False

        note.title = new_title

        save_notes(
            self.notes,
            self.file_path,
        )

        return True

    def update_body(
    self,
    note_id: int,
    new_body: str,
    ) -> bool:
        """Update a note's body."""

        note = self.find_by_id(note_id)

        if note is None:
            return False

        note.body = new_body

        note.word_count = len(
            new_body.split()
        )

        save_notes(
            self.notes,
            self.file_path,
        )

        return True

    def toggle_pin(
    self,
    note_id: int,
    ) -> bool:
        """Toggle whether a note is pinned."""

        note = self.find_by_id(note_id)

        if note is None:
            return False

        note.is_pinned = not note.is_pinned

        save_notes(
            self.notes,
            self.file_path,
        )

        return True

    def delete(
    self,
    note_id: int,
    ) -> bool:
        """Delete a note by id."""

        note = self.find_by_id(note_id)

        if note is None:
            return False

        self.notes.remove(note)

        save_notes(
            self.notes,
            self.file_path,
        )

        return True

    def filter_by_category(self, category: Category) -> list[Note]:
        """Return notes matching the given category."""
        results = []

        for note in self.notes:
            if note.category == category:
                results.append(note)

        return results

    def search_by_title(self, term: str) -> list[Note]:
        """Return notes whose titles contain the search term."""
        term_lower = term.lower()
        results = []

        for note in self.notes:
            title_lower = note.title.lower()

            if term_lower in title_lower:
                results.append(note)

        return results

    def search_by_body(self, term: str) -> list[Note]:
        """Return notes whose bodies contain the search term."""
        term_lower = term.lower()
        results = []

        for note in self.notes:
            body_lower = note.body.lower()

            if term_lower in body_lower:
                results.append(note)

        return results

    def notes_by_date_range(
    self,
    start_date: str,
    end_date: str,
    ) -> list[Note]:
        """Return notes created within the inclusive date range."""
        results = []

        for note in self.notes:
            if start_date <= note.created_date <= end_date:
                results.append(note)

        return results

    def stats(self) -> dict:
        """Return summary statistics for the notebook."""

        total = len(self.notes)

        by_category = {}

        for category in Category:
            by_category[category.value] = 0

        pinned_count = 0
        total_words = 0

        for note in self.notes:

            by_category[note.category.value] += 1

            if note.is_pinned:
                pinned_count += 1

            total_words += note.word_count

        if total == 0:
            average_words = 0.0
        else:
            average_words = round(
                total_words / total,
                2,
            )

        if not self.notes:
            longest_note_id = None
        else:
            def get_word_count(note: Note) -> int:
                return note.word_count

            longest_note = max(
                self.notes,
                key=get_word_count,
            )

            longest_note_id = longest_note.id

        return {
            "total": total,
            "pinned_count": pinned_count,
            "by_category": by_category,
            "total_words": total_words,
            "average_words": average_words,
            "longest_note_id": longest_note_id,
        }