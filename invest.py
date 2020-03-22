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
        q = "SELECT id, symbol, entry_price, shares, dividend, target, bail_area, commission"
        q += " FROM " + self.invest_tbl + " WHERE status = 'open'"
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
            items['target'] = row[5]
            items['bail_area'] = row[6]
            items['commission'] = row[7]
            items['adjs'] = []
            a = self.get_inv_adjusts(row[0])
            if a != False:
                for adjs in a:
                    adj = {}
                    adj['id'] = row[0]
                    adj['shares'] = adjs[0]
                    adj['price'] = adjs[1]
                    adj['commission'] = adjs[2]
                    items['adjs'].append(adj)

            investments.append(items)

        return investments

    def get_inv_adjusts(self, id):
        q = "SELECT shares, price, commission FROM " + self.adj_tbl + " WHERE inv_id = " + str(id)
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
            commissions = 0
            shares += p['shares']
            amount += p['entry_price'] * p['shares']
            commissions += p['commission']

            for a in p['adjs']:
                shares += a['shares']
                amount += a['price'] * a['shares']
                commissions += a['commission']

            items['symbol'] = p['symbol']
            items['shares'] = shares
            items['amount_invested'] = amount
            items['est_annual_div'] = shares * p['div']
            items['avg_price'] = round(amount / shares, 2)
            items['commissions'] = commissions
            items['initial_entry_price'] = p['entry_price']

            positions.append(items)

        return positions

    def calc_totals(self):
        positions = self.calc_positions()
        if positions == False:
            return False

        items = {}
        commissions = 0
        count = 0
        amount = 0
        shares = 0
        for p in positions:
            commissions += p['commissions']
            count += 1
            amount += p['amount_invested']
            shares += p['shares']

        items['commissions'] = commissions
        items['positions'] = count
        items['invested'] = amount
        items['shares'] = shares
        return items

