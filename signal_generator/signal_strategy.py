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




# GENERAL FUNCTIONS ============================================================

class back_test:

    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy


    def run(self):
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

        params = []
        keys = list(parametrs.keys())
        values = list(parametrs.values())

        for i in range(len(keys)):
            params.append([keys[i], values[i]])

        PnL_list = []
        for strategy in run:
            value = round(strategy.broker.get_value(), 2)
            PnL = round(value - startcash, 2)
            PnL_list.append(PnL)


        return run, signals[0], params, PnL_list

    #   signal in format of : [['buy', {'price': 1165.0}, {'date': datetime.date(2018, 6, 17)}], ...]
    #   parameters in format of : {'param1': 1, 'param2': 2, ...}
    #   PnL in format of : [965.0, ...]

    def persian_signals(self):
        data = self.run()[1]
        for x in data:
            date = x[2].get("date")
            persian_date = jalali.Gregorian(date).persian_string()
            x[2]["date"] = persian_date
        return data
    # data in format of : [['buy', {'price': 1165.0}, {'date': '1397-3-27'}], ...]


# EMA ============================================================

class ema_cross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=5,  # period for the fast moving average
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

class ema_optimal:

    def __init__(self, data):
        self.data = data
        self.indicator = ema_cross

        # Variable for our starting cash

        startcash = 10000

        # Create an instance of cerebro
        cerebro = bt.Cerebro(optreturn=False)

        # Add our strategy
        cerebro.optstrategy(self.indicator, pfast=range(5, 10), pslow=range(30, 40))

        # Get Symbol data from database.
        data = bt.feeds.PandasData(dataname=self.data)

        # Add the data to Cerebro
        cerebro.adddata(data)

        # Set our desired cash start
        cerebro.broker.setcash(startcash)

        # Run over everything
        opt_runs = cerebro.run()

        # Generate results list
        final_results_list = []
        for run in opt_runs:
            for strategy in run:
                value = round(strategy.broker.get_value(), 2)
                PnL = round(value - startcash, 2)
                pfast = strategy.params.pfast
                pslow = strategy.params.pslow
                final_results_list.append([pfast, pslow, PnL])

        # Sort by Pnl
        by_PnL = sorted(final_results_list, key=lambda x: x[2], reverse=True)

        # for result in by_PnL:
        #     print(f'pfast: {result[0]}, pslow: {result[1]}, PnL: {result[2]}')

        self.optimized = by_PnL[0]
    #   max_profit in format of : [param1, param2, pnl]

    def run(self):
        # Variable for our starting cash
        startcash = 10000

        # Create an instance of cerebro
        cerebro = bt.Cerebro()

        # Add our strategy
        cerebro.addstrategy(self.indicator, pfast=self.optimized[0], pslow=self.optimized[1])

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

        params = []
        keys = list(parametrs.keys())
        values = list(parametrs.values())

        for i in range(len(keys)):
            params.append([keys[i], values[i]])

        PnL_list = []
        for strategy in run:
            value = round(strategy.broker.get_value(), 2)
            PnL = round(value - startcash, 2)
            PnL_list.append(PnL)


        return run, signals[0], params, PnL_list
    #   signal in format of : [['buy', {'price': 1165.0}, {'date': datetime.date(2018, 6, 17)}], ...]
    #   parameters in format of : {'param1': 1, 'param2': 2}

    def persian_signals(self):
        data = self.run()[1]
        for x in data:
            date = x[2].get("date")
            persian_date = jalali.Gregorian(date).persian_string()
            x[2]["date"] = persian_date
        return data
    # data in format of : [['buy', {'price': 1165.0}, {'date': '1397-3-27'}], ...]


# MACD ============================================================
class macd_cross(bt.Strategy):

    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=18,  # period for the fast moving average
        pslow=26,   # period for the slow moving average
        psignal=9
    )

    def __init__(self):

        self.signal = []
        self.startcash = self.broker.getvalue()
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.p.pfast,
                                       period_me2=self.p.pslow,
                                       period_signal=self.p.psignal)
        self.crossover = bt.ind.CrossOver(self.macd.macd, self.macd.signal)  # crossover signal

    def next(self):

        if not self.position:  # not in the market

            if self.crossover[0] > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long
                self.signal.append(["buy", {"price": self.data.close[0]}, {"date": self.data.datetime.date()}])

        else:

            if self.crossover[0] < 0:  # in the market & cross to the downside
                self.sell()  # close long position
                self.signal.append(["sell", {"price": self.data.close[0]}, {"date": self.data.datetime.date()}])

            elif self.crossover[0] > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long
                self.signal.append(["buy", {"price": self.data.close[0]}, {"date": self.data.datetime.date()}])

class macd_optimal:

    def __init__(self, data):
        self.data = data
        self.indicator = macd_cross

        # Variable for our starting cash

        startcash = 10000

        # Create an instance of cerebro
        cerebro = bt.Cerebro(optreturn=False)

        # Add our strategy
        cerebro.optstrategy(self.indicator, pfast=range(10, 20), pslow=range(20, 30), psignal=range(5,15))

        # Get Symbol data from database.
        data = bt.feeds.PandasData(dataname=self.data)

        # Add the data to Cerebro
        cerebro.adddata(data)

        # Set our desired cash start
        cerebro.broker.setcash(startcash)

        # Run over everything
        opt_runs = cerebro.run()

        # Generate results list
        final_results_list = []
        for run in opt_runs:
            for strategy in run:
                value = round(strategy.broker.get_value(), 2)
                PnL = round(value - startcash, 2)
                pfast = strategy.params.pfast
                pslow = strategy.params.pslow
                psignal = strategy.params.psignal
                final_results_list.append([pfast, pslow, psignal, PnL])

        # Sort by Pnl
        by_PnL = sorted(final_results_list, key=lambda x: x[3], reverse=True)

        # for result in by_PnL:
        #     print(f'pfast: {result[0]}, pslow: {result[1]}, psignal: {result[2]}, PnL: {result[3]},')

        self.optimized = by_PnL[0]
    #   max_profit in format of : [param1, param2, pnl]

    def run(self):
        # Variable for our starting cash
        startcash = 10000

        # Create an instance of cerebro
        cerebro = bt.Cerebro()

        # Add our strategy
        cerebro.addstrategy(self.indicator, pfast=self.optimized[0], pslow=self.optimized[1], psignal=self.optimized[2])

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

        params = []
        keys = list(parametrs.keys())
        values = list(parametrs.values())

        for i in range(len(keys)):
            params.append([keys[i], values[i]])

        PnL_list = []
        for strategy in run:
            value = round(strategy.broker.get_value(), 2)
            PnL = round(value - startcash, 2)
            PnL_list.append(PnL)

        return run, signals[0], params, PnL_list
    #   signal in format of : [['buy', {'price': 1165.0}, {'date': datetime.date(2018, 6, 17)}], ...]
    #   parameters in format of : {'param1': 1, 'param2': 2}

    def persian_signals(self):
        data = self.run()[1]
        for x in data:
            date = x[2].get("date")
            persian_date = jalali.Gregorian(date).persian_string()
            x[2]["date"] = persian_date
        return data
    # data in format of : [['buy', {'price': 1165.0}, {'date': '1397-3-27'}], ...]


# SAMPLE CODE ============================================================

    # optimal_run = ema_optimal(db_data).persian_signals()
    # print(optimal_run)
    #
    # normal_run = back_test(db_data, ema_cross).persian_signals()
    # print(normal_run)


if __name__ == "__main__":



    macd = back_test(db_data, macd_cross).persian_signals()
    print(macd)

    # optimal_run = macd_optimal(db_data).run()
    #
    # print(optimal_run[3])
    # print(optimal_run[2])


























































