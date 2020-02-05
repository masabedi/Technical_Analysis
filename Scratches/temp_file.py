
import pandas as pd
import backtrader as bt
import datetime
import os.path
import sys


# DATA ============================================================

import data_catcher.history as history
# sahamyab_data = history.sahamyab_dataframe("وغدیر", 12)
db_data = history.database_dataframe()


# Backtesting ============================================================

class ema_cross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=5,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    def __init__(self):
        self.startcash = self.broker.getvalue()
        ema1 = bt.ind.EMA(period=self.p.pfast)  # fast moving average
        ema2 = bt.ind.EMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(ema1, ema2)  # crossover signal

    def next(self):
        # if not self.position:  # not in the market
        if self.crossover > 0:  # if fast crosses slow to the upside
            self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position

    # def stop(self):
    #     pnl = round(self.broker.getvalue() - self.startcash,1)
    #     print(f'Fast Period: {self.params.pfast} Slow Period: {self.params.pslow} Final PnL: {pnl}')

class firstStrategy(bt.Strategy):
    params = dict(period=21)

    def __init__(self):
        self.startcash = self.broker.getvalue()
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.params.period)

    def next(self):
        # this means if you don't have it buy it
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
                self.signal = +1
        # this means only if you have it you can sell it + you can buy it too
        else:
            if self.rsi > 70:
                self.order = self.sell()
                self.signal = -1

            elif self.rsi < 30:
                self.order = self.buy()
                self.signal = +1



    # def stop(self):
    #     pnl = round(self.broker.getvalue() - self.startcash,1)
    #     print(f'RSI Period: {self.params.period} Final PnL: {pnl}')


if __name__ == "__main__":


    #Variable for our starting cash
    startcash = 10000

    #Create an instance of cerebro
    cerebro = bt.Cerebro(writer=True)
    cerebro.addwriter(bt.WriterFile, csv=True, out="result.csv")

    #Add our strategy
    cerebro.addstrategy(firstStrategy)
    # cerebro.optstrategy(firstStrategy, pfast=range(5,10), pslow=range(20,25))
    # cerebro.addstrategy(ema_cross, pfast=5, pslow=24)

    #Get Symbol data from database.
    data = bt.feeds.PandasData(dataname=db_data)

    #Add the data to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(startcash)

    # Run over everything
    cerebro.run()




    # # #Finally plot the end results
    # cerebro.plot(style='candlestick')











































