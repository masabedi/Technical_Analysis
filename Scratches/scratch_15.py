import data_catcher.history as history
import backtrader as bt
from datetime import datetime

db_data = history.database_dataframe()

class firstStrategy(bt.Strategy):
    params = dict(period=21)

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.p.period)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy(size=100)
        else:
            if self.rsi > 70:
                self.sell(size=100)


if __name__ == "__main__":

    #Variable for our starting cash
    startcash = 10000

    #Create an instance of cerebro
    cerebro = bt.Cerebro()

    #Add our strategy
    cerebro.addstrategy(firstStrategy)

    #Get Symbol data from database.
    data = bt.feeds.PandasData(dataname=db_data)

    #Add the data to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(startcash)

    # Run over everything
    cerebro.run()

    #Get final portfolio Value
    portvalue = cerebro.broker.getvalue()
    pnl = portvalue - startcash

    #Print out the final result
    print('Final Portfolio Value: ${}'.format(portvalue))
    print('P/L: ${}'.format(pnl))

    #Finally plot the end results
    cerebro.plot(style='candlestick')