from abc import abstractclassmethod, ABC

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.table import Table

import address_book as book

class Input(ABC):
    @abstractclassmethod
    def get_input(self):
        pass


class Output(ABC):
    @abstractclassmethod
    def user_output(self, data):
        pass


class CLI_Input(Input):
        
    __PROMPTS = {'command_prompt': 'Please enter your command: ',

               'search_prompt_pattern': 'Enter a pattern to search: ',
               'search_prompt_scope': 'Enter field to search (or enter to search everywhere): ',

               'user_name_prompt': 'Enter contact name: ',
               'user_del_prompt': 'Enter contact name to delete: ',

               'phone_prompt': 'Enter phone number: ',
               'phone_del_prompt': 'Enter phone to delete: ',
               'old_phone_prompt': 'Enter old phone number: ',
               'new_phone_prompt': 'Enter new phone number: ',

               'birthday_prompt': 'Enter birthday(yyyy-mm-dd): ',
               'birthday_search_prompt': 'Enter quantity of days: ',

               'email_prompt': 'Enter email: ',
               'email_del_prompt': 'Enter e-mail to delete: ',
               'old_email_prompt': 'Enter old e-mail: ',
               'new_email_prompt': 'Enter new e-mail: ',

               'address_prompt': 'Enter address: ',
               'address_del_prompt': 'Enter address to delete: ',
               'old_address_prompt': 'Enter old address: ',
               'new_address_prompt': 'Enter new address: ',

               'memo_prompt': 'Enter memo: ',
               'memo_del_prompt': 'Enter memo to delete: ',
               'old_memo_prompt': 'Enter old memo: ',
               'new_memo_prompt': 'Enter new memo: '
               }

    def __init__(self, my_book):
        self.__book = my_book
        self.__NAME_COMMANDS = {

        'help': self.__help,
        'hello': self.__hello,
        'show-all': self.__show_all,
        'close': self.__exit,
        'exit': self.__exit,

        'user-add': self.__add_user,
        'user-find': self.__find_user,
        'user-delete': self.__delete_user,
        'pattern-find': self.__find_pattern,

        'phone-add': self.__add_phone,
        'phone-delete': self.__delete_phone,
        'phone-replace': self.__change_phone,

        'birthday-add': self.__add_birthday,
        'birthday-delete': self.__delete_birthday,
        'birthday-replace': self.__replace_birthday,
        'birthday-next': self.__next_birthday,
        'birthday-find': self.__find_birthday,

        'email-add': self.__add_email,
        'email-delete': self.__delete_email,
        'email-replace': self.__replace_email,

        'memo-add': self.__add_memo,
        'memo-delete': self.__delete_memo,
        'memo-replace': self.__replace_memo,

        'address-add': self.__add_addr,
        'address-delete': self.__delete_addr,
        'address-replace': self.__replace_addr
    }


    def __hello(self):
        return ('How can I help you?', 'normal')

    def __help(self):
        help_list = [
            ['Command', 'Description'], #header
            ['help', 'command description'],
            ['hello', 'greets the user'],
            ['show-all', 'show all records in the book'],
            ['close | exit', 'for exit'],

            ['user-add', 'add new user'],
            ['user-find', 'find user by name'],
            ['user-delete', 'delete user from address book'],
            ['pattern-find', 'find given pattern in user`s record fields'],

            ['phone-add', 'add phone to existing user'],
            ['phone-delete', 'delete phone from user'],
            ['phone-replace', 'chandge user`s phone'],

            ['birthday-add', 'add birthday to existing user'],
            ['birthday-delete', 'delete birthday from existing user'],
            ['birthday-replace', 'chandge user`s birthday'],
            ['birthday-next',
                'shows the number of days until the user`s next birthday'],
            ['birthday-find',
                'displaying a list of users with birthdays in given number of days'],

            ['email-add', 'add e-mail to user'],
            ['email-delete', 'delete e-mail from user'],
            ['email-replace', 'replace existing user`s e-mail with new'],

            ['memo-add',
                'add memo to user (max.240 printable characters)'],
            ['memo-delete', 'delete memo from user'],
            ['memo-replace',
                'replace existing user`s memo with new text'],

            ['address-add',
                'add address to user (max.100 printable characters)'],
            ['address-delete', 'delete address from user'],
            ['address-replace',
                'replace existing user`s address with new text']
        ]
        return (help_list, 'table')

    def __show_all(self):
        if self.__book:
            return (self.__book, 'table')
        return ('No users found', 'warning')

    def __exit(self):
        return ('Good bye!', 'normal')

    def __add_user(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        phone = input(self.__PROMPTS.get('phone_prompt'))
        birthday = input(self.__PROMPTS.get('birthday_prompt'))
        email = input(self.__PROMPTS.get('email_prompt'))
        address = input(self.__PROMPTS.get('address_prompt'))
        memo = input(self.__PROMPTS.get('memo_prompt'))
        user_input_list = [name, phone, birthday, email, address, memo]

        if name == '':
            return ('Enter the name please', 'critical')

        phone = self.__book.find_pattern(phone, 'phones')
        record = self.__book.find(name)
        if record:
            return ('User already exists.', 'warning')
        elif phone:
            return ('Phone exist', 'warning')
        else:
            param_names = book.PARAM_NAMES
            rec_data = {param_names[i]: user_input_list[i]
                        for i in range(len(param_names))}
            record = book.Record(**rec_data)

        self.__book.add_record(record)
        
        return (f'User {name} successfully added.', 'normal')

    def __delete_user(self):
        name = input(self.__PROMPTS.get('user_del_prompt')).capitalize()

        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'warning')
        self.__book.delete(name)
        
        return (f'User {name} successfully deleted.', 'normal')

    def __find_user(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()

        list_rec = self.__book.find(name)
        if list_rec:
            ret_book = book.AddressBook()
            ret_book.rec_per_page = self.__book.rec_per_page
            ret_book.add_record(list_rec)
            return (ret_book, 'table')
        return (f'User {name} not found.', 'warning')

    def __find_pattern(self):
        value = input(self.__PROMPTS.get('search_prompt_pattern'))
        scope = input(self.__PROMPTS.get('search_prompt_scope'))

        list_rec = self.__book.find_pattern(value, scope)
        if len(list_rec) != 0:
            ret_book = book.AddressBook()
            ret_book.rec_per_page = self.__book.rec_per_page
            for rec_ in list_rec:
                ret_book.add_record(rec_)
            return (ret_book, 'table')
        return (f'Pattern {value} not found.', 'warning')

    def __add_phone(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        value = input(self.__PROMPTS.get('phone_prompt'))

        found = self.__book.find_pattern(value, 'phones')
        if found:
           return ('Phone exist', 'warning')
        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'warning')
        record.add_phone(value)
        return (f'For user {name} successfully added phone {value}.', 'normal')

    def __change_phone(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        old_value = input(self.__PROMPTS.get('old_phone_prompt'))
        new_value = input(self.__PROMPTS.get('new_phone_prompt'))

        found = self.__book.find_pattern(new_value, 'phones')
        if found:
            return ('Phone exist', 'warning')
        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'warning')

        if record.phones is not None:
            record.edit_phone(old_value, new_value)
            return (f'Phone {old_value} from user {name} successfully changet to phone {new_value}', 'normal')
        else:
            record.add_phone(new_value)
            return (f'For user {name} successfully added phone {new_value}', 'normal')

    def __delete_phone(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        value = input(self.__PROMPTS.get('phone_del_prompt'))

        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'critical')
        record.delete_phone(value)
        return (f'From user {name} successfully deleted phone {value}.', 'normal')

    def __add_birthday(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        value = input(self.__PROMPTS.get('birthday_prompt'))

        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'critical')
        record.add_birthday(value)
        return (f'To user {name} successfully added birthday date:\n\t {value}', 'normal')

    def __replace_birthday(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        value = input(self.__PROMPTS.get('birthday_prompt'))

        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'critical')
        if record.birthday is not None:
            record.edit_birthday(value)
            return (f'Birthday of user {name} successfully changet to {value}', 'normal')
        else:
            record.add_birthday(value)
            return (f'To user {name} successfully added birthday date:\n\t {value}', 'normal')

    def __delete_birthday(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()

        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'critical')
        record.delete_birthday()
        return (f'From user {name} successfully deleted birthday date.', 'normal')

    def __find_birthday(self):
        value = input(self.__PROMPTS.get('birthday_search_prompt'))

        qua_days = value
        if not qua_days:
            qua_days = 10
        else:
            qua_days = int(qua_days)

        list_rec = self.__book.find_records_for_birthday(qua_days)
        if len(list_rec) != 0:
            ret_book = book.AddressBook()
            ret_book.qua_for_iter = self.__book.rec_per_page
            for rec_ in list_rec:
                ret_book.add_record(rec_)
            return (ret_book, 'table')
        return (f'Contact with birthdays in {qua_days} days not found.', 'warning')

    def __next_birthday(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()

        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'critical')
        days = record.days_to_birthday()
        if days:
            return (f'Next birthday for user {name} after {days} days', 'normal')
        else:
            return (f'Unknown birthday for user {name}', 'warning')

    def __add_email(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        value = input(self.__PROMPTS.get('email_prompt'))

        found = self.__book.find_pattern(value, 'emails')
        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'critical')
        elif found:
            return ('User already has an e-mail', 'warning')
        record.add_email(value)
        return (f'To user {name} successfully added e-mail:\n\t {value}', 'normal')

    def __delete_email(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        value = input(self.__PROMPTS.get('email_del_prompt'))

        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'critical')
        record.delete_email(value)
        return (f'From user {name} successfully deleted e-mail {value}.', 'normal')

    def __replace_email(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        old_value = input(self.__PROMPTS.get('old_email_prompt'))
        new_value = input(self.__PROMPTS.get('new_email_prompt'))

        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'critical')

        found = self.__book.find_pattern(new_value, 'emails')
        if found:
            return ('User already has an e-mail', 'warning')

        if record.emails is not None:
            record.edit_email(old_value, new_value)
            return (f'For user {name} e-mail\n\t{old_value} \nsuccessfully changed to:\n\t{new_value}', 'normal')
        else:
            record.add_email(new_value)
            return (f'To user {name} successfully added e-mail:\n\t {new_value}', 'normal')

    def __add_memo(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        value = input(self.__PROMPTS.get('memo_prompt'))

        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'critical')
        record.add_memo(value)
        return (f'To user {name} successfully added memo:\n\t {value}', 'normal')

    def __delete_memo(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        value = input(self.__PROMPTS.get('memo_del_prompt'))

        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'critical')
        record.delete_memo(value)
        return (f'From user {name} successfully deleted memo {value}.', 'normal')

    def __replace_memo(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        old_value = input(self.__PROMPTS.get('old_memo_prompt'))
        new_value = input(self.__PROMPTS.get('new_memo_prompt'))

        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'critical')
        if record.memos is not None:
            record.edit_memo(old_value, new_value)
            return (f'For user {name} memo\n\t{old_value} \nsuccessfully changed to:\n\t{new_value}', 'normal')
        else:
            record.add_memo(new_value)
            return (f'To user {name} successfully added memo:\n\t {new_value}', 'normal')

    def __add_addr(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        value = input(self.__PROMPTS.get('address_prompt'))

        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'critical')

        found = self.__book.find_pattern(value, 'address')
        if found:
            return ('User already has an address', 'warning')

        record.add_address(value)
        return (f'To user {name} successfully added address:\n\t {value}', 'normal')

    def __delete_addr(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        value = input(self.__PROMPTS.get('address_del_prompt'))

        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'critical')
        record.delete_address(value)
        return (f'From user {name} successfully deleted address {value}.', 'normal')

    def __replace_addr(self):
        name = input(self.__PROMPTS.get('user_name_prompt')).capitalize()
        old_value = input(self.__PROMPTS.get('old_address_prompt'))
        new_value = input(self.__PROMPTS.get('new_address_prompt'))

        record = self.__book.find(name)
        if not record:
            return ('User not exists, repeat please', 'critical')

        found = self.__book.find_pattern(new_value, 'address')
        if found:
            return ('User already has an address', 'warning')

        if record.address is not None:
            record.edit_address(old_value, new_value)
            return (f'For user {name} address\n\t{old_value} \nsuccessfully changed to:\n\t{new_value}', 'normal')
        else:
            record.add_address(new_value)
            return (f'To user {name} successfully added address:\n\t {new_value}', 'normal')
        
    def get_input(self):
        try:
            user_input = prompt(self.__PROMPTS.get('command_prompt'), completer=WordCompleter(
                self.__NAME_COMMANDS.keys(), ignore_case=True))

            return_data = self.__NAME_COMMANDS[user_input]()

        except KeyboardInterrupt:
            # user_input_list = ('\nCommand input interrupted. Exiting...',)
            exit()
        except KeyError:
            return_data = ('Wrong command, try again', 'critical')

        # except IndexError:
        #     return_data = ('Give me name please', 'critical')
        # except TypeError:
        #     return_data = ('Wrong command, try again', )
        # except ValueError:
        #     return_data = ('Wrong number, repeat please', )

        # except book.UserExists:
        #     return_data = ('User already exists.')
        # except book.WrongName:
        #     return_data = ('User not exists, repeat please', )
        # except book.WrongPhone:
        #     return_data = (
        #         'Phone should have only digits and be at least 10 digits long.', )
        # except book.ExistsPhone:
        #     return_data = ('Phone exist', )
        # except book.NotExistsPhone:
        #     return_data = ('Phone not exist', )
        # except book.WrongBirthday:
        #     return_data = ('Wrong birthday, repeat please', )
        # except book.ExistsBirthday:
        #     return_data = ('User already has a birthday', )
        # except book.WrongMemo:
        #     return_data = (
        #         'Not printable characters in Memo or record size excides.', )
        # except book.ExistsMemo:
        #     return_data = ('User already has a memo', )
        # except book.WrongAddress:
        #     return_data = (
        #         'Not printable characters in Address or record size excides.', )
        # except book.ExistsAddress:
        #     return_data = ('User already has an address', )
        # except book.WrongEmail:
        #     return_data = ('Wrong e-mail, repeat please', )
        # except book.ExistsEmail:
        #     return_data = ('User already has an e-mail', )

        return return_data

class CLI_Output(Output):
    def __init__(self):
        self.__styles = {
            'normal': 'green',
            'warning': 'yellow',
            'critical': 'red',
            'table': {
                'header_style': 'bold blue', 
                'row_style': 'bright_green'
            }
        }

    def table(self, title=None, title_style=None, header=[], header_style=None, rows=[], row_style=None):

        table = Table()
        if title:
            table.title = title
            table.title_style = title_style
            table.title_justify = 'left'

        longest_row = max([len(row) for row in rows])
        if len(header) < longest_row:
            for i in range(longest_row - len(header)):
                header.append(f'Column_{i}')

        for column in header:
            table.add_column(column, header_style=header_style, width=40)

        for row in rows:
            table.add_row(*row, style=row_style)

        table.show_lines = True

        Console().print(table)

    def __value_getter(self, value):

        if isinstance(value, list):
            value = ' '.join([str(i) for i in value])
        elif value:
            value = str(value)
        else:
            value = ''
        return value

    def __book_output(self, data):
        records = []
        rec_per_page = data[0].rec_per_page

        for record in data[0].data.values():
            row = [
                self.__value_getter(record.name),
                self.__value_getter(record.phones),
                self.__value_getter(record.emails),
                self.__value_getter(record.birthday),
                self.__value_getter(record.address),
                self.__value_getter(record.memos)
            ]
            records.append(row)

        header = ['Name', 'Phones', 'E-mails',
                'Birthday', 'Address', 'Memos']
        title = '...'
        page = []
        for row in enumerate(records, start=1):
            if (row[0] == len(records)):  # and (page != []):
                page.append(row[1])
                self.table(title=title, header=header, rows=page,
                           **self.__styles.get(data[1]))
                page.clear()
            elif row[0] % rec_per_page:
                page.append(row[1])
            else:
                page.append(row[1])
                self.table(title=title, header=header, rows=page,
                           **self.__styles.get(data[1]))
                page.clear()
                if input('Continue (n - to break)?').lower() == 'n':
                    break

    def user_output(self, data):

        if isinstance(data[0], str):
            console = Console()
            console.print(data[0], style=self.__styles.get(data[1]))

        elif isinstance(data[0], book.AddressBook):
            self.__book_output(data)
        
        elif isinstance(data[0], list):
            self.table(header=data[0][0], rows=data[0][1:], **self.__styles.get(data[1]))
        
        else:
            console = Console()
            console.print(
                f'Got uknown data format {type(data)}', style=self.__styles.get('critical'))
