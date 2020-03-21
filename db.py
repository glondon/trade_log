import pymysql
import utils

class DB:

    db = None

    def __init__(self):
        try:
            self.db = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd = '', db = 'trade_log')
        except pymysql.Error as e:
            print('Unable to connect to DB\n' + str(e))
            utils.exit_app()

    def run_query(self, q, one = False):
        try:
            cur = self.db.cursor()
            cur.execute(q)
            if cur.rowcount > 0:
                if one == False:
                    return cur.fetchall()
                else:
                    return cur.fetchone()
            return False
        except pymysql.Error as e:
            print('DB error: ' + e)
            return False
