"""Tests for the Pydantic models."""

import pytest
from pydantic import ValidationError

from task_tracker.models import Task, Priority, Status


class TestTaskModel:
    """Tests for validation and defaults on the Task model."""

    def test_task_created_with_valid_data(self):
        """A valid Task can be constructed."""
        task = Task(
            id=1,
            title="Fix login bug",
            priority=Priority.HIGH,
            created_date="2026-08-13",
            tags=["bug", "urgent"],
        )

        assert task.id == 1
        assert task.title == "Fix login bug"
        assert task.priority == Priority.HIGH
        assert task.status == Status.TODO
        assert task.created_date == "2026-08-13"
        assert task.tags == ["bug", "urgent"]

    def test_task_defaults_to_todo_status(self):
        """When status is omitted, it defaults to Status.TODO."""
        task = Task(
            id=1,
            title="Write docs",
            priority=Priority.MEDIUM,
            created_date="2026-08-13",
        )

        assert task.status == Status.TODO

    def test_task_defaults_to_empty_tags(self):
        """When tags are omitted, they default to an empty list."""
        task = Task(
            id=1,
            title="Write docs",
            priority=Priority.MEDIUM,
            created_date="2026-08-13",
        )

        assert task.tags == []

    def test_task_rejects_id_zero(self):
        """Task id must be greater than zero."""
        with pytest.raises(ValidationError):
            Task(
                id=0,
                title="Invalid task",
                priority=Priority.HIGH,
                created_date="2026-08-13",
            )

    def test_task_rejects_negative_id(self):
        """Task id cannot be negative."""
        with pytest.raises(ValidationError):
            Task(
                id=-5,
                title="Invalid task",
                priority=Priority.HIGH,
                created_date="2026-08-13",
            )

    def test_task_rejects_empty_title(self):
        """Task title cannot be empty."""
        with pytest.raises(ValidationError):
            Task(
                id=1,
                title="",
                priority=Priority.HIGH,
                created_date="2026-08-13",
            )

    def test_task_rejects_too_many_tags(self):
        """Task cannot contain more than ten tags."""
        tags = [
            "tag1",
            "tag2",
            "tag3",
            "tag4",
            "tag5",
            "tag6",
            "tag7",
            "tag8",
            "tag9",
            "tag10",
            "tag11",
        ]

        with pytest.raises(ValidationError):
            Task(
                id=1,
                title="Too many tags",
                priority=Priority.LOW,
                created_date="2026-08-13",
                tags=tags,
            )