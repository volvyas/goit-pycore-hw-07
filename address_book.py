from collections import UserDict
from datetime import datetime as dt, timedelta as td, date as d
from typing import Final

DATE_FORMAT: Final =  '%d.%m.%Y'

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    
class Birthday(Field):
    def __init__(self, value):
        self.value = dt.strptime(value, DATE_FORMAT)
        
    def __str__(self):
        return dt.strftime(self.value, DATE_FORMAT)


class Name(Field):
    def __init__(self, value):
        if(value is None or len(value) == 0):
             raise ValueError('Name cannot be null or empty')
        self.value = value
	

class Phone(Field):
    def __init__(self, value):
        self.__check_len__(value)
        self.value = value

    @staticmethod
    def __check_len__(phone):
        if(len(phone) < 10 or not phone.isdigit()):
            raise ValueError('Phone number must have at least 10 digits')

    def __str__(self):
        return f"{self.value}"
          

class Record:
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []
        self.__birthday = birthday

    @property #readonly, usually people do not born twice
    def birthday(self):
        return self.__birthday

    def add_birthday(self, date: str):
        self.__birthday = Birthday(date)

    def find_phone(self, phone):
        phones = list(filter(lambda ph: ph == phone, self.phones))
        if(len(phones)>0): return phones[0]
        else: return None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)
        
    def remove_phone(self, phone):
        existing_phone = self.find_phone(phone)
        if(existing_phone != None):
            self.phones.remove(existing_phone)

    def edit_phone(self, old_phone, new_phone):
        existing_phone = self.find_phone(old_phone)
        if(existing_phone != None):
            existing_phone.set(new_phone)

    def get_phones(self):
        return "; ".join(p.value for p in self.phones)

    def __str__(self):
        return f"Contact name: {self.name.value}, {'' if self.birthday is None else 'Birthday: ' + self.birthday.__str__() + ', '}Phones: {self.get_phones()}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value.lower()] = record

    def find(self, name: str) -> Record:
        return self.data.get(name.lower())
    
    def delete(self, name):
        self.data.pop(name.lower())

    def __str__(self):
        records_l = ['Address book:']
        for value in self.data.values():
            records_l.append(f"{value}")
        return "\n\t".join(records_l);

    def get_upcoming_birthdays(self):
        current_date = dt.today().date()
        result_list = []

        def get_congrats_date_from_record(record):
            birthday_date = record.birthday.value
            congrats_date = d(current_date.year, birthday_date.month, birthday_date.day)
            return congrats_date
        def get_working_day(date): return date + td(days=7-date.weekday()) if(date.weekday() in [5,6]) else date

        for record in self.data.values():
            if record.birthday is None:
                continue
            congrats_date = get_congrats_date_from_record(record)
            days_diff = congrats_date - current_date
            if(congrats_date < current_date): continue

            if(days_diff.days <= 7):
                congrats_date = get_working_day(congrats_date)
                result_list.append({'name': record.name.value, 'congratulation_date': congrats_date.strftime(DATE_FORMAT)})

        return result_list