import sys
import os

def menu():
    #TODO finish adding menu items
    menu_list = [
        '1. View current trades',
        '2. Add new trade',
        '3. Update a trade',
        '4. Remove a trade',
        '5. View wins to losses',
        '6. View menu',
        '7. Show trading rules',
        '8. Exit program'
    ]

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
    if value < 1 or value > 8:
        return False
    else:
        return value

def show_rules():
    #TODO finish adding trading rules
    rules = [
        'Patience - with winners',
        'Options spreads (be a seller of premium) - limit risk (less strict on stops because hedged)',
        'Mental stop losses ES = around 20pts - at some point you have to take a loss if wrong, forex 200 pips, stocks 20pts while scaling out - actually put hard stops in to protect against emotion',
        'Never take a trade based off someone else\'s opinion - do own research',
        'Never pick tops or bottoms against a big trend'
    ]

    for item in rules:
        print(item)

# functions end - start running

menu()

print('--------')
option = input('Choose option')
entered = validate_int(option)

if(entered != False):
    if(entered == 7):
        show_rules()
    if(entered == 8):
        sys.exit('Trade Log exited')

    print('good')
    print('You entered', entered)
else:
    print('Not a vaild option')
