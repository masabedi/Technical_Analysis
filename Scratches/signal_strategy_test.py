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



# Backtesting ============================================================

class ema_cross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=35   # period for the slow moving average
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







class back_test:

    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy

    def backtrader_run(self):
        # Variable for our starting cash
        startcash = 10000

        # Create an instance of cerebro
        cerebro = bt.Cerebro()

        # Add our strategy
        cerebro.addstrategy(self.strategy)

        # Get Symbol data from database.
        data = bt.feeds.PandasData(dataname=self.data)

        # Add the data to Cerebro
        cerebro.adddata(data)

        # Set our desired cash start
        cerebro.broker.setcash(startcash)

        # Run over everything
        run = cerebro.run()

        # Getting signals
        signals = []

        for strategy in run:
            signal = strategy.signal
            signals.append(signal)

        # Get all attribute from params
        parametrs = run[0].params.__dict__

        return run, signals[0], parametrs

    def persian_signals(self):
        data = self.backtrader_run()[1]
        for x in data:
            date = x[2].get("date")
            persian_date = jalali.Gregorian(date).persian_string()
            x[2]["date"] = persian_date
        return data


    def ema_optimizer(self):

        #Variable for our starting cash
        startcash = 10000

        #Create an instance of cerebro
        cerebro = bt.Cerebro(optreturn=False)

        #Add our strategy
        cerebro.optstrategy(self.strategy, pfast=range(5, 21), pslow=range(30, 60))
        # cerebro.optstrategy(strg, *kwargs)

        #Get Symbol data from database.
        data = bt.feeds.PandasData(dataname=self.data)

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

    ema = back_test(db_data, ema_cross)
    signal = ema.backtrader_run()[1]
    parametrs = ema.backtrader_run()[2]
    persian = ema.persian_signals()
    optimizer = ema.ema_optimizer()
    print(optimizer)




















































