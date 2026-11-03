"""Tests for the Note Pydantic model."""

import pytest
from pydantic import ValidationError

from notebook.models import Category, Note


class TestNoteModel:
    """Tests for Note model validation and defaults."""

    def test_note_created_with_valid_data(self):
        """A valid Note can be created successfully."""
        note = Note(
            id=1,
            title="Learn Python",
            body="Today I learned about enums and Pydantic models.",
            category=Category.LEARNING,
            is_pinned=True,
            created_date="2026-08-18",
            word_count=8,
        )

        assert note.id == 1
        assert note.title == "Learn Python"
        assert note.body == "Today I learned about enums and Pydantic models."
        assert note.category == Category.LEARNING
        assert note.is_pinned is True
        assert note.created_date == "2026-08-18"
        assert note.word_count == 8

    def test_note_defaults_to_not_pinned(self):
        """is_pinned defaults to False when omitted."""
        note = Note(
            id=1,
            title="Work note",
            body="Prepare for tomorrow's meeting.",
            category=Category.WORK,
            created_date="2026-08-18",
            word_count=4,
        )

        assert note.is_pinned is False

    def test_note_rejects_id_zero(self):
        """Note id must be greater than zero."""
        with pytest.raises(ValidationError):
            Note(
                id=0,
                title="Invalid note",
                body="This note has an invalid id.",
                category=Category.PERSONAL,
                created_date="2026-08-18",
                word_count=6,
            )

    def test_note_rejects_negative_id(self):
        """Note id cannot be negative."""
        with pytest.raises(ValidationError):
            Note(
                id=-3,
                title="Invalid note",
                body="This note has an invalid id.",
                category=Category.PERSONAL,
                created_date="2026-08-18",
                word_count=6,
            )

    def test_note_rejects_empty_title(self):
        """Note title cannot be empty."""
        with pytest.raises(ValidationError):
            Note(
                id=1,
                title="",
                body="This note has a valid body.",
                category=Category.WORK,
                created_date="2026-08-18",
                word_count=6,
            )

    def test_note_rejects_title_over_100_characters(self):
        """Note title cannot exceed 100 characters."""
        long_title = "a" * 101

        with pytest.raises(ValidationError):
            Note(
                id=1,
                title=long_title,
                body="Valid body",
                category=Category.WORK,
                created_date="2026-08-18",
                word_count=2,
            )

    def test_note_rejects_empty_body(self):
        """Note body cannot be empty."""
        with pytest.raises(ValidationError):
            Note(
                id=1,
                title="Valid title",
                body="",
                category=Category.IDEA,
                created_date="2026-08-18",
                word_count=1,
            )

    def test_note_rejects_body_over_10000_characters(self):
        """Note body cannot exceed 10,000 characters."""
        long_body = "a" * 10001

        with pytest.raises(ValidationError):
            Note(
                id=1,
                title="Valid title",
                body=long_body,
                category=Category.IDEA,
                created_date="2026-08-18",
                word_count=1,
            )

    def test_note_rejects_word_count_zero(self):
        """word_count must be greater than zero."""
        with pytest.raises(ValidationError):
            Note(
                id=1,
                title="Valid title",
                body="Some body text",
                category=Category.LEARNING,
                created_date="2026-08-18",
                word_count=0,
            )