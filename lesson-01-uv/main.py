from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int


def main():
    user = User(name="Rahul", age=30)
    print(user)
    print(f"Name: {user.name}, Age: {user.age}")


if __name__ == "__main__":
    main()