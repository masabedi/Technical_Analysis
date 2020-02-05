
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

        self.buysell = []
        self.trades = []
        self.signal = []
        self.test = self.data.datetime.date()
        self.startcash = self.broker.getvalue()
        ema1 = bt.ind.EMA(period=self.p.pfast)  # fast moving average
        ema2 = bt.ind.EMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(ema1, ema2)  # crossover signal



    def next(self):
        # Access -1, because drawdown[0] will be calculated after "next"
        # self.log('DrawDown: %.2f' % self.stats.drawdown.drawdown[-1])
        # self.log('MaxDrawDown: %.2f' % self.stats.drawdown.maxdrawdown[-1])
        # self.log('BUY_SELL: %.2f' % self.stats.buysell[0])




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

        # if not math.isnan(self.stats.buysell[0]):
        #     self.buysell.append(self.stats.buysell[0])
        # elif not math.isnan(self.stats.trades[0]):
        #     self.trades.append(self.stats.trades[0])
    # def stop(self):
    #     pnl = round(self.broker.getvalue() - self.startcash,1)
    #     print(f'Fast Period: {self.params.pfast} Slow Period: {self.params.pslow} Final PnL: {pnl}')

class firstStrategy(bt.Strategy):
    params = dict(period=21)

    def __init__(self):
        self.startcash = self.broker.getvalue()
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.params.period)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.close()
        else:
            if self.rsi > 70:
                self.sell()

    # def stop(self):
    #     pnl = round(self.broker.getvalue() - self.startcash,1)
    #     print(f'RSI Period: {self.params.period} Final PnL: {pnl}')

if __name__ == "__main__":


    #Variable for our starting cash
    startcash = 10000

    #Create an instance of cerebro
    cerebro = bt.Cerebro(writer=True)
    cerebro.addwriter(bt.WriterFile, csv=True)
    # cerebro = bt.Cerebro(optreturn=False)
    # cerebro = bt.Cerebro()


    # add observer
    # cerebro.addobserver(bt.observers.DrawDown)
    # cerebro.addobserver(bt.observers.BuySell)
    # cerebro.addobserver(bt.observers.Trades)

    #Add our strategy
    cerebro.addstrategy(ema_cross)
    # cerebro.optstrategy(firstStrategy, pfast=range(5,10), pslow=range(20,25))
    # cerebro.addstrategy(ema_cross, pfast=5, pslow=24)

    #Get Symbol data from database.
    data = bt.feeds.PandasData(dataname=db_data)

    #Add the data to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(startcash)

    # Run over everything
    run =  cerebro.run()


    for strategy in run:
        signals = strategy.signal
        date = strategy.test
        print(signals)
        print(date)






    # # Generate results list
    # final_results_list = []
    #
    # for strategy in run:
    #     value = round(strategy.broker.get_value(),2)
    #     PnL = round(value - startcash,2)
    #     # rsi = strategy.rsi[0]
    #     pfast = strategy.params.pfast
    #     pslow = strategy.params.pslow
    #     final_results_list.append([pfast,pslow,PnL])
    #
    # #Sort Results List
    # by_period = sorted(final_results_list, key=lambda x: x[0])
    # by_PnL = sorted(final_results_list, key=lambda x: x[1], reverse=True)

    # #Print results
    # print('Results: Ordered by period:')
    # for result in by_period:
    #     print('Period: {}, PnL: {}'.format(result[0], result[1]))
    # print('Results: Ordered by Profit:')
    # for result in by_PnL:
    #     print('Period: {}, PnL: {}'.format(result[0], result[1]))

    # print(final_results_list)
    #
    # for i in run:
    #     print(i.getpositionbyname())

    # signals = strategy.signal
    # for x in signals:
    #     print(x[0],x[1],x[2])


    # buysell = strategy.buysell
    # trades = strategy.trades
    # print(math.isnan(buysell[0]))
    # print(buysell)
    # print(trades)
    # #Finally plot the end results
    cerebro.plot(style='candlestick')





































