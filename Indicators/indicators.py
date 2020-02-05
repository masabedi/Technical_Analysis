import datetime
# import data_catcher.history as history
import pandas as pd
import talib

# sahamyab_data = history.sahamyab_dataframe("وغدیر", 12)
# db_data = history.database_dataframe()
#
# data = db_data

# columns = ['time', 'Close', 'High', 'Low', 'Open', 'value']
# end date is 1398/10/10  = 1577750400

# General functions ============================================================


def profit_calculation(data, signal_column_name: str):
    buy_price = 0
    buy_count = 0
    sell_price = 0
    sell_count = 0

    for i in range(len(data)):
        if data.loc[i, signal_column_name] == 'buy':
            buy_price += data.loc[i, 'Close']
            buy_count += 1
        elif data.loc[i, signal_column_name] == 'sell':
            sell_price += data.loc[i, 'Close']
            sell_count += 1
    average_buy = buy_price / buy_count
    average_sell = sell_price / sell_count
    profit = ((average_sell - average_buy) / average_buy) * 100
    return profit

def date_convertor(timestapm_columns):
    index = timestapm_columns
    for i in range(len(index)):
        date = int(index[i])
        index[i] = datetime.datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
    return index


# # SIGNAL CALCULATORS ============================================================
#
# def range_signal_calculator(data: pd.DataFrame, indicator: str, overbought_range: int, oversold_range: int):
#
#     signal = indicator + "_signal"
#     data[signal] = None
#     period = len(data) - 1
#
#     def indicator_value(data, range, row):
#         value = data.loc[range, [row]]
#         item = value.item()
#         return item
#
#     for i in range(period):
#         trend = str
#         period0 = period - (i + 1)
#         period1 = period - i
#
#         buy = bool((indicator_value(data, period0, indicator) < oversold_range) and (
#                 indicator_value(data, period1, indicator) > oversold_range))
#
#         sell = bool((indicator_value(data, period0, indicator) < overbought_range) and (
#                 indicator_value(data, period1, indicator) > overbought_range))
#         if buy:
#             trend = 'buy'
#
#         elif sell:
#             trend = 'sell'
#         else:
#             trend = '-'
#
#         data.loc[period1, signal] = trend
#
#     return data
#
# def cross_signal_calculation(data: pd.DataFrame, indicator: str, first_line: str, second_line: str):
#     signal = indicator + "_signal"
#     data[signal] = None
#     period = len(data) - 1
#
#     def indicator_value(data, range, row):
#         value = data.loc[range, [row]]
#         item = value.item()
#         return item
#
#     for i in range(period):
#         trend = str
#         period0 = period - (i + 1)
#         period1 = period - i
#
#         if (indicator_value(data, period0, first_line ) < indicator_value(data, period0, second_line) and
#         indicator_value(data, period1, first_line) > indicator_value(data, period1, second_line)):
#             trend = "buy"
#
#         elif (indicator_value(data, period0, first_line ) > indicator_value(data, period0, second_line) and
#         indicator_value(data, period1, first_line) < indicator_value(data, period1, second_line)):
#             trend = "sell"
#
#         else:
#             trend = "-"
#         data.loc[period1, signal] = trend
#     data.loc[0, signal] = "-"
#     return data
#
# def amount_signal_calculation(data:pd.DataFrame, indicator:str, base_value:int):
#     signal = indicator + "_signal"
#     data[signal] = None
#     period = len(data) - 1
#
#     def indicator_value(data, range, row):
#         value = data.loc[range, [row]]
#         item = value.item()
#         return item
#
#     for i in range(period):
#         trend = str
#         period0 = period - (i + 1)
#         period1 = period - i
#
#         if (indicator_value(data, period0, indicator) < base_value) and (indicator_value(data, period1, indicator) > base_value) :
#             trend = "buy"
#
#         elif (indicator_value(data, period0, indicator) > -base_value) and (indicator_value(data, period1, indicator) < -base_value) :
#             trend = "sell"
#
#         else:
#             trend = "-"
#
#         data.loc[period1, signal] = trend


# Indicators ============================================================


# Bollinger Bands (BB)

def bollinger_calculation(data):
    name1 = "bollinger_upperband"
    name2 = "bollinger_middleband"
    name3 = "bollinger_Lowerband"

    upperband, middleband, Lowerband = talib.BBANDS(data["Close"], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    data[name1] = upperband
    data[name2] = middleband
    data[name3] = Lowerband

    return data[[name1, name2, name3]]

# Average True Range (ATR)
def atr_calculation(data, timeperiod=14):
    name = "atr"
    atr = talib.ATR(data["High"], data["Low"], data["Close"], timeperiod=timeperiod)
    data[name] = atr
    return data[[name]]

# EMA
def ema_calculation(data, n=5):
    name = "ema" + str(n)
    ema = talib.EMA(data["Close"], timeperiod=n)
    data[name] = ema
    return data[[name]]


# SMA
def sma_calculation(data, n=30):
    name = "sma" + str(n)
    sma = talib.SMA(data["Close"], timeperiod=n)
    data["Close"] = sma
    return data["Close"]


# Moving Average Convergence Divergence (MACD)
def macd_calculation(data, fastperiod=12, slowperiod=26, signalperiod=9):
    name1 = "macd"
    name2 = "macdsignal"
    name3 = "macdhist"

    macd, macdsignal, macdhist = talib.MACD(data["Close"], fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)

    data[name1] = macd
    data[name2] = macdsignal
    data[name3] = macdhist
    return data[[name1]], data[[name2]], data[[name3]]

# Average Directional Movement Index (ADX)
def adx_calculator(data, timeperiod=14):
    name1 = "adx"

    adx = talib.ADX(data["High"], data["Low"], data["Close"], timeperiod=timeperiod)

    data[name1] = adx

    return data[[name1]]

# Commodity Channel Index (CCI)
def cci_calculation(data, timeperiod=14):
    name = "cci"
    cci = talib.CCI(data["High"], data["Low"], data["Close"], timeperiod=timeperiod)
    data[name] = cci
    return data[[name]]

# Parabolic Stop And Reverse (Parabolic SAR)
def sar_calculation(data, acceleration=0.02, maximum=0.2):
    name = "sar"
    sar = talib.SAR(data["High"], data["Low"], acceleration=acceleration, maximum=maximum)
    data[name] = sar

    return data[[name]]

# Aroon
# TODO calculate other stages
def aroon_calculator(data, timeperiod=14):
    name1 = "aroonup"
    name2 = "aroondown"
    aroondown, aroonup = talib.AROON(data["High"], data["Low"], timeperiod=timeperiod)

    data[name1] = aroonup
    data[name2] = aroondown
    return data[[name1, name2]]


# Stochastic Oscillator (SR)
def stoch_caclulation(data, fastk_period=5, sLowk_period=3, sLowk_matype=0, sLowd_period=3,
                         sLowd_matype=0):
    name1 = "stoch_sLowk"
    name2 = "stoch_sLowd"

    sLowk, sLowd = talib.STOCH(data["High"], data["Low"], data["Close"], fastk_period=fastk_period, sLowk_period=sLowk_period, sLowk_matype=sLowk_matype, sLowd_period=sLowd_period,
                         sLowd_matype=sLowd_matype)
    data[name1] = sLowk
    data[name2] = sLowd

    return data[[name1, name2]]

# Relative Strength Index (RSI)
def rsi_calculation(data,timeperiod=14):
    name = "rsi"
    rsi = talib.RSI(data['Close'], timeperiod=timeperiod)
    data[name] = rsi
    return data[[name]]

# Williams %R (WR)
def williams_calculation(data, timeperiod=14):

    name = "williams"
    williams = talib.WILLR(data["High"], data["Low"], data["Close"], timeperiod=timeperiod)
    data[name] = williams
    return data[[name]]


# --------------------- Running code -------------------------------

if __name__ == "__main__":
    indicator = macd_calculation(data)
    print(indicator)







