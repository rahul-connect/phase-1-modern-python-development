from greetings.formal import formal_greeting, formal_farewell
from greetings.casual import casual_greeting, casual_farewell


def get_required_field(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value == "":
            print("Field is required")
        else:
            return value
        
def get_preference(prompt: str) -> str | None:
    while True:
        value = input(prompt).strip()
        if value == "":
            print("Field is required")
        elif value.lower() == "formal" or value.lower() == "casual":
            return value
        else:
            print("Sorry, I don't know that style")
            return None

def print_greetings(name: str, preference: str) -> None:
    if preference == "formal":
        print(formal_greeting(name))
        print(formal_farewell(name))
    else:
        print(casual_greeting(name))
        print(casual_farewell(name))



def main():
    name = get_required_field("Enter your name: ")
    preference = get_preference("Enter preference (formal or casual): ")
    if preference is not None:
        print_greetings(name,preference)



if __name__ == "__main__":
    main()
