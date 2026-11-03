"""Tests for the Notebook class."""

from pathlib import Path

import pytest

from notebook.models import Category
from notebook.notebook import Notebook

@pytest.fixture
def notebook_path(tmp_path: Path) -> Path:
    """Provide a fresh temporary JSON file path."""
    return tmp_path / "test_notes.json"


@pytest.fixture
def empty_notebook(notebook_path: Path) -> Notebook:
    """Provide an empty notebook."""
    return Notebook(notebook_path)


@pytest.fixture
def populated_notebook(notebook_path: Path) -> Notebook:
    """Provide a notebook with three pre-created notes."""
    notebook = Notebook(notebook_path)

    notebook.add(
        "Learn Python",
        "Today I learned about Python sorting.",
        Category.LEARNING,
        "2026-08-18",
        True,
    )

    notebook.add(
        "Team meeting",
        "Discussed roadmap and release priorities.",
        Category.WORK,
        "2026-08-17",
    )

    notebook.add(
        "Startup idea",
        "Build a tool for organizing startup ideas.",
        Category.IDEA,
        "2026-08-19",
    )

    return notebook



class TestNotebook:
    """Tests for Notebook business logic and persistence."""

    def test_new_notebook_starts_empty(self, empty_notebook):
        """A fresh notebook starts with no notes."""
        assert empty_notebook.notes == []

    def test_add_returns_first_note_with_id_one(self, empty_notebook):
        """The first added note receives id 1."""
        note = empty_notebook.add(
            "First note",
            "This is my first note.",
            Category.PERSONAL,
            "2026-08-18",
        )

        assert note.id == 1

    def test_add_returns_sequential_ids(self, empty_notebook):
        """Successive notes receive increasing ids."""
        first = empty_notebook.add(
            "First",
            "First note body.",
            Category.PERSONAL,
            "2026-08-18",
        )

        second = empty_notebook.add(
            "Second",
            "Second note body.",
            Category.WORK,
            "2026-08-18",
        )

        assert first.id == 1
        assert second.id == 2


    def test_add_after_delete_uses_max_id_plus_one(self, populated_notebook):
        """Deleted ids are not reused when adding new notes."""
        deleted = populated_notebook.delete(2)

        assert deleted is True

        new_note = populated_notebook.add(
            "New note",
            "This note was added after deletion.",
            Category.PERSONAL,
            "2026-08-20",
        )

        assert new_note.id == 4

    def test_add_computes_word_count(self, empty_notebook):
        """Adding a note automatically computes its word count."""
        note = empty_notebook.add(
            "Word count test",
            "Python makes text processing very easy",
            Category.LEARNING,
            "2026-08-18",
        )

        assert note.word_count == 6

    def test_add_persists_across_notebook_instances(self, notebook_path):
        """A newly-created Notebook using the same file path reloads saved notes."""
        notebook1 = Notebook(notebook_path)

        notebook1.add(
            "Persistent note",
            "This note should survive a reload.",
            Category.WORK,
            "2026-08-18",
        )

        notebook2 = Notebook(notebook_path)

        assert len(notebook2.notes) == 1
        assert notebook2.notes[0].title == "Persistent note"

    def test_find_by_id_returns_existing_note(self, populated_notebook):
        """Finding an existing id returns the correct Note."""
        note = populated_notebook.find_by_id(2)

        assert note is not None
        assert note.id == 2
        assert note.title == "Team meeting"

    def test_find_by_id_returns_none_when_missing(self, populated_notebook):
        """Finding a nonexistent id returns None."""
        note = populated_notebook.find_by_id(999)

        assert note is None

    def test_update_title_changes_existing_note(self, populated_notebook):
        """Updating an existing note changes its title and returns True."""
        result = populated_notebook.update_title(
            2,
            "Updated team meeting",
        )

        note = populated_notebook.find_by_id(2)

        assert result is True
        assert note is not None
        assert note.title == "Updated team meeting"

    def test_update_title_returns_false_for_missing_id(self, populated_notebook):
        """Updating the title of a missing note returns False."""
        result = populated_notebook.update_title(
            999,
            "Nothing",
        )

        assert result is False

    def test_update_body_changes_body_and_recomputes_word_count(
        self,
        populated_notebook,
    ):
        """Updating a body also refreshes the derived word count."""
        result = populated_notebook.update_body(
            1,
            "Python sorting is becoming much easier now",
        )

        note = populated_notebook.find_by_id(1)

        assert result is True
        assert note is not None
        assert note.body == "Python sorting is becoming much easier now"
        assert note.word_count == 7

    def test_update_body_returns_false_for_missing_id(self, populated_notebook):
        """Updating the body of a missing note returns False."""
        result = populated_notebook.update_body(
            999,
            "New body",
        )

        assert result is False

    def test_toggle_pin_flips_false_to_true(self, populated_notebook):
        """Toggling an unpinned note makes it pinned."""
        note_before = populated_notebook.find_by_id(2)

        assert note_before is not None
        assert note_before.is_pinned is False

        result = populated_notebook.toggle_pin(2)

        note_after = populated_notebook.find_by_id(2)

        assert result is True
        assert note_after is not None
        assert note_after.is_pinned is True

    def test_toggle_pin_flips_true_to_false(self, populated_notebook):
        """Toggling a pinned note makes it unpinned."""
        note_before = populated_notebook.find_by_id(1)

        assert note_before is not None
        assert note_before.is_pinned is True

        result = populated_notebook.toggle_pin(1)

        note_after = populated_notebook.find_by_id(1)

        assert result is True
        assert note_after is not None
        assert note_after.is_pinned is False

    def test_toggle_pin_returns_false_for_missing_id(self, populated_notebook):
        """Toggling a nonexistent note returns False."""
        result = populated_notebook.toggle_pin(999)

        assert result is False

    def test_delete_removes_existing_note(self, populated_notebook):
        """Deleting an existing note removes it and returns True."""
        result = populated_notebook.delete(2)

        assert result is True
        assert populated_notebook.find_by_id(2) is None
        assert len(populated_notebook.notes) == 2

    def test_delete_returns_false_for_missing_id(self, populated_notebook):
        """Deleting a nonexistent note returns False."""
        result = populated_notebook.delete(999)

        assert result is False
        assert len(populated_notebook.notes) == 3

    def test_list_all_sorts_pinned_notes_first(self, populated_notebook):
        """Pinned notes appear before unpinned notes."""
        notes = populated_notebook.list_all()

        assert notes[0].id == 1
        assert notes[0].is_pinned is True

    def test_list_all_sorts_by_date_descending_within_pin_group(
    self,
    populated_notebook,
    ):
        """Within the same pin group, newer notes appear first."""
        notes = populated_notebook.list_all()

        ids = [note.id for note in notes]

        assert ids == [1, 3, 2]

    def test_list_all_sorts_same_date_by_id(self, empty_notebook):
        """Notes with the same pin status and date are sorted by id ascending."""
        empty_notebook.add(
            "First",
            "First body",
            Category.WORK,
            "2026-08-18",
        )

        empty_notebook.add(
            "Second",
            "Second body",
            Category.WORK,
            "2026-08-18",
        )

        empty_notebook.add(
            "Third",
            "Third body",
            Category.WORK,
            "2026-08-18",
        )

        notes = empty_notebook.list_all()

        ids = [note.id for note in notes]

        assert ids == [1, 2, 3]


    def test_filter_by_category_returns_matching_notes(self, populated_notebook):
        """Filtering by category returns only notes in that category."""
        notes = populated_notebook.filter_by_category(
            Category.WORK
        )

        assert len(notes) == 1
        assert notes[0].id == 2
        assert notes[0].category == Category.WORK

    def test_filter_by_category_returns_empty_when_no_match(
    self,
    populated_notebook,
    ):
        """Filtering by an unused category returns an empty list."""
        notes = populated_notebook.filter_by_category(
            Category.PERSONAL
        )

        assert notes == []

    def test_search_by_title_is_case_insensitive(self, populated_notebook):
        """Title search matches regardless of letter case."""
        notes = populated_notebook.search_by_title(
            "PYTHON"
        )

        assert len(notes) == 1
        assert notes[0].title == "Learn Python"

    def test_search_by_title_matches_substring(self, populated_notebook):
        """Title search matches when the term appears inside the title."""
        notes = populated_notebook.search_by_title(
            "meet"
        )

        assert len(notes) == 1
        assert notes[0].title == "Team meeting"

    def test_search_by_title_returns_empty_when_no_match(
    self,
    populated_notebook,
    ):
        """Title search returns an empty list when nothing matches."""
        notes = populated_notebook.search_by_title(
            "banana"
        )

        assert notes == []

    def test_search_by_body_is_case_insensitive(self, populated_notebook):
        """Body search matches regardless of letter case."""
        notes = populated_notebook.search_by_body(
            "ROADMAP"
        )

        assert len(notes) == 1
        assert notes[0].id == 2

    def test_search_by_body_matches_substring(self, populated_notebook):
        """Body search matches a term contained inside the note body."""
        notes = populated_notebook.search_by_body(
            "startup"
        )

        assert len(notes) == 1
        assert notes[0].id == 3

    def test_notes_by_date_range_returns_notes_inside_range(
    self,
    populated_notebook,
    ):
        """Date range returns notes whose dates fall inside the range."""
        notes = populated_notebook.notes_by_date_range(
            "2026-08-18",
            "2026-08-19",
        )

        ids = [note.id for note in notes]

        assert 1 in ids
        assert 3 in ids
        assert 2 not in ids

    def test_notes_by_date_range_is_inclusive(
    self,
    populated_notebook,
    ):
        """Notes exactly on the start and end dates are included."""
        notes = populated_notebook.notes_by_date_range(
            "2026-08-17",
            "2026-08-18",
        )

        ids = [note.id for note in notes]

        assert 1 in ids
        assert 2 in ids

    def test_notes_by_date_range_excludes_outside_dates(
    self,
    populated_notebook,
    ):
        """Notes outside the requested date range are excluded."""
        notes = populated_notebook.notes_by_date_range(
            "2026-08-18",
            "2026-08-18",
        )

        ids = [note.id for note in notes]

        assert ids == [1]

    def test_stats_empty_notebook(self, empty_notebook):
        """Stats on an empty notebook return the correct empty values."""
        stats = empty_notebook.stats()

        assert stats["total"] == 0
        assert stats["pinned_count"] == 0

        assert stats["by_category"] == {
            "personal": 0,
            "work": 0,
            "learning": 0,
            "idea": 0,
        }

        assert stats["total_words"] == 0
        assert stats["average_words"] == 0.0
        assert stats["longest_note_id"] is None

    def test_stats_populated_notebook(self, populated_notebook):
        """Stats correctly summarize a populated notebook."""
        stats = populated_notebook.stats()

        assert stats["total"] == 3
        assert stats["pinned_count"] == 1

        assert stats["by_category"] == {
            "personal": 0,
            "work": 1,
            "learning": 1,
            "idea": 1,
        }

        assert stats["total_words"] == 18
        assert stats["average_words"] == 6.0
        assert stats["longest_note_id"] == 3

    def test_stats_average_words_is_rounded_to_two_decimals(
    self,
    empty_notebook,
    ):
        """Average word count is rounded to two decimal places."""
        empty_notebook.add(
            "One",
            "one two",
            Category.PERSONAL,
            "2026-08-18",
        )

        empty_notebook.add(
            "Two",
            "one two three",
            Category.WORK,
            "2026-08-18",
        )

        empty_notebook.add(
            "Three",
            "one two three four five",
            Category.IDEA,
            "2026-08-18",
        )

        stats = empty_notebook.stats()

        assert stats["total_words"] == 10
        assert stats["average_words"] == 3.33


    def test_stats_longest_note_id(self, empty_notebook):
        """Stats returns the id of the note with the highest word count."""
        first = empty_notebook.add(
            "Short",
            "one two",
            Category.PERSONAL,
            "2026-08-18",
        )

        second = empty_notebook.add(
            "Longest",
            "one two three four five six",
            Category.LEARNING,
            "2026-08-18",
        )

        empty_notebook.add(
            "Medium",
            "one two three",
            Category.WORK,
            "2026-08-18",
        )

        stats = empty_notebook.stats()

        assert stats["longest_note_id"] == second.id