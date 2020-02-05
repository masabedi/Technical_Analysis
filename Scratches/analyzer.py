import backtrader as bt
from datetime import datetime
from collections import OrderedDict



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
        if not self.position:
            if self.rsi < 30:
                self.buy()
        else:
            if self.rsi > 70:
                self.sell()

    # def stop(self):
    #     pnl = round(self.broker.getvalue() - self.startcash,1)
    #     print(f'RSI Period: {self.params.period} Final PnL: {pnl}')

if __name__ == "__main__":

    #Variable for our starting cash
    startcash = 100000

    #Create an instance of cerebro
    cerebro = bt.Cerebro()

    #Add our strategy
    cerebro.addstrategy(firstStrategy)

    #Get Apple data from Yahoo Finance.
    data = bt.feeds.PandasData(dataname=db_data)


    #Add the data to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(startcash)

    # Add the analyzers we are interested in
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="mysharpe")
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
    cerebro.addanalyzer(bt.analyzers.Returns, _name="retrn")


    # Run over everything
    thestrats = cerebro.run()
    thestrat = thestrats[0]

    sharp = thestrat.analyzers.mysharpe.get_analysis()
    ta = thestrat.analyzers.ta.get_analysis()
    sqn = thestrat.analyzers.sqn.get_analysis()
    retrn = thestrat.analyzers.retrn.get_analysis()
    # print(sharp.keys())
    print(retrn.keys())
    # print(sharp.values())
    print(retrn.values())
    # print(ta.values())
    # print(keys)
    # print(ta.get("lost"))
    # # #Finally plot the end results
    # cerebro.plot(style='candlestick')
