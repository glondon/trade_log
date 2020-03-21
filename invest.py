import db
import utils
from pprint import pprint

class Invest:

    db = None
    invest_tbl = 'investments'
    adj_tbl = 'inv_adjusts'

    def __init__(self):
        try:
            self.db = db.DB()
        except Exception as e:
            print('Unable to connect to DB\n' + str(e))
            utils.exit_app()

    def get_investments(self):
        q = "SELECT id, symbol, entry_price, shares, dividend FROM " + self.invest_tbl + " WHERE status = 'open'"
        r = self.db.run_query(q)
        if r == False:
            return False

        items = {}
        adj = {}
        for row in r:
            items['id'] = row[0]
            items['symbol'] = row[1]
            items['entry_price'] = row[2]
            items['shares'] = row[3]
            items['div'] = row[4]
            items['adjs'] = []
            a = self.get_inv_adjusts(row[0])
            if a != False:
                for adjs in a:
                    adj['id'] = row[0]
                    adj['shares'] = adjs[0]
                    adj['price'] = adjs[1]
                    items['adjs'].append(adj)
                    adj = {} # reset

        return items

    def get_inv_adjusts(self, id):
        q = "SELECT shares, price FROM " + self.adj_tbl + " WHERE inv_id = " + str(id)
        r = self.db.run_query(q)
        if r != False:
            return r

        return False