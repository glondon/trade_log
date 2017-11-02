import sys
import os
import pymysql
import datetime
from pprint import pprint

class TradeLog:

    db = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd = '', db = 'trade_log')
    positions = ['long', 'short']
    accounts = ['tos', 'ibg', 'ibc']

    #def __init__(self):
    #    print('init')

    def menu(self):
        #TODO finish adding menu items
        menu_list = [
            '1.  View trades',
            '2.  Add new trade',
            '3.  Update a trade',
            '4.  Remove a trade',
            '5.  View wins to losses',
            '6.  View menu',
            '7.  Show trading rules',
            '8.  Exit program',
            '9.  Show watchlist',
            '10. Show weekly trade ideas',
            '11. Add trade idea'
        ]

        self.title('Menu')

        for item in menu_list:
            print(item)

    def show_rules(self):
        #TODO finish adding trading rules
        cur = self.db.cursor()
        cur.execute("SELECT rule FROM trade_rules ORDER BY rule DESC")

        self.title('Trading Rules')

        for row in cur.fetchall():
            print(row[0])

        cur.close()

    def show_watchlist(self):
        #TODO finish adding watchlist items
        cur = self.db.cursor()
        cur.execute("SELECT ticker FROM watchlist ORDER BY ticker DESC")

        self.title('Watchlist')

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

    def show_trade_plan(self):
        #TODO finish adding weekly trade ideas
        begin_week = datetime.date.today() - datetime.timedelta(days = datetime.date.today().isoweekday() % 7)
        cur = self.db.cursor()
        query = "SELECT ticker, notes, idea_date FROM trade_ideas WHERE idea_date >= " + str(begin_week) + " ORDER BY idea_date DESC"
        cur.execute(query)

        self.title('Trade ideas')

        if cur.rowcount > 0:
            to_show = ''
            for row in cur.fetchall():
                to_show += str(row[2]) + ' - ' + row[0] + ' - ' + row[1] + '\n'

            print(to_show)
        else:
            print('None')

    def trade_entry(self):
        self.title('Trade Entry')

        print('Enter the symbol, entry price, position, date, and account:\n(comma separated):\n')

        values = input()

        if values != '':
            result = self.split_string(values)
            if len(result) == 5:
                symbol = result[0]
                entry_price = result[1]
                position = result[2]
                trade_date = result[3]
                account = result[4]
                
                errors = []
                position = position.lower()
                symbol = symbol.upper()
                account = account.lower()

                if len(symbol) > 8 or len(symbol) == 0:
                    errors.append('Symbol cannot be empty or greater than 5')
                if not self.validate_float(entry_price):
                    errors.append('Entry price not a valid float value')
                if not position in self.positions:
                    errors.append('Position can only be long or short')
                if not self.validate_date(trade_date):
                    errors.append('Invalid trade date entered')
                if not account in self.accounts:
                    errors.append('Account not valid')

                if len(errors) > 0:
                    for x in errors:
                        print(x)
                else:
                    query = "INSERT INTO trades (symbol, entry, position, entry_date, account) VALUES (%s, %s, %s, %s, %s)"
                    try:
                        cur = self.db.cursor()
                        cur.execute(query, (symbol, entry_price, position, trade_date, account))
                        db.commit()
                        cur.close()
                        print('Trade successfully inserted')
                    except ValueError:
                        print('Problem inserting trade')

            else:
                print('5 values must be entered for a new trade')
        else:
            print('Nothing entered')

    def add_idea(self):
        self.title('Add Trade Idea')

        print('Enter symbol & notes (comma separated):\n')

        values = input()

        if values != '':
            result = self.split_string(values)
            if len(result) == 2:
                symbol = result[0]
                notes = result[1]

                symbol = symbol.upper()
                date = datetime.date.today()
                errors = []

                if len(symbol) > 8 or len(symbol) == 0:
                    errors.append('Symbol cannot be greater than 8 or empty') 
                if len(notes) > 255 or len(notes) == 0:
                    errors.append('Notes cannot be greater than 255 or empty')

                if len(errors) > 0:
                    for x in errors:
                        print(x)
                else:
                    query = "INSERT INTO trade_ideas (ticker, notes, idea_date) VALUES (%s, %s, %s)"
                    try:
                        cur = self.db.cursor()
                        cur.execute(query, (symbol, notes, date))
                        self.db.commit()
                        cur.close()
                        print('Trade idea successfully added')
                    except ValueError:
                        print('Problem inserting trade idea')
            else:
                print('2 values must be entered for new trade idea')
        else:
            print('Nothing entered')

    def view_trades(self):
        #start with showing all trades - later add open,closed, wins, losses, etc..

        self.title('View Trades')
        month_begin = datetime.date.today().replace(day = 1)
        
        #initial query
        query = "SELECT id, symbol, position, entry_date, account, entry_comm, exit_comm, result, trade_reasons, notes, status "
        query += "FROM trades WHERE entry_date >= '" + str(month_begin) + "' ORDER BY entry_date DESC"

        try:
            cur = self.db.cursor()
            cur.execute(query)
            if cur.rowcount > 0:
                #TODO improve this - show values based on open or closed
                #TODO only grab basic items, added up commission, show result
                #print('{0:2} {1:6} {2:10} {3:9} {4:5} {5:6} {6:5} {7:8} {8:8}'
                #    .format('ID', 'SYMBOL', 'ENTRY', 'EXIT', 'POS', 'STOP', 'TARGET', 'EN:DATE', 'EX:DATE'))
                d = {}
                for row in cur.fetchall():
                    d.setdefault('ID', []).append(row[0])
                    d.setdefault('SYMBOL', []).append(row[1])
                    d.setdefault('ENTRY', []).append(str(row[2]))

                #    print('{0:2d} {1:6} {2:8f} {3:8f} {4:5} {5:8f} {6:8f} {7:10} {8:10}'
                #        .format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], str(row[7]), str(row[8])))     

                #pprint(d)
                for k, v in d.items():
                    print(k, v)           
            else:
                print('No trades found')
        except ValueError:
            print('Problem retrieving trades')

    @staticmethod
    def exit_app():
        sys.exit('Trade Log exited')

    # utility methods

    @staticmethod
    def title(string):
        print('\n-------------')
        print(string + ':')
        print('-------------\n')

    @staticmethod
    def validate_float(value):
        try:
            test = float(value)
        except ValueError:
            return False

        if value.find('.') != -1:
            i, f = value.split('.')
            if len(f) == 2 or len(f) == 1:
                return True
            else:
                return False
        else:
            return True

    @staticmethod
    def validate_date(value):
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_int(value):
        while True:
            try:
                value = int(value)
            except ValueError:
                return False
            else:
                break
        if value < 1 or value > 11:
            return False
        else:
            return value

    @staticmethod
    def split_string(values):
        return [item.strip() for item in values.split(',')]


# class end - start running

t = TradeLog()
t.menu()

print('\n--------\n')

options = {
    1 : t.view_trades,
    2 : t.trade_entry,
    6 : t.menu,
    7 : t.show_rules,
    8 : t.exit_app,
    9 : t.show_watchlist,
    10 : t.show_trade_plan,
    11 : t.add_idea
}

while True:
    option = input('Choose option\n')
    entered = t.validate_int(option)

    if(entered != False):
        if entered in options:
            options[entered]()
        else:
            print('Not a valid option')

        print('\nYou entered ', entered)
    else:
        print('Not a vaild option')

t.db.close()
