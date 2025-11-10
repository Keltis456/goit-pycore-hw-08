from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)

    @staticmethod
    def validate(value):
        # Перевірка на 10 цифр
        return value.isdigit() and len(value) == 10


class Birthday(Field):
    def __init__(self, value):
        try:
            super().__init__(datetime.strptime(value, "%d.%m.%Y"))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        # Додавання телефону
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        # Видалення телефону
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone {phone} not found")

    def edit_phone(self, old_phone, new_phone):
        # Редагування телефону
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            # Валідуємо новий номер через створення Phone об'єкту
            new_phone_obj = Phone(new_phone)
            # Знаходимо індекс старого телефону і замінюємо його
            index = self.phones.index(phone_to_edit)
            self.phones[index] = new_phone_obj
        else:
            raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone):
        # Пошук телефону
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        # Додавання запису до self.data
        self.data[record.name.value] = record

    def find(self, name) -> Record:
        # Знаходження запису за ім'ям
        record = self.data.get(name)
        if record:
            return record

    def delete(self, name):
        # Видалення запису за ім'ям
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today()
        current_year = today.year
        upcoming = []
        for user in self.data.values():
            # Skip users without birthday
            if user.birthday is None:
                continue
            # Parse the birthday string to a datetime object
            bday = user.birthday.value
            # Set the birthday to this year
            bday_this_year = bday.replace(year=current_year)
            # If birthday already passed this year, set to next year
            if bday_this_year.date() < today.date():
                bday_for_this_year = bday.replace(year=current_year + 1)
            else:
                bday_for_this_year = bday_this_year

            days_until = (bday_for_this_year.date() - today.date()).days
            if 0 <= days_until < 7:
                # Check if birthday falls on weekend
                if bday_for_this_year.weekday() == 5:  # Saturday
                    # Shift to Monday
                    congratulations_date = bday_for_this_year.replace(
                        day=(bday_for_this_year.day + 2))
                elif bday_for_this_year.weekday() == 6:  # Sunday
                    # Shift to Monday
                    congratulations_date = bday_for_this_year.replace(
                        day=(bday_for_this_year.day + 1))
                else:
                    congratulations_date = bday_for_this_year
                upcoming.append({
                    "name": user.name.value,
                    "congratulation_date":
                        congratulations_date.strftime("%Y.%m.%d")
                })
        return upcoming
