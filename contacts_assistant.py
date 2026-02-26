from typing import Final
from address_book import AddressBook, Record

CONTACTS_FILE_NAME: Final = 'contacts.txt'
NOT_FOUND:Final[str] = "Contact {name} not found."
ADDED:Final[str] = "Contact {name} has been added."
UPDATED:Final[str] = "Contact {name} has been updated."

address_book = AddressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone(10 digits) please."
        except KeyError:
            return f"Phone for {args[0][0] if isinstance(args[0], list) else args[0]} not found"
        except IndexError as e:
            return e
    return inner

def input_date_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return e
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = UPDATED.format(name = name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = ADDED.format(name = record.name)
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args,  book: AddressBook):
    name, phone = args
    record = book.find(name)
    message = UPDATED.format(name = name)
    if record is None:
        return NOT_FOUND.format(name = record.name)
    if phone:
        record.add_phone(phone)

    return message

@input_date_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    message = UPDATED.format(name = name)
    if record:
        record.add_birthday(birthday)
        return message
    else: return NOT_FOUND

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        return record.birthday
    else: return NOT_FOUND

@input_error
def print_phone(args, book: AddressBook):
    name, *_ = args
    return f"{name}: {book[name]}"

def upcoming_birthdays(book: AddressBook):
    message = "Birthdays for next week: \n"
    for bd in book.get_upcoming_birthdays():
        message += f"{bd.get('name')}: {bd.get('congratulation_date')}\n"
    return message
    
def print_all(book: AddressBook):
    return book


def main():
    print("Welcome to the assistant bot!")
    while True:
        userInput = input("Enter a command: ")
        command, *arguments = parse_input(userInput)

        match command:
            case 'hello':
                print("How can I help you?")
            case 'add':
                print(add_contact(arguments, address_book))
            case 'change':
                print(change_contact(arguments, address_book))
            case 'phone':
                print(print_phone(arguments, address_book))
            case 'add-birthday':
                print(add_birthday(arguments, address_book))
            case 'show-birthday':
                print(show_birthday(arguments, address_book))
            case 'birthdays':
                print(upcoming_birthdays(address_book))
            case 'all':
                print(print_all(address_book))
            case 'exit' | 'close':
                print("Good bye!")
                break
            case _:
                print(f"Invalid command: {command}")

            


if __name__ == '__main__':
    main()