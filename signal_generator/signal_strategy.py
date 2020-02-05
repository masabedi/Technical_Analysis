from tools import jalali
import pandas as pd
import backtrader as bt
import datetime
import os.path
import sys
import math


# DATA ============================================================

import data_catcher.history as history
# sahamyab_data = history.sahamyab_dataframe("وغدیر", 12)
db_data = history.database_dataframe()


def persian_date(data):
    for x in data:
        date = x[2].get("date")
        persian_date = jalali.Gregorian(date).persian_string()
        x[2]["date"] = persian_date
    return data

# Backtesting ============================================================

class ema_cross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=5,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))



    def __init__(self):

        self.signal = []
        self.startcash = self.broker.getvalue()
        ema1 = bt.ind.EMA(period=self.p.pfast)  # fast moving average
        ema2 = bt.ind.EMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(ema1, ema2)  # crossover signal

    def next(self):

        if not self.position:  # not in the market

            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long
                self.signal.append(["buy", {"price": self.data.close[0]}, {"date": self.data.datetime.date()}])

        else:

            if self.crossover < 0:  # in the market & cross to the downside
                self.sell()  # close long position
                self.signal.append(["sell", {"price": self.data.close[0]}, {"date": self.data.datetime.date()}])

            elif self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long
                self.signal.append(["buy", {"price": self.data.close[0]}, {"date": self.data.datetime.date()}])

    # def stop(self):
    #     pnl = round(self.broker.getvalue() - self.startcash,1)
    #     print(f'Fast Period: {self.params.pfast} Slow Period: {self.params.pslow} Final PnL: {pnl}')

def backtrader_run(pd_data, strg):

    #Variable for our starting cash
    startcash = 10000

    #Create an instance of cerebro
    cerebro = bt.Cerebro()

    #Add our strategy
    cerebro.addstrategy(strg)

    #Get Symbol data from database.
    data = bt.feeds.PandasData(dataname=pd_data)

    #Add the data to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(startcash)

    # Run over everything
    run =  cerebro.run()

    # Getting signals
    signals = []

    for strategy in run:
        signal = strategy.signal
        signals.append(signal)

    # Get all attribute from params
    parametrs = run[0].params.__dict__

    return run, signals[0], parametrs



def optimizer(pd_data, strg):

    #Variable for our starting cash
    startcash = 10000

    #Create an instance of cerebro
    cerebro = bt.Cerebro(optreturn=False)

    #Add our strategy
    cerebro.optstrategy(strg, pfast=range(5, 8), pslow=range(20, 24))
    # cerebro.optstrategy(strg, *kwargs)

    #Get Symbol data from database.
    data = bt.feeds.PandasData(dataname=pd_data)

    #Add the data to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(startcash)

    # Run over everything
    opt_runs =  cerebro.run()

    # Generate results list
    final_results_list = []
    for run in opt_runs:
        for strategy in run:
            value = round(strategy.broker.get_value(),2)
            PnL = round(value - startcash,2)
            pfast = strategy.params.pfast
            pslow = strategy.params.pslow
            final_results_list.append([pfast,pslow,PnL])

    # Sort by Pnl
    by_PnL = sorted(final_results_list, key=lambda x: x[2], reverse=True)

    max_profit = by_PnL[0]

    return max_profit

if __name__ == "__main__":

    # run = backtrader_run(db_data, ema_cross)
    # mainm = run[0]
    # # signals = run[1]
    # print(mainm[0].__dict__)
    # signals = persian_date(signals)
    # print(signals)

    result = optimizer(db_data, ema_cross)
    print(result)

















































