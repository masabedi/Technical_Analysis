import data_catcher.history as history
import pandas as pd
import talib


sahamyab_data = history.sahamyab_dataframe("وغدیر", 12)
db_data = history.database_dataframe()

data = db_data

# columns = ['time', 'close', 'high', 'low', 'open', 'value']
# end date is 1398/10/10  = 1577750400

# General functions


def profit_calculation(data, signal_column_name: str):
    buy_price = 0
    buy_count = 0
    sell_price = 0
    sell_count = 0

    for i in range(len(data)):
        if data.loc[i, signal_column_name] == 'buy':
            buy_price += data.loc[i, 'close']
            buy_count += 1
        elif data.loc[i, signal_column_name] == 'sell':
            sell_price += data.loc[i, 'close']
            sell_count += 1
    average_buy = buy_price / buy_count
    average_sell = sell_price / sell_count
    profit = ((average_sell - average_buy) / average_buy) * 100
    return profit


def range_signal_calculator(data: pd.DataFrame, indicator: str, overbought_range: int, oversold_range: int):

    signal = indicator + "_signal"
    data[signal] = None
    period = len(data) - 1

    def indicator_value(data, range, row):
        value = data.loc[range, [row]]
        item = value.item()
        return item

    for i in range(period):
        trend = str
        period0 = period - (i + 1)
        period1 = period - i

        buy = bool((indicator_value(data, period0, indicator) < oversold_range) and (
                indicator_value(data, period1, indicator) > oversold_range))

        sell = bool((indicator_value(data, period0, indicator) < overbought_range) and (
                indicator_value(data, period1, indicator) > overbought_range))
        if buy:
            trend = 'buy'

        elif sell:
            trend = 'sell'
        else:
            trend = '-'

        data.loc[period1, signal] = trend

    return data


def cross_signal_calculation(data: pd.DataFrame, indicator: str, first_line: str, second_line: str):
    signal = indicator + "_signal"
    data[signal] = None
    period = len(data) - 1

    def indicator_value(data, range, row):
        value = data.loc[range, [row]]
        item = value.item()
        return item

    for i in range(period):
        trend = str
        period0 = period - (i + 1)
        period1 = period - i

        if (indicator_value(data, period0, first_line ) < indicator_value(data, period0, second_line) and
        indicator_value(data, period1, first_line) > indicator_value(data, period1, second_line)):
            trend = "buy"

        elif (indicator_value(data, period0, first_line ) > indicator_value(data, period0, second_line) and
        indicator_value(data, period1, first_line) < indicator_value(data, period1, second_line)):
            trend = "sell"

        else:
            trend = "-"
        data.loc[period1, signal] = trend
    data.loc[0, signal] = "-"
    return data


def amount_signal_calculation(data:pd.DataFrame, indicator:str, base_value:int):
    signal = indicator + "_signal"
    data[signal] = None
    period = len(data) - 1

    def indicator_value(data, range, row):
        value = data.loc[range, [row]]
        item = value.item()
        return item

    for i in range(period):
        trend = str
        period0 = period - (i + 1)
        period1 = period - i

        if (indicator_value(data, period0, indicator) < base_value) and (indicator_value(data, period1, indicator) > base_value) :
            trend = "buy"

        elif (indicator_value(data, period0, indicator) > -base_value) and (indicator_value(data, period1, indicator) < -base_value) :
            trend = "sell"

        else:
            trend = "-"

        data.loc[period1, signal] = trend


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







