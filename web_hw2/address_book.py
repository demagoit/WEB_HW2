'''
CLI Phone book assistant.
'''
from collections import UserDict
import datetime
import json
from re import match

class UserExists(Exception):
    # (f'User {name} already exists.')
    pass

class WrongName(Exception):
# (f'Name should start with letter and contain only letters and digits - "{value}" given.')
    pass

class WrongPhone(Exception):
    # (f'Phone should have only digits and be at least 10 digits long - "{value}" given.')
    pass

class ExistsPhone(Exception):
    pass

class NotExistsPhone(Exception):
    # (f'Phone "{phone}" not found for contact "{self.name}".')
    # (f'Phone "{old_phone}" not found for contact "{self.name}".')
    pass

class WrongBirthday(Exception):
    # (f'Birthday expected in format: YYYY-MM-DD, instead "{value}" given.')
    pass

class ExistsBirthday(Exception):
    pass

class WrongMemo(Exception):
    pass

class ExistsMemo(Exception):
    pass


class WrongAddress(Exception):
    pass

class ExistsAddress(Exception):
    pass


class WrongEmail(Exception):
    pass

class ExistsEmail(Exception):
    pass

PARAM_NAMES = ['name', 'phones', 'birthday', 'emails', 'address', 'memos']

class Field:
    '''
    Basic class for all fields in Record
    '''

    def __init__(self):
        self.__value = None

    def __str__(self):
        return str(self.__value)  

    def __repr__(self):
        return str(self.__value)


class Birthday(Field):
    '''
    Birthday field. Only one value possible.
    '''

    def __init__(self, value = None):
        super().__init__()
        self.value = value

    @property
    def value(self):
        return self._Field__value

    @value.setter
    def value(self, value):
        if not value:
            self.delete()
        self.add(value)

    def __is_valid(self, value):
            try:
                datetime.date.fromisoformat(value)
                return True
            except ValueError:
                raise WrongBirthday
            
    def add(self, value):
        if self._Field__value:
            raise ExistsBirthday
        if self.__is_valid(value):
            self._Field__value = datetime.date.fromisoformat(value)

    def change(self, value):
        self._Field__value = None
        self.add(value)

    def delete(self):
        self._Field__value = None
        remove_object = True
        return remove_object


class Name(Field):
    '''
    Class for Record Name
    '''

    def __init__(self, value):
        super().__init__()
        self.value = value

    @property
    def value(self):
        return self._Field__value

    @value.setter
    def value(self, value):
        if not value.isidentifier():
            raise WrongName
        if (len(value) == 0) | (value is None):
            raise WrongName
        self._Field__value = value


class Phone(Field):
    '''
    Class for Phone field. Have value validation. Can have multiple values.
    '''

    def __init__(self, *value):
        super().__init__()
        self.value = value

    @property
    def value(self):
        return self._Field__value

    @value.setter
    def value(self, values):
        if not values:
            self._Field__value = None
            return
        if not self._Field__value:
            self._Field__value = []
        
        self.add(*values)

    def __is_valid(self, phone):
            if not phone.isdigit():
                raise WrongPhone
            if len(phone) != 10:
                raise WrongPhone
            return True
 
    def add(self, *phones):
        for phone in phones:
            if self.__is_valid(phone):
                self._Field__value.append(phone)

    def change(self, old_phone, new_phone):

        for item in self._Field__value:
            if item == old_phone:
                self._Field__value.insert(
                    self._Field__value.index(item), new_phone)
                self._Field__value.remove(item)
                return
        raise NotExistsPhone

    def delete(self, phone):
        remove_object = False
        if phone in self.value:
            self.value.remove(phone)
        if len(self.value) == 0:
            remove_object = True
        return remove_object

    def __str__(self):
        return ', '.join(self._Field__value)

    def __repr__(self):
        return str(self._Field__value)


class Memo(Field):
    '''Class for Memo field. Have value validation. Can have multiple values.'''
    def __init__(self, *memo_text):
        super().__init__()
        self.value = memo_text

    @property
    def value(self):
        return self._Field__value

    @value.setter
    def value(self, values):
        if not values:
            self._Field__value = None
            return
        if not self._Field__value:
            self._Field__value = []

        self.add(*values)

    def __is_valid(self, memo_text):
            if not memo_text.isprintable():
                raise WrongMemo
            if len(memo_text) > 240:
                raise WrongMemo
            return True

    def add(self, *memo_text):
        for item in memo_text:
            if self.__is_valid(item):
                self._Field__value.append(item)

    def change(self, old_memo_text, new_memo_text):

        for item in self._Field__value:
            if item == old_memo_text:
                self._Field__value.insert(
                    self._Field__value.index(item), new_memo_text)
                self._Field__value.remove(item)
                return
        raise WrongMemo

    def delete(self, memo_text):
        remove_object = False
        if memo_text in self.value:
            self.value.remove(memo_text)
        if len(self.value) == 0:
            remove_object = True
        return remove_object

    def __str__(self):
        return ', '.join(self._Field__value)

    def __repr__(self):
        return str(self._Field__value)


class Address(Field):
    '''Class for Address field. Have value validation. Can have multiple values.'''
    def __init__(self, *values):
        super().__init__()
        self.value = values

    @property
    def value(self):
        return self._Field__value

    @value.setter
    def value(self, values):
        if not values:
            self._Field__value = None
            return
        if not self._Field__value:
            self._Field__value = []

        self.add(*values)

    def __is_valid(self, value):
            if not value.isprintable():
                raise WrongAddress
            if len(value) > 100:
                raise WrongAddress
            return True

    def add(self, *values):
        for item in values:
            if self.__is_valid(item):
                self._Field__value.append(item)

    def change(self, old_value, new_value):

        for item in self._Field__value:
            if item == old_value:
                self._Field__value.insert(
                    self._Field__value.index(item), new_value)
                self._Field__value.remove(item)
                return
        raise WrongAddress

    def delete(self, value):
        remove_object = False
        if value in self.value:
            self.value.remove(value)
        if len(self.value) == 0:
            remove_object = True
        return remove_object

    def __str__(self):
        return ', '.join(self._Field__value)

    def __repr__(self):
        return str(self._Field__value)


class Email(Field):
    '''Class for E-mail field. Have value validation. Can have multiple values.'''
    def __init__(self, *values):
        super().__init__()
        self.value = values

    @property
    def value(self):
        return self._Field__value

    @value.setter
    def value(self, values):
        if not values:
            self._Field__value = None
            return
        if not self._Field__value:
            self._Field__value = []

        self.add(*values)

    def __is_valid(self, value):
        if match(r"[a-zA-Z0-9]+[\w\-]+[\.]?[a-zA-Z\w\-]+[@]{1}[a-z]+[\.]{1}[a-z]{2,}", value) == None:
            raise WrongEmail
        return True

    def add(self, *values):
        for item in values:
            if self.__is_valid(item):
                self._Field__value.append(item)

    def change(self, old_value, new_value):

        for item in self._Field__value:
            if item == old_value:
                self._Field__value.insert(
                    self._Field__value.index(item), new_value)
                self._Field__value.remove(item)
                return
        raise WrongEmail

    def delete(self, value):
        remove_object = False
        if value in self.value:
            self.value.remove(value)
        if len(self.value) == 0:
            remove_object = True
        return remove_object

    def __str__(self):
        return ', '.join(self._Field__value)

    def __repr__(self):
        return str(self._Field__value)


class Record():
    '''
    Class for storing each contact record. Have methods to add/delete/change each field.
    '''

    def __init__(self, name: str, phones=None, birthday=None, emails=None, memos=None, address=None):
        self.__name = None
        self.__phones = None
        self.__birthday = None
        self.__emails = None
        self.__memos = None
        self.__address = None
        self.name = name
        self.phones = phones
        self.birthday = birthday
        self.emails = emails
        self.memos = memos
        self.address = address

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = Name(value)

    @property
    def phones(self):
        return self.__phones
    
    @phones.setter
    def phones(self, value):
        if value:
            value=[value] if isinstance(value, str) else value
            if self.__phones:
                self.__phones.add(*value)
            else:
                self.__phones = Phone(*value)
    
    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, value):
        if value:
            if self.__birthday:
                raise ExistsBirthday
            self.__birthday = Birthday(value)

    @property
    def emails(self):
        return self.__emails

    @emails.setter
    def emails(self, value):
        # self.__emails = Email(value)
        if value:
            value = [value] if isinstance(value, str) else value
            if self.__emails:
                self.__emails.add(*value)
            else:
                self.__emails = Email(*value)

    @property
    def memos(self):
        return self.__memos

    @memos.setter
    def memos(self, value):
        if value:
            value=[value] if isinstance(value, str) else value
            if self.__memos:
                self.__memos.add(*value)
            else:
                self.__memos = Memo(*value)

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        if value:
            value = [value] if isinstance(value, str) else value
            if self.__address:
                self.__address.add(*value)
            else:
                self.__address = Address(*value)

    def add_phone(self, value):
        '''додавання об'єктів'''
        self.phones = value

    def delete_phone(self, value: str):
        '''видалення об'єктів'''
        if self.phones.delete(value):
            self.phones= None

    def edit_phone(self, old_phone: str, new_phone: str):
        '''редагування об'єктів'''
        self.phones.change(old_phone, new_phone)

    def find_phone(self, pattern):
        for item in self.__phones.value:
            pattern_match = item.lower().find(pattern.lower())
            if pattern_match != -1:
                return item
        return None

    def add_birthday(self, value):
        self.birthday = value

    def delete_birthday(self):
        self.__birthday = None

    def edit_birthday(self, value: str):
        '''редагування об'єктів'''
        self.birthday.change(value)

    def days_to_birthday(self):
        '''
        метод days_to_birthday, який повертає кількість днів до наступного дня народження контакту,
        якщо день народження заданий.
        '''

        if not self.birthday:
            days_to_bd = None
        else:
            td = datetime.date.today()
            obd = datetime.date.fromisoformat(str(self.birthday))
            bd = datetime.date(td.year, obd.month, obd.day)

            if td <= bd:
                days_to_bd = (bd - td).days
            else:
                days_to_bd = (datetime.date(
                    bd.year + 1, bd.month, bd.day) - td).days

        return days_to_bd
    
    def add_email(self, value):
        # if self.emails.value:
        #     raise ExistsEmail
        # self.emails = Email(email)
        self.emails = value
    
    def delete_email(self, value):
        if self.emails.delete(value):
            self.emails = None

    def edit_email(self, old_value: str, new_value: str):
        '''редагування об'єктів'''
        self.emails.change(old_value, new_value)

    def add_memo(self, value):
        self.memos = value

    def delete_memo(self, value):
        if self.memos.delete(value):
            self.memos = None

    def edit_memo(self, old_value: str, new_value: str):
        '''редагування об'єктів'''
        self.memos.change(old_value, new_value)

    def add_address(self, value):
        self.address = value

    def delete_address(self, value):
        if self.address.delete(value):
            self.address = None

    def edit_address(self, old_value: str, new_value: str):
        '''редагування об'єктів'''
        self.address.change(old_value, new_value)

    def __str__(self):
        return f'Contact name: {self.name}, birthday {self.birthday}, phones: {self.phones}'

    def __repr__(self):
        return f'Record: {self.__name}'


class AddressBook(UserDict):
    '''
    Class to store all records. Have methods to add/delete/change/find records.
    '''

    def __init__(self):
        super().__init__()
        self.__n = 10  # records per printed sheet

    @property
    def rec_per_page(self):
        '''records per printed sheet'''
        return self.__n

    @rec_per_page.setter
    def rec_per_page(self, value: str):
        try:
            self.__n = int(value)
        except:
            raise ValueError("Number per page shold be integer.")

    def add_record(self, contact: Record):
        '''додає запис до self.data.'''
        name = str(contact.name)
        if name in self.data.keys():
            raise UserExists
        
        self.data[name] = contact

    def find_pattern(self, pattern: str, field = None):
        '''Search records by pattern'''
        rec_search_fields = PARAM_NAMES

        if len(pattern) == 0:
            return None

        if field:
            if field in rec_search_fields:
                search_fields = [field]
            else:
                raise KeyError('Wrong argument')
        else:
            search_fields = rec_search_fields

        match_list = []

        for name in self.data.keys():
            record = self.data.get(name)
            for attr in search_fields:
                obj = getattr(record, attr, None)
                if not obj:
                    continue
                elif isinstance(obj, str) or isinstance(obj.value, str):
                    pattern_match = obj.value.lower().find(pattern.lower())
                    if pattern_match != -1:
                        match_list.append(record)
                else:
                    for item in obj.value:
                        pattern_match = item.lower().find(pattern.lower())
                        if pattern_match != -1:
                            match_list.append(record)
                            continue
        return match_list

    def find(self, name: str):
        '''Search records by Name'''
        if name in self.data.keys():
            return self.data.get(name)
        return None

    def find_records_for_birthday(self, qua_days):
        '''find records with birthdays in given period'''
        list_rec = []
        for records in self.data.values():
            delta_day = records.days_to_birthday()
            if delta_day != None and delta_day <= qua_days:
                list_rec.append(records)
        return list_rec
    
    def delete(self, name: str):
        if name in self.data.keys():
            self.data.pop(name)
        else:
            raise WrongName

    def save_JSON(self, filename='phonebook.json'):
        with open(filename, 'w') as fh:
            json.dump(self, fh, indent=4, cls=BookEncoder)

    def load_JSON(self, filename='phonebook.json'):
        with open(filename, 'r') as fh:
            input = json.load(fh)

        for item in input.keys():
            fields = input.get(item)
            rec = Record(**fields)
            self.add_record(rec)

    def __iter__(self):
        return AddressBookItterator(self)


class AddressBookItterator(UserDict):
    def __init__(self, adr_book: AddressBook):
        self.data = adr_book.data
        self.__n = adr_book.rec_per_page  # records per printed sheet
        self.__current_index = 0
        self.__records = list(self.data.keys())
        self.__records.sort()

    def __next__(self):

        output = ''
        for _ in range(self.__n):
            if self.__current_index < len(self.__records):
                record = self.data.get(self.__records[self.__current_index])
                output += str(record) + '\n'
                self.__current_index += 1
            else:
                break

        if output:
            return output

        raise StopIteration


# subclass JSONEncoder
# https://pynative.com/make-python-class-json-serializable/
class BookEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            out = str(obj)
        elif 'data' in obj.__dict__:
            out = obj.__dict__.get("data")
        elif isinstance(obj, Record):
            out = obj.__dict__
            out = {key.split('__')[1]: value for key, value in out.items()}
        else:
            out = obj.value
        return out


# class BookDencoder(json.JSONDecoder):
#     def default(self, obj):
#         out = obj.__dict__
#         for item in out.keys():
#             phones = item.get('phones')
#             out[item] = Record(item.get('name'), item.get('birthday'))
#             for phone in phones:
#                 out[item].add_phone(phone)
#         return out
    
    # csv and pickle serialisation, CLI, pypi package 