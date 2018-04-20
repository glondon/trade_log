import sys

def exit_app():
    sys.exit('Trade Log exited')

def title(string):
    print('\n-------------')
    print(string + ':')
    print('-------------\n')

def format_price(value):
    temp = str(value)
    if temp.find('.') != -1:
        i, f = temp.split('.')
        if len(f) == 4:
            if int(f[2]) > 0:
                return value
            else:
                return format(value, '.2f')

def traded_most(values):
    #only counting ES for now - since I know it's the favorite
    return values.count('ES')

def sum_accounts(values):
    tos = 0
    ibg = 0
    ibc = 0

    for x in values:
        if x == 'tos':
            tos += 1
        elif x == 'ibg':
            ibg += 1
        else:
            ibc += 1

    return [tos, ibg, ibc]

def sum_statuses(values):
    open = 0
    closed = 0
    for x in values:
        if x == 'open':
            open += 1
        else:
            closed += 1

    return [open, closed]

def win_rate(values):
    wins = 0
    losses = 0
    counter = 0
    sum = 0
    lrg = max(values)
    sml = min(values)
    for x in values:
        sum += x
        if x < 0:
            losses += 1
            counter += 1
        elif x > 0:
            wins += 1
            counter += 1

    if wins > 0 and counter > 0:
        win_rate = wins / counter * 100
    else:
        win_rate = float(0)

    if counter > 0:
        avg = sum / counter
    else:
        avg = float(0)

    return [wins, losses, win_rate, avg, lrg, sml]

def sum_exit_early(values):
    times = 0
    not_times = 0
    for x in values:
        if x.get('exit') == 1 and x.get('status') == 'closed':
            times += 1
        elif x.get('exit') == 0 and x.get('status') == 'closed':
            not_times += 1

    return [times, not_times]

def sum_positions(values):
    lng = 0
    sht = 0
    for x in values:
        if x == 'long':
            lng += 1
        else:
            sht += 1

    return [lng, sht]

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

def validate_date(value):
    try:
        datetime.datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_int(value):
    try:
        value = int(value)
        return value
    except ValueError:
        return False

def split_string(values):
    return [item.strip() for item in values.split(',')]

def get_month(month):
    months = {
        1 : 'January',
        2 : 'February',
        3 : 'March',
        4 : 'April',
        5 : 'May',
        6 : 'June',
        7 : 'July',
        8 : 'August',
        9 : 'September',
        10 : 'October',
        11 : 'November',
        12 : 'December'
    }

    if month in months:
        return months[month]
    else:
        return 'Invalid Month'

def account_results(t_vals, g_vals, b_vals):
    t = sum(t_vals)
    g = sum(g_vals)
    b = sum(b_vals)
    return [t, g, b]

def month_check(m):
    if m >= 1 or m <= 12:
        return True
    else:
        return False

def year_check(y):
    years = [2017, 2018]
    if y in years:
        return True
    else:
        return False
        