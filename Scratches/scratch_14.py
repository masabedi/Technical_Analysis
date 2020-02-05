import data_catcher.history as history
import pandas as pd
import backtrader as bt
import datetime
import os.path
import sys

# DATA ============================================================


# sahamyab_data = history.sahamyab_dataframe("وغدیر", 12)
db_data = history.database_dataframe()


# Backtesting ============================================================

def add_data(data_feed):
    args = parse_args()

    # Create a cerebro entity
    cerebro = bt.Cerebro(stdstats=False)

    # Add a strategy
    cerebro.addstrategy(bt.Strategy)

    dataframe = data_feed

    if not args.noprint:
        print('--------------------------------------------------')
        print(dataframe)
        print('--------------------------------------------------')

    # Pass it to the backtrader datafeed and add it to the cerebro
    data = bt.feeds.PandasData(dataname=dataframe)

    cerebro.adddata(data)

    # Run over everything
    cerebro.run()

    # Plot the result
    # cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pandas test script')

    parser.add_argument('--noheaders', action='store_true', default=False,
                        required=False,
                        help='Do not use header rows')

    parser.add_argument('--noprint', action='store_true', default=False,
                        help='Print the dataframe')

    return parser.parse_args()


class test_strategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        # define date
        dt = dt or self.datas[0].datetime.date(0)

        # pring date and desirable text
        print(f"{dt.isoformat()}, {txt}")

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders
        self.sma = bt.indicators.SMA(period=15)

    def next(self):

        if self.sma > self.data.close:
            self.log(f"Buy: SMA = {self.sma[0]}, Close  = {self.dataclose[0]:0.0f}")
            # Do something
            pass

        elif self.sma < self.data.close:
            self.log(f"Sell : SMA = {self.sma[0]}, Close  = {self.dataclose[0]:0.0f}")
            # Do something else
            pass


class SMACloseSignal(bt.Indicator):
    lines = ('signal',)
    params = (('period', 30),)

    def __init__(self):
        self.lines.signal = self.data - bt.indicators.SMA(period=self.p.period)


if __name__ == "__main__":
    cerebro = bt.Cerebro()

    cerebro.addstrategy(test_strategy)

    data = bt.feeds.PandasData(dataname=db_data)

    cerebro.adddata(data)

    cerebro.add_signal(bt.SIGNAL_SHORT, SMACloseSignal)

    cerebro.run()











































