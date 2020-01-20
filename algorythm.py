import data_catcher.history as history
# for data feed
import Indicators.indicators as indicator
# for indicators

import pandas as pd




sahamyab_data = history.sahamyab_dataframe("وغدیر", 12)
db_data = history.database_dataframe()

data = db_data

# columns = ['time', 'close', 'high', 'low', 'open', 'value']
# end date is 1398/10/10  = 1577750400

# General functions



# Indicators ============================================================

# EMA
def ema_calculation(data, n1=5, n2=35):
    name1 = "ema" + str(n1)
    name2 = "ema" + str(n2)
    ema1 = talib.EMA(data["close"], timeperiod=n1)
    ema2 = talib.EMA(data["close"], timeperiod=n2)

    data[name1] = ema1
    data[name2] = ema2
    return data[[name1]], data[[name2]]



# Backtesting ============================================================

from backtesting import Strategy
from backtesting.lib import crossover


class SmaCross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    n2 = 20

    def init(self):
        # Precompute two moving averages
        self.sma1 = ema_calculation(self, n1=n1, n2=n2)[0]
        self.sma2 = ema_calculation(self, n1=n1, n2=n2)[1]

    def next(self):
        # If sma1 crosses above sma2, buy the asset
        if crossover(self.sma1, self.sma2):
            self.buy()

        # Else, if sma1 crosses below sma2, sell it
        elif crossover(self.sma2, self.sma1):
            self.sell()

# --------------------- Running code -------------------------------
from backtesting import Backtest
if __name__ == "__main__":
    bt = Backtest(data, SmaCross(0, data), cash=10000, commission = .002)

    print(bt.run())



