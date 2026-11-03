"""Tests for the TaskTracker class."""

from pathlib import Path

import pytest

from task_tracker.models import Priority, Status
from task_tracker.tracker import TaskTracker


@pytest.fixture
def tracker_path(tmp_path: Path) -> Path:
    """Provide a fresh temporary JSON file path."""
    return tmp_path / "test_tasks.json"


@pytest.fixture
def empty_tracker(tracker_path: Path) -> TaskTracker:
    """Provide a tracker containing no tasks."""
    return TaskTracker(tracker_path)


@pytest.fixture
def populated_tracker(tracker_path: Path) -> TaskTracker:
    """Provide a tracker containing three pre-created tasks."""
    tracker = TaskTracker(tracker_path)

    tracker.add(
        "Write docs",
        Priority.HIGH,
        "2026-08-13",
        ["docs"],
    )

    tracker.add(
        "Review PR",
        Priority.MEDIUM,
        "2026-08-13",
    )

    tracker.add(
        "Fix bug",
        Priority.LOW,
        "2026-08-14",
        ["bug", "urgent"],
    )

    return tracker


class TestTaskTracker:
    """Tests for TaskTracker business logic and persistence."""

    def test_new_tracker_starts_empty(self, empty_tracker):
        """A fresh tracker starts with no tasks."""
        assert empty_tracker.tasks == []

    def test_add_returns_task_with_correct_id(self, empty_tracker):
        """Adding tasks assigns sequential persistent ids."""
        first = empty_tracker.add(
            "First task",
            Priority.HIGH,
            "2026-08-13",
        )

        second = empty_tracker.add(
            "Second task",
            Priority.LOW,
            "2026-08-14",
        )

        assert first.id == 1
        assert second.id == 2

    def test_add_creates_new_id_after_delete(self, populated_tracker):
        """Deleting an id does not cause that id to be reused."""
        deleted = populated_tracker.delete(2)

        assert deleted is True

        new_task = populated_tracker.add(
            "New task",
            Priority.MEDIUM,
            "2026-08-15",
        )

        assert new_task.id == 4

    def test_add_defaults_to_empty_tags(self, empty_tracker):
        """Adding without tags stores an empty list."""
        task = empty_tracker.add(
            "Task without tags",
            Priority.HIGH,
            "2026-08-13",
        )

        assert task.tags == []

    def test_add_persists_to_file(self, tracker_path):
        """Tasks saved by one tracker are loaded by another tracker."""
        tracker1 = TaskTracker(tracker_path)

        tracker1.add(
            "Persistent task",
            Priority.HIGH,
            "2026-08-13",
        )

        tracker2 = TaskTracker(tracker_path)

        assert len(tracker2.tasks) == 1
        assert tracker2.tasks[0].title == "Persistent task"
        assert tracker2.tasks[0].id == 1

    def test_find_by_id_returns_task_when_exists(self, populated_tracker):
        """Finding an existing id returns the matching task."""
        task = populated_tracker.find_by_id(2)

        assert task is not None
        assert task.id == 2
        assert task.title == "Review PR"

    def test_find_by_id_returns_none_when_missing(self, populated_tracker):
        """Finding a nonexistent id returns None."""
        task = populated_tracker.find_by_id(999)

        assert task is None

    def test_update_status_succeeds_for_existing_task(self, populated_tracker):
        """Updating an existing task changes its status."""
        result = populated_tracker.update_status(
            1,
            Status.DONE,
        )

        task = populated_tracker.find_by_id(1)

        assert result is True
        assert task is not None
        assert task.status == Status.DONE

    def test_update_status_returns_false_for_missing_id(
        self,
        populated_tracker,
    ):
        """Updating a nonexistent task returns False."""
        result = populated_tracker.update_status(
            999,
            Status.DONE,
        )

        assert result is False

    def test_update_priority_succeeds_for_existing_task(
        self,
        populated_tracker,
    ):
        """Updating an existing task changes its priority."""
        result = populated_tracker.update_priority(
            3,
            Priority.HIGH,
        )

        task = populated_tracker.find_by_id(3)

        assert result is True
        assert task is not None
        assert task.priority == Priority.HIGH

    def test_update_priority_returns_false_for_missing_id(
        self,
        populated_tracker,
    ):
        """Updating priority for a missing task returns False."""
        result = populated_tracker.update_priority(
            999,
            Priority.HIGH,
        )

        assert result is False

    def test_delete_removes_task_and_returns_true(self, populated_tracker):
        """Deleting an existing task removes it and returns True."""
        result = populated_tracker.delete(2)

        assert result is True
        assert populated_tracker.find_by_id(2) is None
        assert len(populated_tracker.tasks) == 2

    def test_delete_returns_false_for_missing_id(self, populated_tracker):
        """Deleting a nonexistent task returns False."""
        result = populated_tracker.delete(999)

        assert result is False
        assert len(populated_tracker.tasks) == 3

    def test_list_all_sorted_by_priority(self, populated_tracker):
        """Tasks are sorted high, medium, low."""
        tasks = populated_tracker.list_all()

        priorities = [task.priority for task in tasks]

        assert priorities == [
            Priority.HIGH,
            Priority.MEDIUM,
            Priority.LOW,
        ]

    def test_list_all_sorts_same_priority_by_id(self, empty_tracker):
        """Tasks with the same priority are ordered by ascending id."""
        empty_tracker.add(
            "First",
            Priority.HIGH,
            "2026-08-13",
        )

        empty_tracker.add(
            "Second",
            Priority.HIGH,
            "2026-08-13",
        )

        empty_tracker.add(
            "Third",
            Priority.HIGH,
            "2026-08-13",
        )

        tasks = empty_tracker.list_all()

        ids = [task.id for task in tasks]

        assert ids == [1, 2, 3]

    def test_filter_by_status(self, populated_tracker):
        """Filtering by TODO returns only TODO tasks."""
        results = populated_tracker.filter_by_status(
            Status.TODO
        )

        assert len(results) == 3

        for task in results:
            assert task.status == Status.TODO

    def test_filter_by_priority(self, populated_tracker):
        """Filtering by HIGH returns only high-priority tasks."""
        results = populated_tracker.filter_by_priority(
            Priority.HIGH
        )

        assert len(results) == 1
        assert results[0].title == "Write docs"
        assert results[0].priority == Priority.HIGH

    def test_search_by_title_is_case_insensitive(
        self,
        populated_tracker,
    ):
        """Title searching ignores letter case."""
        results = populated_tracker.search_by_title("REVIEW")

        assert len(results) == 1
        assert results[0].title == "Review PR"

    def test_search_by_title_returns_empty_when_no_match(
        self,
        populated_tracker,
    ):
        """Title search returns an empty list when nothing matches."""
        results = populated_tracker.search_by_title("banana")

        assert results == []

    def test_filter_by_tag_is_case_insensitive(
        self,
        populated_tracker,
    ):
        """Tag filtering ignores letter case."""
        results = populated_tracker.filter_by_tag("URGENT")

        assert len(results) == 1
        assert results[0].title == "Fix bug"

    def test_filter_by_tag_returns_empty_when_missing(
        self,
        populated_tracker,
    ):
        """Filtering for an unused tag returns an empty list."""
        results = populated_tracker.filter_by_tag("finance")

        assert results == []

    def test_stats_with_empty_tracker(self, empty_tracker):
        """Empty tracker statistics contain zeros."""
        stats = empty_tracker.stats()

        assert stats["total"] == 0
        assert stats["percent_done"] == 0.00
        assert stats["unique_tags"] == 0

        assert stats["by_status"] == {
            "todo": 0,
            "in_progress": 0,
            "done": 0,
        }

        assert stats["by_priority"] == {
            "low": 0,
            "medium": 0,
            "high": 0,
        }

    def test_stats_counts_correctly(self, populated_tracker):
        """Statistics correctly count tasks, categories, and tags."""
        populated_tracker.update_status(
            1,
            Status.DONE,
        )

        populated_tracker.update_status(
            2,
            Status.IN_PROGRESS,
        )

        stats = populated_tracker.stats()

        assert stats["total"] == 3

        assert stats["by_status"] == {
            "todo": 1,
            "in_progress": 1,
            "done": 1,
        }

        assert stats["by_priority"] == {
            "low": 1,
            "medium": 1,
            "high": 1,
        }

        assert stats["percent_done"] == pytest.approx(
            33.33,
            abs=0.01,
        )

        assert stats["unique_tags"] == 3