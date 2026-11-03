import pytest
from shopping_list import ShoppingList

@pytest.fixture
def empty_list():
    """A fresh, empty ShoppingList for each test."""
    return ShoppingList()


@pytest.fixture
def populate_list():
    """A ShoppingList with three items: milk, eggs, bread."""
    shopping = ShoppingList()
    shopping.add("milk")
    shopping.add("eggs")
    shopping.add("bread")
    return shopping

def test_new_list_is_empty(empty_list):
    assert empty_list.is_empty()

def test_add_single_item(empty_list):
    empty_list.add("milk")
    assert len(empty_list.items) == 1

def test_add_multiple_items(empty_list):
    empty_list.add("milk")
    empty_list.add("eggs")
    empty_list.add("bread")
    assert empty_list.items == ["milk", "eggs", "bread"]

def test_add_strips_whitespace(empty_list):
    empty_list.add("  milk  ")
    assert "milk" in empty_list.items

def test_add_empty_string_does_not_add(empty_list):
    empty_list.add("")
    assert empty_list.is_empty()

def test_add_only_whitespace_does_not_add(empty_list):
    empty_list.add("   ")
    assert empty_list.is_empty()

def test_remove_existing_item_returns_true(populate_list):
    assert populate_list.remove("eggs")

def test_remove_existing_item_removes_it(populate_list):
    populate_list.remove("eggs")
    assert "eggs" not in populate_list.items

def test_remove_missing_item_returns_false(populate_list):
    assert not populate_list.remove("butter")

def test_remove_from_empty_list_returns_false(empty_list):
    assert not empty_list.remove("Tea")

def test_is_empty_after_clear(populate_list):
    populate_list.clear()
    assert populate_list.is_empty()

@pytest.mark.parametrize("items_to_add, expected_empty", [
    ([], True),
    (["milk"], False),
    (["milk", "eggs"], False),
])
def test_is_empty_various_states(items_to_add, expected_empty):
    shopping = ShoppingList()
    for item in items_to_add:
        shopping.add(item)
    assert shopping.is_empty() == expected_empty
