class ShoppingList:
    """A shopping list that lets you add, remove, and view items."""
    
    def __init__(self):
        """Initialize with an empty list."""
        self.items: list[str] = []
    
    def add(self, item: str) -> None:
        """Add an item to the list. Skip if empty."""
        validate_item = item.strip()
        if validate_item == "":
            print("Item cannot be empty")
        else:
            self.items.append(item)
            print(f"{validate_item} added successfully")
    
    def remove(self, item: str) -> bool:
        """Remove an item if it exists. Return True if removed, False if not found."""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def show(self) -> None:
        """Print the list, or 'List is empty' if empty."""
        if not self.items:
            print("List is empty")
        else:
            for index,item in enumerate(self.items):
                print(f"{index+1}. {item}")
    
    def is_empty(self) -> bool:
        """Return True if the list has no items."""
        return not self.items
    
    def __str__(self) -> str:
        """Return a string representation of the list."""
        if self.is_empty():
            return "ShoppingList (empty)"

        return f"ShoppingList with {len(self.items)} items"

    def clear(self) -> None:
         """Remove all items from the list."""
         self.items.clear()
         self.show()



if __name__ == "__main__":
    shopping = ShoppingList()
    print(shopping)
    shopping.add("milk")
    shopping.add("eggs")
    shopping.add("bread")
    shopping.show()
    print(shopping)
    remove_butter = shopping.remove("butter")
    if remove_butter:
        print("Butter is removed successfully")
    else:
        print("Butter is not in the list or already deleted")

    remove_eggs = shopping.remove("eggs")
    if remove_eggs:
        print("Eggs is removed successfully")
    else:
        print("Eggs are not in the list or already deleted")

    shopping.show()
    print(shopping.is_empty())
    shopping.clear()
    print(shopping.is_empty())
    