from Indicators import indicators
import tools.jalali as jalali
import data_catcher.history as history
import pandas as pd


# sahamyab_data = history.sahamyab_dataframe("وغدیر", 12)
db_data = history.database_dataframe()

data = db_data


def persian_date(data):
    persian = []
    for i in range(len(data.index)):
        gregorian_date = (data.index[i]).date()
        persian_date = jalali.Gregorian(gregorian_date).persian_string()
        persian.append(persian_date)
    data.index = persian
    return data


# SIGNAL CALCULATORS ============================================================

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



def cross_signal(series1: pd.DataFrame, series2: pd.DataFrame):
    signal = str(series1.columns.values[0]) + "_" + str(series2.columns.values[0]) +"_cross"
    data = pd.concat([series1,series2], axis=1, sort=False)
    data[signal] = None
    period = len(series1) - 1

    def series_value(data, range):
        value = data.iloc[range, :]
        item = value.values[0]
        return item

    for i in range(period):
        trend = str
        period0 = period - (i + 1)
        period1 = period - i

        if (series_value(series1, period0) < series_value(series2, period0) and
        series_value(series1, period1) > series_value(series2, period1)):
            trend = "buy"

        elif (series_value(series1, period0) > series_value(series2, period0) and
        series_value(series1, period1) < series_value(series2, period1)):
            trend = "sell"

        else:
            trend = "-"
        data.iloc[period1, 2] = trend
    data.iloc[0, 2] = "-"
    return data

def center_signal(series1: pd.DataFrame):
    series1["zero"] = 0
    series2 = pd.DataFrame(data=series1["zero"])
    signal = str(series1.columns.values[0]) + "_zero" +"_cross"
    data = pd.DataFrame(data=series1)
    data[signal] = None
    period = len(series1) - 1

    def series_value(data, range):
        value = data.iloc[range, :]
        item = value.values[0]
        return item

    for i in range(period):
        trend = str
        period0 = period - (i + 1)
        period1 = period - i

        if (series_value(series1, period0) < series_value(series2, period0) and
        series_value(series1, period1) > series_value(series2, period1)):
            trend = "buy"

        elif (series_value(series1, period0) > series_value(series2, period0) and
        series_value(series1, period1) < series_value(series2, period1)):
            trend = "sell"

        else:
            trend = "-"
        data.iloc[period1, 2] = trend
    data.iloc[0, 2] = "-"
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


# DATA PREPARING ============================================================

# Date converting

data = persian_date(data)

# EMA
def ema_signal(data, period1, period2):

    ema1 = indicators.ema_calculation(data,period1)
    ema2 = indicators.ema_calculation(data, period2)
    ema_signal = cross_signal(ema1, ema2)
    return ema_signal

# MACD
def macd_signal(data, fastperiod=12, slowperiod=26, signalperiod=9):
    macd = indicators.macd_calculation(data, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
    signal1 = cross_signal(macd[0], macd[1])
    signal2 = center_signal(macd[0])
    signal_lst = [
        signal1[str(signal1.columns[0])],
        signal1[str(signal1.columns[1])],
        signal1[str(signal1.columns[2])],
        signal2[str(signal2.columns[2])]
    ]
    signal_pd = pd.DataFrame(data=signal_lst)
    return signal_pd.T

#


if __name__ == "__main__":
    print(macd_signal(data))
    print(ema_signal(data, 5, 30))



