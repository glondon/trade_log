import sys
import os
import pymysql
import datetime

db = pymysql.connect( host='localhost', port=3306, user='root', passwd='', db='trade_log' )

def menu():
    #TODO finish adding menu items
    menu_list = [
        '1.  View current trades',
        '2.  Add new trade',
        '3.  Update a trade',
        '4.  Remove a trade',
        '5.  View wins to losses',
        '6.  View menu',
        '7.  Show trading rules',
        '8.  Exit program',
        '9.  Show watchlist',
        '10. Show weekly trade ideas'
    ]

    print('\n-----')
    print('Menu:')
    print('-----\n')

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
    if value < 1 or value > 10:
        return False
    else:
        return value

def show_rules(db):
    #TODO finish adding trading rules
    cur = db.cursor()
    cur.execute("SELECT rule FROM trade_rules ORDER BY rule DESC")
    #print(cur.description)

    print('\n--------------')
    print('Trading Rules:')
    print('--------------\n')

    for row in cur.fetchall():
        print(row[0])

    cur.close()

def show_watchlist(db):
    #TODO finish adding watchlist items
    cur = db.cursor()
    cur.execute("SELECT ticker FROM watchlist ORDER BY ticker DESC")

    print('\n----------')
    print('Watchlist:')
    print('----------\n')

    watchlist = ''
    result = cur.fetchall()
    for i, row in enumerate(result):
        if i == len(result) - 1:
            watchlist += row[0]
        elif i == 10 or i == 20 or i == 30:
            watchlist += '\n'
        else:
            watchlist += row[0] + ', '

    print(watchlist)

    cur.close()

def show_trade_plan(db):
    #TODO finish adding weekly trade ideas
    begin_week = datetime.date.today() - datetime.timedelta(days = datetime.date.today().isoweekday() % 7)
    cur = db.cursor()
    query = "SELECT ticker, notes FROM trade_ideas WHERE idea_date >= " + str(begin_week) + " ORDER BY ticker DESC"
    cur.execute(query)

    print('\n-----------')
    print('Trade ideas:')
    print('-----------\n')

    if cur.rowcount > 0:
        to_show = ''
        for row in cur.fetchall():
            to_show += row[0] + ' - ' + row[1] + '\n'

        print(to_show)
    else:
        print('None')

def validate_float(value):
    try:
        test = float(value)
        return True
    except ValueError:
        return False

def trade_entry(db):
    print('\n-----------')
    print('Trade Entry:')
    print('-----------\n')

    print('Enter the symbol, entry price, and date to get started (comma separated):\n')

    values = input()

    if values != '':
        result = [item.strip() for item in values.split(',')]
        if len(result) == 3:
            symbol = result[0]
            entry_price = result[1]
            trade_date = result[2]
            #validate values
            errors = []
            if len(symbol) > 5 or len(symbol) == 0:
                errors.append('Symbol cannot be empty or greater than 5')
            if not validate_float(entry_price):
                errors.append('Entry price not a valid float value')

            if len(errors) > 0:
                print('failed')
            else:
                print('passed')

        else:
            print('3 values must be entered')
    else:
        print('Nothing entered')


# functions end - start running

menu()

print('\n--------\n')

while True:
    option = input('Choose option\n')
    entered = validate_int(option)

    if(entered != False):
        #TODO find better way to do this
        if entered == 2:
            trade_entry(db)
        if entered == 6:
            menu()
        if entered == 7:
            show_rules(db)
        if entered == 8:
            sys.exit('Trade Log exited')
        if entered == 9:
            show_watchlist(db)
        if entered == 10:
            show_trade_plan(db)

        print('')
        print('Function done executing...')
        print('You entered ', entered)
    else:
        print('Not a vaild option')

db.close()
