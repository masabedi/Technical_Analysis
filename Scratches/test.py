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
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None


    def next(self):
        # Simply log the closing price of the series from the reference
        self.log(f"Close, {self.dataclose[0]:0.0f}")

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.buy()

        else:

            # Already in the market ... we might sell
            if len(self) >= (self.bar_executed + 5):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()



''' Guide
 self.order : Check if an order is pending
 self.position : Check if we are in the market

 Buy strategies :
 Strategy 1 :
 If the price has been falling 3 sessions in a row … BUY

 if self.dataclose[0] < self.dataclose[-1]:
        # current close less than previous close

        if self.dataclose[-1] < self.dataclose[-2]:
            # previous close less than the previous close

            # BUY, BUY, BUY!!! (with default parameters)
            self.log('BUY CREATE, %.2f' % self.dataclose[0])

            # Keep track of the created order to avoid a 2nd order
            self.order = self.buy()


 Sell Strategies :
 S-Strategy 1 :
 Exit after 5 bars (on the 6th bar) have elapsed for good or for worse

 if len(self) >= (self.bar_executed + 5):
    # SELL, SELL, SELL!!! (with all possible default parameters)
    self.log('SELL CREATE, %.2f' % self.dataclose[0])

    # Keep track of the created order to avoid a 2nd order
    self.order = self.sell()

 '''

if __name__ == "__main__":

    cerebro = bt.Cerebro()

    cerebro.addstrategy(test_strategy)

    data = bt.feeds.PandasData(dataname=db_data)

    cerebro.adddata(data)

    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())











































