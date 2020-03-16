import pymysql

class DB:
    db = None

    def __init__(self):
        try:
            self.db = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd = '', db = 'trade_log')
        except Exception as e:
            print('Unable to connect to DB\n' + str(e))
            utils.exit_app()

    def connection(self):
        return self.db
