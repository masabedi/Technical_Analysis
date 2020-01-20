import data_catcher.history as history
import pandas as pd
import talib
import datetime



sahamyab_data = history.sahamyab_dataframe("وغدیر", 12)
db_data = history.database_dataframe()

data = db_data

def date_convertor(timestapm_columns):
    index = timestapm_columns
    for i in range(len(index)):
        date = int(index[i])
        index[i] = datetime.datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
    return index

# Backtesting ============================================================


import pandas as pd


def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    return pd.Series(values).rolling(n).mean()


from backtesting import Strategy
from backtesting.lib import crossover


class SmaCross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    n2 = 20

    def init(self):
        # Precompute two moving averages
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self):
        # If sma1 crosses above sma2, buy the asset
        if crossover(self.sma1, self.sma2):
            self.buy()

        # Else, if sma1 crosses below sma2, sell it
        elif crossover(self.sma2, self.sma1):
            self.sell()


if __name__ == "__main__":

    from backtesting import Backtest
    bt = Backtest(data, SmaCross, cash=10000, commission=.002)
    print(bt.run())
    # bt.plot()





































