from models import User, Priority, Status, Task



def main():

    user1 = User(
        id = 1,
        name = "Rahul",
        email = "rahul@gmail.com",
        age = 29,
        is_active = False     
    )

    print(f"User1 name: {user1.name}")
    print(f"User1 email: {user1.email}")

    user2 = User(
        id = 2,
        name = "Pratik",
        email = "pratik@gmail.com",
        age = 30   
    )

    print(f"User2 active status: {user2.is_active}")

    raw_data = {
    "id": 1,
    "title": "Ship the AI feature",
    "priority": "high",
    "status": "in_progress",
    "assignee": {
        "id": 42,
        "name": "Rahul",
        "email": "rahul@example.com",
        "age": 30
    },
    "tags": ["ai", "urgent"]
}
    task = Task(**raw_data)
    
    assert task.assignee is not None
    print(f"Task Assignee: {task.assignee.name}")

    print(task.model_dump())
    print(task.model_dump_json(indent=2))

    try:
        bad_user = User(
            id=-1,
            name="",
            email="rahul@example.com",
            age=200
        )
    except Exception as e:
        print("Caught expected error:")
        print(e)



if __name__ == "__main__":
    main()
