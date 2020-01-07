import data_catcher.history as history
import ta
import pandas as pd

sahamyab_data = history.sahamyab_dataframe("وغدیر", 12)
db_data = history.database_dataframe()

data = db_data

# columns = ['time', 'close', 'high', 'low', 'open', 'value']
# end date is 1398/10/10  = 1577750400



# +++++++++++++ EMA INDICATOR +++++++++++++
"""

Short EMA cross up long Ema means an uptrend
Short EMA cross down long Ema means an downtrend


"""


def ema_calculation(data, n1=5, n2=35):
    name1 = "ema" + str(n1)
    name2 = "ema" + str(n2)
    ema1 = ta.ema_indicator(data['close'], n=n1, fillna=True)
    ema2 = ta.ema_indicator(data['close'], n=n2, fillna=True)
    data[name1] = ema1
    data[name2] = ema2
    return data

def ema_signals(ema):
    ema['ema_signal'] = None
    period = len(ema)-1

    for i in range(len(ema)-1):
        trend = str
        if (int(ema.loc[period - (i+1) , ['ema5']]) < int(ema.loc[period - (i+1) , ['ema35']]) and
                int(ema.loc[period - i, ['ema5']]) > int(ema.loc[period - i, ['ema35']])):
            trend = 'buy'

        elif (int(ema.loc[period - (i + 1), ['ema5']]) > int(ema.loc[period - (i + 1), ['ema35']]) and

                int(ema.loc[period - i, ['ema5']]) < int(ema.loc[period - i, ['ema35']])):
            trend = 'sell'

        else:
            trend = '-'


        ema.loc[period - i , 'ema_signal'] = trend

    ema.loc[0, "ema_signal"] = "-"
    return ema

def profit_calculation(signal):
    buy_price = 0
    buy_count = 0
    sell_price = 0
    sell_count = 0

    for i in range(len(signal)):
        if signal.loc[i, 'ema_signal'] == 'buy':
            buy_price += signal.loc[i, 'close']
            buy_count += 1
        elif signal.loc[i, 'ema_signal'] == 'sell':
            sell_price += signal.loc[i, 'close']
            sell_count += 1
    average_buy = buy_price / buy_count
    average_sell = sell_price / sell_count
    profit = ((average_sell - average_buy) / average_buy) * 100
    return profit


# +++++++++++++ RSI INDICATOR +++++++++++++

# +++++++++++++ SAR INDICATOR +++++++++++++

# +++++++++++++ CCI INDICATOR +++++++++++++

# +++++++++++++ STOCH INDICATOR +++++++++++++

# +++++++++++++ AROON INDICATOR +++++++++++++

# +++++++++++++ MACD INDICATOR +++++++++++++

"""

When the KST line is negative yet crosses above the signal line, upside momentum is increasing.
When the KST line is positive and crosses below the signal line, downside momentum is increasing.


"""

def macd_calculation(data):
    macd = ta.macd(data['close'], fillna=True)
    macd_signal = ta.macd_signal(data['close'], fillna=True)
    macd_diff = ta.macd_diff(data['close'], fillna=True)
    data['macd'] = macd
    data['macd_signal'] = macd_signal
    data['macd_diff'] = macd_diff
    return data


def macd_trend(macd):
    data['macd_trend'] = None
    period = len(macd) - 1
    
    for i in range(len(macd)-1):
        trend = str

        if (int(macd.loc[period - (i + 1), ['macd']]) < int(macd.loc[period - (i + 1), ['macd_signal']]) and
                int(macd.loc[period - i, ['macd']]) > int(macd.loc[period - i, ['macd_signal']])):
            trend = 'bull'

        elif (int(macd.loc[period - (i + 1), ['macd']]) > int(macd.loc[period - (i + 1), ['macd_signal']]) and
              int(macd.loc[period - i, ['macd']]) < int(macd.loc[period - i, ['macd_signal']])):
            trend = 'bear'

        else:
            trend = '-'

        macd.loc[period - i, 'macd_trend'] = trend

    macd.loc[0, "macd_trend"] = "-"
    return macd
        



# +++++++++++++ WILLIAMS INDICATOR +++++++++++++

# +++++++++++++ STOCH.RSI INDICATOR +++++++++++++

# +++++++++++++ BOLLINGER INDICATOR +++++++++++++

# +++++++++++++ ADX INDICATOR +++++++++++++

# +++++++++++++ ATR INDICATOR +++++++++++++






if __name__ == "__main__":
    macd = macd_calculation(data)
    print(macd_trend(macd))


