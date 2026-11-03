

def greet(name: str) -> str:
    """Return the greeting message with the name"""
    return f"Hello, {name}! Welcome"

def is_valid_age(age: int) -> bool:
    """Checks if age is valid or return false"""
    if 0 <= age <= 120:
        return True
    return False

def calculate_tip(bill: float, percent: float = 15.0) -> float:
    """Calculate and return the tip amount"""
    return bill * (percent / 100)
   

def safe_divide(a: float, b: float) -> float | None:
    """Check if number is divisible or not"""
    if b != 0:
        return a / b
    return None

def count_items_by_status(items: list[dict], status: str) -> int:
    """Return the counts of a given status in the items"""
    status_count = 0

    for item in items:
        if item['status'] == status:
            status_count += 1

    return status_count

if __name__ == "__main__":
    print(greet("Rahul"))
    print(is_valid_age(30))
    print(is_valid_age(200))
    print(calculate_tip(500))
    print(calculate_tip(500, 20))
    print(safe_divide(10, 2))
    print(safe_divide(10, 0))
    print(safe_divide(10, -2))
    
    items = [
        {"status": "todo"},
        {"status": "done"},
        {"status": "todo"},
        {"status": "in_progress"},
    ]
    print(count_items_by_status(items, "todo"))