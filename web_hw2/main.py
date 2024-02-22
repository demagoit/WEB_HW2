"""Консольний бот для управління додатком"""
# import bot_helper.address_book as book
# import bot_helper.note_book as notebook
# import bot_helper.pretty as pretty
# from bot_helper.commands import *

# from . import address_book as book
# from . import note_book as notebook
# from . import pretty
# from .commands import *

import os
import address_book as book
from book_IO import *


class Singleton:
    '''will keep instance of working adress book'''
    __instance = None
    __book = None

    def __new__(cls, path: os.path = None):
        if cls.__instance is None:
            cls.__instance = super().__new__(Singleton)
            if os.path.exists(path):
                cls.__book = book.AddressBook()
                cls.__book.load_JSON(path)
            else:
                cls.__book = book.AddressBook()
        return cls.__book

def main():
    """Initiate or loads address book"""
    
    # handler_hello()

    # current_path = os.path.abspath(os.getcwd())
    current_path = os.path.dirname(__file__)
    file_name_phones = os.path.join(current_path, 'phonebook.json')
    my_book_phones = Singleton(file_name_phones)

    CLI_in = CLI_Input(my_book_phones)
    CLI_out = CLI_Output()

    CLI_out.user_output(CLI_in.get_help())
    while True:

        # ret_rezault = get_command_suggestions(my_book_phones)
        ret_rezault = CLI_in.get_input()

        if ret_rezault:
            # pretty.parser(ret_rezault, '1')
            CLI_out.user_output(ret_rezault)
            # pretty.parser(ret_rezault, mode)
            if ret_rezault[0] == "Good bye!":
                my_book_phones.save_JSON(file_name_phones)
                exit()

if __name__ == "__main__":
    main()
