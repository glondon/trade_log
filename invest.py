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

        investments = []
        
        for row in r:
            items = {}
            items['id'] = row[0]
            items['symbol'] = row[1]
            items['entry_price'] = row[2]
            items['shares'] = row[3]
            items['div'] = row[4]
            items['adjs'] = []
            a = self.get_inv_adjusts(row[0])
            if a != False:
                for adjs in a:
                    adj = {}
                    adj['id'] = row[0]
                    adj['shares'] = adjs[0]
                    adj['price'] = adjs[1]
                    items['adjs'].append(adj)

            investments.append(items)

        return investments

    def get_inv_adjusts(self, id):
        q = "SELECT shares, price FROM " + self.adj_tbl + " WHERE inv_id = " + str(id)
        r = self.db.run_query(q)
        if r != False:
            return r

        return False

    def calc_positions(self):
        invests = self.get_investments()
        if invests == False:
            return False
        
        positions = []
        
        for p in invests:
            items = {}
            shares = 0
            amount = 0
            shares += p['shares']
            amount = p['entry_price'] * p['shares']

            for a in p['adjs']:
                shares += a['shares']
                amount += a['price'] * a['shares']

            items['symbol'] = p['symbol']
            items['shares'] = shares
            items['amount_invested'] = amount
            items['est_annual_div'] = shares * p['div']
            items['avg_price'] = round(amount / shares, 2)

            positions.append(items)
            
        return positions