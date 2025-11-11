from adress_book import AddressBook, Record, Birthday
import pickle


def parse_input(user_input):
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e) if str(e) else "Enter the argument for the command"
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command."
        except AttributeError:
            return "Contact not found."
    return inner


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def phone_contact(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    return "; ".join([phone.value for phone in record.phones])


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    record.birthday = Birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    return "Birthday not found."


@input_error
def birthdays(args, book: AddressBook):
    return book.get_upcoming_birthdays()


@input_error
def all_contacts(book: AddressBook):
    result = []
    for name, record in book.data.items():
        phones = "; ".join([phone.value for phone in record.phones])
        bday = (record.birthday.value.strftime("%d.%m.%Y")
                if record.birthday else "Not set")
        result.append(f"{name}: {phones}, Birthday: {bday}")
    return "\n".join(result)


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if not command:
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(phone_contact(args, book))
        elif command == "all":
            print(all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")
    save_data(book)


if __name__ == "__main__":
    main()
