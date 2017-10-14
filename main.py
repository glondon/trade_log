import sys
import os

def menu():
    menu_list = ['1. View current trades',
                 '2. Add new trade',
                 '3. Update a trade',
                 '4. Remove a trade',
                 '5. View wins to losses',
                 '6. View menu']

    for item in menu_list:
        print(item)

def validate_int(value):
    while True:
        try:
            value = int(value)
        except ValueError:
            return False
        else:
            break
    if value < 1 or value > 6:
        return False
    else:
        return value

menu()

option = input('Choose option')
entered = validate_int(option)

if(entered != False):
    print('good')
    print('You entered', entered)
else:
    print('Not a vaild option')
