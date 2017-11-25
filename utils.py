import sys

def exit_app():
    sys.exit('Trade Log exited')

def format_price(value):
    temp = str(value)
    if temp.find('.') != -1:
        i, f = temp.split('.')
        if len(f) == 4:
            if int(f[2]) > 0:
                return value
            else:
                return format(value, '.2f')