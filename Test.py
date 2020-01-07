import pandas as pd
import logging
import ta
import platform
from scipy.stats import linregress
import matplotlib

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s  -  %(message)s')

# isin = 'IRO1GDIR0000 : Ghadir'


file_name = 'IRO1GDIR0000.csv'

# Seprating OS
os_system = platform.system()

if os_system == 'Darwin':
    modified_directory = r'/Users/masoudabedi/Documents/TseClient - Modified'
    indicators_directory = r'/Users/masoudabedi/Documents/Indicators'

    file = modified_directory + '/' + file_name
    indicators_file = indicators_directory + '/' + 'Indicators-' + file_name

else:
    modified_directory = r"C:\Users\masou\Documents\TseClient - Modified"
    indicators_directory = r"C:\Users\masou\Documents\Indicators"

    file = modified_directory + '\\' + file_name
    indicators_file = indicators_directory + '\\' + 'Indicators-' + file_name

csv = pd.read_csv(file)

#  Columns = ['date_time'	'open_price'	'high_price'	'low_price'	'real_close_price'	'volume']



# Definig period from last data
period_range = len(csv)
last_data = int(csv.count()[0])-1
period = []
for i in range(period_range):
    period.append(last_data - i)

period = period[::-1]

csv = pd.read_csv(file)

# =============================================== FUNCTION SECTION =====================================================

# this function calculate signal based on a oversold and overbought range
def signal_calculation(df: pd.DataFrame, indicator: str, signal: str, overbought_range, oversold_range):
    df[signal] = None

    for i in range(len(period)):
        trend = str
        buy = bool((df.loc[period[i - 1], [indicator]].item() < oversold_range) and (
                df.loc[period[i], [indicator]].item() > oversold_range))
        sell = bool((df.loc[period[i - 1], [indicator]].item() > overbought_range) and (
                df.loc[period[i], [indicator]].item() < overbought_range))

        if buy:
            trend = 'Buy'
        elif sell:
            trend = 'Sell'
        else:
            trend = '-'

        csv.loc[period[i], signal] = trend

# this function calculate signal based on crossing a signal line
def cross_calculation(df: pd.DataFrame, indicator: str, signal_line: str, signal: str):
    df[signal] = None

    for i in range(len(period)):
        trend = str
        buy = bool((df.loc[period[i - 1], [indicator]].item() < df.loc[period[i - 1], [signal_line]].item()) and
                   (df.loc[period[i], [indicator]].item() > df.loc[period[i], [signal_line]].item()))
        sell = bool((df.loc[period[i - 1], [indicator]].item() > df.loc[period[i - 1], [signal_line]].item()) and
                    (df.loc[period[i], [indicator]].item() < df.loc[period[i], [signal_line]].item()))

        if buy:
            trend = 'Buy'
        elif sell:
            trend = 'Sell'
        else:
            trend = '-'

        csv.loc[period[i], signal] = trend

# this function calculate profit of a signal
def profit_calculation(df: pd.DataFrame, signal: str):
    buy_price = 0
    buy_count = 0
    sell_price = 0
    sell_count = 0

    for i in range(len(df)):
        if df.loc[i, signal] == 'Buy':
            buy_price += df.loc[i, 'real_close_price']
            buy_count += 1
        elif df.loc[i, signal] == 'Sell':
            sell_price += df.loc[i, 'real_close_price']
            sell_count += 1
    average_buy = buy_price / buy_count
    average_sell = sell_price / sell_count
    profit = ((average_sell - average_buy) / average_buy) * 100

    print(f'\n{signal}')
    print(f'Profit = {profit:.1f}%')

    return profit

# this function calculate highs and lows of price and indicator
def high_low_calculation(df: pd.DataFrame, column_name: str, high_low_column_name: str):
    df[high_low_column_name + '_highs'] = None
    df[high_low_column_name + '_lows'] = None

    for i in range(2, len(df)):
        low_point = bool((df.loc[i - 1, [column_name]].item() < df.loc[i, [column_name]].item()) and
                         (df.loc[i - 1, [column_name]].item() < df.loc[i - 2, [column_name]].item()))
        high_point = bool((df.loc[i - 1, [column_name]].item() > df.loc[i, [column_name]].item()) and
                          (df.loc[i - 1, [column_name]].item() > df.loc[i - 2, [column_name]].item()))
        if low_point:
            df.loc[i - 1, [high_low_column_name + '_lows']] =  df.loc[i - 1, [column_name]].item()
        elif high_point:
            df.loc[i - 1, [high_low_column_name + '_highs']] =  df.loc[i - 1, [column_name]].item()
        else:
            df.loc[i - 1, [high_low_column_name + '_highs']] = None
            df.loc[i - 1, [high_low_column_name + '_lows']] = None
    return df[high_low_column_name + '_highs'] , df[high_low_column_name + '_lows']


# this function slope of a given number of highs and lows and can be used for divergence identification
def slope_calculation(df:pd.DataFrame, high_low:str, high_low_column_name:str, column_name:str, slope_range:int):
    high_low_df = pd.DataFrame(index=['index', high_low_column_name, 'quantity'])
    for i in range(len(df)):
        if csv.loc[i, [high_low_column_name]].item() == high_low:
            high_low_df = high_low_df.append([{'index': int(i), high_low: df.loc[i, high_low_column_name], 'quantity': df.loc[i, column_name]}],
                                 ignore_index=True)
    x = [i for i in range(1, slope_range + 1)]
    y = []
    for i in range(slope_range):
        y.append(high_low_df.loc[((len(high_low_df) - 1) - i), 'quantity'])

    y = y[::-1]
    regres = linregress(x, y)
    # can return high_low_df
    return regres[0], y

# modifying overbought and oversold areas to produce enough signal
def modify_overbought_oversold_area(dataframe:pd.DataFrame, indicator_column_name:str, signal_column_name:str, overbought_range:int, oversold_range:int):
    signal_calculation(dataframe, indicator_column_name, signal_column_name, overbought_range, oversold_range)
    global overbought
    global oversold
    count_dict = dataframe[signal_column_name].value_counts().to_dict()
    while ('Sell' not in count_dict) or ('Buy' not in count_dict):
        if 'Sell' not in count_dict:
            overbought_range -= 1
        elif 'Buy' not in count_dict:
            oversold_range += 1
        elif ('Sell' not in count_dict) and ('Buy' not in count_dict):
            overbought_range -= 1
            oversold_range += 1

        signal_calculation(dataframe, indicator_column_name, signal_column_name, overbought_range, oversold_range)

        count_dict = dataframe[signal_column_name].value_counts().to_dict()

    overbought = overbought_range
    oversold = oversold_range

# maximize profit by changing overbought and oversold range
def maximize_profit_range(dataframe:pd.DataFrame, indicator_column_name:str, signal_column_name:str, overbought_range:int, oversold_range:int):
    modify_overbought_oversold_area(dataframe, indicator_column_name, signal_column_name, overbought_range, oversold_range)

    profit = profit_calculation(dataframe,signal_column_name)

    temp_overbought_range = overbought_range
    temp_oversold_range = oversold_range

    profit_list = [[profit, overbought_range, oversold_range]]
    for i in range(10):

        temp_oversold_range = oversold_range
        for i in range(10):
            logging.debug('overbought = %s' % temp_overbought_range)
            logging.debug('oversold = %s' % temp_oversold_range)
            signal_calculation(dataframe, indicator_column_name, signal_column_name, temp_overbought_range, temp_oversold_range)
            profit = profit_calculation(dataframe,signal_column_name)
            profit_list.append([profit, temp_overbought_range, temp_oversold_range])
            temp_oversold_range += 1
        temp_overbought_range -= 1

    max_profit = max([x[0] for x in profit_list])
    for i in profit_list:
        if i[0] == max_profit:
            overbought_range = i[1]
            oversold_range = i[2]
            profit = i[0]

    signal_calculation(dataframe, indicator_column_name, signal_column_name, overbought_range, oversold_range)
    # overbought = function[0]
    # oversold = function[1]
    # profit = function[0]


    return overbought_range, oversold_range, profit


# ===============================================IDICATORS AREA=========================================================

# ++++++++++++++++++++++++++++++++++++++++++++++++ RSI INDICATOR +++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

Overbought - Oversold : When momentum and price rise fast enough, at a high enough level, eventual the security will be considered overbought.
When price and momentum fall far enough they can be considered oversold.

Traditional overbought territory starts above 80 and oversold territory starts below 20.
These values are subjective however, and a technical analyst can set whichever thresholds they choose.

"""
rsi = ta.rsi(csv['real_close_price'], fillna=True)
csv['rsi'] = rsi


# Trend identifying

overbought_range = 80
oversold_range = 20



# max = maximize_profit_range(csv, 'rsi', 'rsi_signal', overbought_range, oversold_range)
# print(max)

highs = high_low_calculation(csv, 'real_close_price', 'rcp_hl')[0]
lows = high_low_calculation(csv, 'real_close_price', 'rcp_hl')[1]
highs = highs.dropna()
highs = highs.reset_index()
lows = lows.dropna()
lows = lows.reset_index()
matplotlib.


# csv = csv.drop(columns=['rsi'])

# ================================================== Writing to CSV ====================================================
csv = csv.drop(columns=['open_price', 'high_price', 'low_price', 'volume'])
csv.to_csv(indicators_file, encoding='utf-8-sig',  index=False)




