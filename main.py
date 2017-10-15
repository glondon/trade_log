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

    print('--------------')
    print('Trading Rules:')
    print('--------------')

    for row in cur.fetchall():
        print(row[0])

    cur.close()

def show_watchlist(db):
    #TODO finish adding watchlist items
    cur = db.cursor()
    cur.execute("SELECT ticker FROM watchlist ORDER BY ticker DESC")

    print('----------')
    print('Watchlist:')
    print('----------')

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

    print('-----------')
    print('Trde ideas:')
    print('-----------')

    if cur.rowcount > 0:
        to_show = ''
        for row in cur.fetchall():
            to_show += row[0] + ' - ' + row[1] + '\n'

        print(to_show)
    else:
        print('None')

# functions end - start running

menu()

print('--------')

while True:
    option = input('Choose option')
    entered = validate_int(option)

    if(entered != False):
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
        print('good')
        print('You entered ', entered)
    else:
        print('Not a vaild option')

db.close()
