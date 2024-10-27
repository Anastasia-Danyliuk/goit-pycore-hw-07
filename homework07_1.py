from collections import UserDict
from datetime import datetime, timedelta



class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if len(value) == 10:
            super().__init__(value)
        else:
            raise ValueError("Phone number must be at least 10 digits")

class Birthday(Field):
    def __init__(self, value):
        try:
            user_birthday = datetime.strptime(value, "%Y.%m.%d").date()
            super().__init__(user_birthday)
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY.MM.DD")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def delete_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def find_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                return phone

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self):
        current_day = datetime.today().date()
        last_greeting_day = current_day + timedelta(days=7)
        upcoming_birthdays = []
        for record in self.data.values():
            user_birthday = record.birthday.value
            user_bd_greeting = user_birthday.replace(year=current_day.year)
            if user_bd_greeting < current_day:
                user_bd_greeting = user_birthday.replace(year=current_day.year + 1)
            if last_greeting_day >= user_bd_greeting >= current_day:
                if user_bd_greeting.weekday() == 5:
                    user_bd_greeting = user_bd_greeting + timedelta(days=2)
                elif user_bd_greeting.weekday() == 6:
                    user_bd_greeting = user_bd_greeting + timedelta(days=1)
                upcoming_birthdays.append(
                    {"name": record.name.value, "greeting_day": user_bd_greeting.strftime("%Y.%m.%d")})
        return upcoming_birthdays

def main():

    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("0987654321")
    john_record.add_phone("5555555555")
    john_record.delete_phone("0987654321")
    john_record.add_birthday("1999.01.13")

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)
    jane_record.add_birthday("1999.11.03")

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    # book.delete("Jane")


    for name, record in book.data.items():
        print(record)

    upcoming_birthdays = book.get_upcoming_birthdays()
    print("Список привітань на цьому тижні:", upcoming_birthdays)

if __name__ == "__main__":
    main()