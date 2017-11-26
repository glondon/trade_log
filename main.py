import pymysql
import datetime
import utils
from pprint import pprint

class TradeLog:
    db = None
    positions = ['long', 'short']
    accounts = ['tos', 'ibg', 'ibc']

    def __init__(self):
        try:
            self.db = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd = '', db = 'trade_log')
        except ValueError as e:
            print('Unable to connect to DB' + e)
            utils.exit_app()

    def menu(self):
        utils.title('Menu')

        menu_list = [
            '1.  View trades - current month',
            '2.  Add new trade',
            '3.  Update a trade',
            '4.  Remove a trade',
            '5.  View all open trades',
            '6.  View menu',
            '7.  View trading rules',
            '8.  Exit program',
            '9.  Show watchlist',
            '10. Show weekly trade ideas',
            '11. Add trade idea',
            '12. View trades - certain date',
            '13. View notes on trades exited early'
        ]

        for item in menu_list:
            print(item)

    def show_rules(self):
        cur = self.db.cursor()
        cur.execute("SELECT rule FROM trade_rules ORDER BY rule DESC")
        counter = 1

        utils.title('Trading Rules')

        for row in cur.fetchall():
            print(str(counter) + ' - ' + row[0])
            print('-------------------------------------------------')
            counter += 1

        cur.close()

        print('Total Rules: ' + str(counter - 1))

    def show_watchlist(self):
        #TODO finish adding watchlist items
        cur = self.db.cursor()
        cur.execute("SELECT ticker FROM watchlist ORDER BY ticker")

        utils.title('Watchlist')

        watchlist = ''
        result = cur.fetchall()
        for i, row in enumerate(result):
            if i == len(result) - 1:
                watchlist += row[0]
            elif i == 10 or i == 21 or i == 32:
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

        utils.title('Trade ideas')

        if cur.rowcount > 0:
            to_show = ''
            for row in cur.fetchall():
                to_show += str(row[2]) + ' - ' + row[0] + ' - ' + row[1] + '\n'

            print(to_show)
        else:
            print('None')

    def trade_entry(self):
        utils.title('Trade Entry')

        print('Enter the symbol, entry price, position, date, and account:\n(comma separated):\n')

        values = input()

        if values != '':
            result = utils.split_string(values)
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
                if not utils.validate_float(entry_price):
                    errors.append('Entry price not a valid float value')
                if not position in self.positions:
                    errors.append('Position can only be long or short')
                if not utils.validate_date(trade_date):
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
        utils.title('Add Trade Idea')

        print('Enter symbol & notes (comma separated):\n')

        values = input()

        if values != '':
            result = utils.split_string(values)
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

    def view_trades(self, month = False, o = False):

        if month == False:
            today = datetime.datetime.today()
            month = today.month

        title = 'Viewing all trades' if o == False else 'Viewing open trades'

        utils.title(title)
        print('Month Start: ' + utils.get_month(month) + '\n')
        
        begin = datetime.date.today().replace(month = month, day = 1)
        
        query = "SELECT * FROM trades WHERE entry_date >= '" + str(begin) + "'"

        if o == False:
            query += ''
        else:
            query += " AND status = '" + o + "'"

        query += " ORDER BY entry_date DESC"

        try:
            cur = self.db.cursor()
            cur.execute(query)
            if cur.rowcount > 0:
                if o == False:
                    format_header = '{0:3} {1:<6} {2:<6} {3:<10} {4:<5} {5:<5} {6:<8} {7:<8}'.format('ID', 'SYMBOL', 'POS', 'EN:DATE', 'ACC', 'COM', 'RESULT', 'STATUS')
                else:
                    format_header = '{0:3} {1:<6} {2:<6} {3:<10} {4:<5} {5:<5} {6:<8} {7:<8} {8:<8}'.format('ID', 'SYMBOL', 'POS', 'EN:DATE', 'ACC', 'COM', 'RESULT', 'STATUS', 'EN:PRICE')
                print(format_header)
                total = 0
                total_comm = 0
                positions = []
                exits = []
                total_trades = 0
                results = []
                statuses = []
                accounts = []
                symbols = []
                for row in cur.fetchall():
                    total += row[13]
                    total_comm += row[11] + row[12]
                    comm = row[11] + row[12]
                    positions.append(row[4])
                    exits.append({'exit': row[14], 'status': row[17]})
                    total_trades += 1
                    results.append(row[13])
                    statuses.append(row[17])
                    accounts.append(row[10])
                    symbols.append(row[1])
                    if o == False:
                        print_row = '{0:<3d} {1:<6} {2:<6} {3:<8} {4:<5} {5:<5f} {6:<8f} {7:<8}'.format(row[0], row[1], row[4], str(row[7]), row[10], comm, row[13], row[17])
                    else:
                        print_row = '{0:<3d} {1:<6} {2:<6} {3:<8} {4:<5} {5:<5f} {6:<8f} {7:<8} {8:<8}'.format(row[0], row[1], row[4], str(row[7]), row[10], comm, row[13], row[17], utils.format_price(row[2]))
                    print(print_row)    

                cur.close()
                after_comm = total - total_comm
                pos_sum = utils.sum_positions(positions)
                exit_early = utils.sum_exit_early(exits)
                win_rate = utils.win_rate(results)
                status_sum = utils.sum_statuses(statuses)
                acc_sum = utils.sum_accounts(accounts)
                print('{0:<22} {1:6}'.format('\nTotal proft/loss: ', '$' + str(total)))
                print('{0:<21} {1:6}'.format('Total commissions: ', '$' + str(total_comm)))     
                print('{0:<15} {1:6}'.format('Total final results: ', '$' + str(after_comm)))   

                print('\nTotal trades: ' + str(total_trades))
                print('Total long: ' + str(pos_sum[0]) + ' Total short: ' + str(pos_sum[1]))
                print('Trades exited early: ' + str(exit_early[0]) + ' Good exits: ' + str(exit_early[1]))
                print('Wins: ' + str(win_rate[0]) + ' Losses: ' + str(win_rate[1]) + ' Win Rate: ' + str(round(win_rate[2], 2)) 
                    + '%' + ' Average: $' + str(round(win_rate[3], 2)))
                minimum = '$' + str(win_rate[5]) if win_rate[5] < 0 else 'No losses'
                print('Largest Profit: $' + str(win_rate[4]) + ' Largest Loss: ' + minimum)
                print('Open trades: ' + str(status_sum[0]) + ' Closed trades: ' + str(status_sum[1]))
                print('Accounts: TOS: ' + str(acc_sum[0]) + ' IBG: ' + str(acc_sum[1]) + ' IBC: ' + str(acc_sum[2]))
                if o == False:
                    print('Number of times ES traded: ' + str(utils.traded_most(symbols)))
            else:
                print('No trades found')
        except ValueError as e:
            print('Problem retrieving trades\n' + e)

    def view_trades_date(self):
        print('Enter a starting month (1-12):\n')

        month = input()

        if utils.validate_int(month):
            month = int(month)
            if month < 1 or month > 12:
                print('Invalid month entered')
            else:
                self.view_trades(month)
        else:
            print('Invalid date entered')

    def view_open(self):
        #view since beginning of current year
        self.view_trades(1, 'open')

    def view_exit_notes(self):
        utils.title('Early Exit Notes')
        #start with trades in most recent trading month
        begin = datetime.date.today().replace(day = 1)
        query = "SELECT symbol, notes FROM trades WHERE early_exit = 1 AND exit_date >= '" + str(begin) + "' ORDER BY exit_date"

        try:
            cur = self.db.cursor()
            cur.execute(query)
            if cur.rowcount > 0:
                for row in cur.fetchall():
                    print(row[0] + ' - ' + row[1])
                    print('---------------------------------------------')
            else:
                print('No trades notes found')
        except ValueError as e:
            print('Problem retrieving trades\n' + e)

# class end - start running

t = TradeLog()
t.menu()

print('\n--------\n')

options = {
    1 : t.view_trades,
    2 : t.trade_entry,
    5 : t.view_open,
    6 : t.menu,
    7 : t.show_rules,
    8 : utils.exit_app,
    9 : t.show_watchlist,
    10 : t.show_trade_plan,
    11 : t.add_idea,
    12 : t.view_trades_date,
    13 : t.view_exit_notes
}

while True:
    option = input('Choose option\n')
    entered = utils.validate_int(option)

    if(entered != False):
        if entered in options:
            options[entered]()
        else:
            print('Not a valid option')

        print('\nYou entered ', entered)
    else:
        print('Not a vaild option')

t.db.close()
