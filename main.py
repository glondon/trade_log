import sys
import os

def menu():
    print('1. View current trades')
    print('2. Add new trade')
    print('3. Update a trade')
    print('4. Remove a trade')
    print('5. View wins to losses')
    print('6. View menu')

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
