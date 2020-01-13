import data_catcher.history as history
from ta import wrapper
from ta import trend
from ta import volatility
from ta import momentum
import pandas as pd

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

# EMA INDICATOR --------------------------------------------------------------------------------

"""
Short EMA cross up long Ema means an uptrend
Short EMA cross down long Ema means an downtrend
"""

def ema_calculation(data, n1=5, n2=35):
    name1 = "ema" + str(n1)
    name2 = "ema" + str(n2)
    ema1 = wrapper.EMAIndicator(data['close'], n=n1, fillna=True)
    ema2 = wrapper.EMAIndicator(data['close'], n=n2, fillna=True)
    data[name1] = ema1
    data[name2] = ema2
    return data, name1, name2

# MACD INDICATOR --------------------------------------------------------------------------------

"""
When the KST line is negative yet crosses above the signal line, upside momentum is increasing.
When the KST line is positive and crosses below the signal line, downside momentum is increasing.
"""

def macd_calculation(data):
    name1 = "macd"
    name2 = "macd_s"
    name3 = "macd_h"

    macd = trend.macd(data['close'], fillna=True)
    macd_signal = trend.macd_signal(data['close'], fillna=True)
    macd_diff = trend.macd_diff(data['close'], fillna=True)
    data[name1] = macd
    data[name2] = macd_signal
    data[name3] = macd_diff
    return data, name1, name2


#  RSI INDICATOR --------------------------------------------------------------------------------

"""
Overbought - Oversold : When momentum and price rise fast enough, at a high enough level, eventual the security will be considered overbought.
When price and momentum fall far enough they can be considered oversold.

Traditional overbought territory starts above 80 and oversold territory starts below 20.
These values are subjective however, and a technical analyst can set whichever thresholds they choose.
"""

def rsi_calculation(data):
    rsi = momentum.rsi(data['close'], 27, fillna=False)
    data['rsi'] = rsi
    return data



# +++++++++++++ SAR INDICATOR +++++++++++++

"""
"""

def sar_calculation(data):
    name1 = "sar_up"
    name2 = "sar_up_indicator"
    name3 = "sar_down"
    name4 = "sar_down_indicator"
    sar_up = trend.psar_up(data["high"], data["low"], data["close"])
    sar_up_indicator = trend.psar_up_indicator(data["high"], data["low"], data["close"])
    sar_down = trend.psar_down(data["high"], data["low"], data["close"])
    sar_down_indicator = trend.psar_up_indicator(data["high"], data["low"], data["close"])
    data[name1] = sar_up
    data[name2] = sar_up_indicator
    data[name3] = sar_down
    data[name4] = sar_down_indicator
    return data

# +++++++++++++ CCI INDICATOR +++++++++++++

"""
High reading 100 or above means uptrend is strong
Low reading -100 or below means downtrend is strong
Going from - or near zero to +100 can signal uptrend
Going from + or near zero to -100 can signal downtrend
"""

def cci_calculation(data):
    cci = trend.cci(data["high"], data["low"], data["close"], fillna=True)
    data["cci"] = cci
    return data



# +++++++++++++ STOCH INDICATOR +++++++++++++

"""
Overbought - Oversold : When momentum and price rise fast enough, at a high enough level, eventual the security will be considered overbought.
When price and momentum fall far enough they can be considered oversold.

Traditional overbought territory starts above 80 and oversold territory starts below 20.
These values are subjective however, and a technical analyst can set whichever thresholds they choose.
"""

def stoch_caclulation(data, n):
    name1 = "stoch"
    name2 = "stoch_signal"
    stoch = momentum.stoch(data["high"], data["low"], data["close"], n, fillna=True)
    stoch_signal = momentum.stoch_signal(data["high"], data["low"], data["close"], n, fillna=True)
    data[name1] = stoch
    data[name2] = stoch_signal

    return data, name1, name2

# +++++++++++++ AROON INDICATOR +++++++++++++

"""

Buy signal : 
stage 1 : aroon up move above aroon down
stage 2 : aroon up moves above 50
stage 3 : aroon-up reach 100 and aroon-down remain at low levels

Sell signal :
stage 1 : aroon-down move above aroon-up
stage 2 : aroon down moves above 50
stage 3 : aroon-down reach 100 and aroon-up remain at low levels

"""
# TODO calculate other stages
# def aroon_calculator(data, n):
#     name1 = "aroon_up"
#     name2 = "aroon_down"
#     aroon_up = ta.aroon_up(data["close"], n)
#     aroon_down = ta.aroon_down(data["close"], n)
#     data[name1] = aroon_up
#     data[name2] = aroon_down
#     return data, name1, name2



# +++++++++++++ WILLIAMS INDICATOR +++++++++++++


"""
bull : 
1- indicator < -80
2- indicator move above -50

bear :
1- indicator > -20
2- indicator move below -50
"""

def williams_calculation(data):
    williams = momentum.wr(data["high"], data["low"], data["close"], fillna=True)
    data["williams"] = williams
    return data


# +++++++++++++ STOCH.RSI INDICATOR +++++++++++++



# +++++++++++++ BOLLINGER INDICATOR +++++++++++++
"""
"""
def bollinger_calculation(data):
    name1 = "bollinger_h_band"
    name2 = "bollinger_h_indicator"
    name3 = "bollinger_l_band"
    name4 = "bollinger_l_indicator"
    name5 = "bollinger_m_band"
    bollinger_h = volatility.bollinger_hband(data["close"], fillna=True)
    bollinger_h_indicator = volatility.bollinger_hband_indicator(data["close"], fillna=True)
    bollinger_l = volatility.bollinger_lband(data["close"], fillna=True)
    bollinger_l_indicator = volatility.bollinger_lband_indicator(data["close"], fillna=True)
    bollinger_m_band = volatility.bollinger_mavg(data["close"], fillna=True)
    data[name1] = bollinger_h
    data[name2] = bollinger_h_indicator
    data[name3] = bollinger_l
    data[name4] = bollinger_l_indicator
    data[name5] = bollinger_m_band
    return data


# +++++++++++++ ADX INDICATOR +++++++++++++

"""
For Stocks like commodities and currencies (Volatile Stocks)
DI+ > DI- : Bull
DI+ < DI- : Bear
ADX < 20 : Weak or no trend
25 < ADX < 50 : Storng trend
50 < ADX < 75 : Very storng trend
75 < ADX < 100 : Exremely storng trend

"""

def adx_calculator(data):
    name1 = "adx"
    name2 = "adx_positive"
    name3 = "adx_negative"
    adx = trend.adx(data["high"], data["low"], data["close"], fillna=True)
    adx_positive = trend.adx_pos(data["high"], data["low"], data["close"], fillna=True)
    adx_negative = trend.adx_neg(data["high"], data["low"], data["close"], fillna=True)
    data[name1] = adx
    data[name2] = adx_positive
    data[name3] = adx_negative
    return data

# +++++++++++++ ATR INDICATOR +++++++++++++

"""

"""

def atr_calculation(data):
    atr = volatility.average_true_range(data["high"], data["low"], data["close"], fillna=True)
    data["atr"] = atr
    return atr




# --------------------- Running code -------------------------------

if __name__ == "__main__":
    atr = atr_calculation(data)
    print(atr)





