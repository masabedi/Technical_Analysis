import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s  -  %(message)s')
logging.disable()

import pandas as pd
import requests
# for getting data
from datetime import datetime
# for getting date time
from dateutil.relativedelta import relativedelta
# for going many years or month we want to the past
import json
import pandas as pd

import mysql.connector
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '19@mY%718',
    database = 'sahamyab',
)

mycursor = mydb.cursor()




def going_past(month):
    time = datetime.now()
    month_count = month
    relative_month = time - relativedelta(months=month_count)
    relative_month_timestamp = datetime.timestamp(relative_month)
    return relative_month_timestamp

def get_data(symbol, history_months:int, resolution="D"):
    from_date = int(going_past(history_months))
    to_date = int(going_past(0))
    url =  "https://www.sahamyab.com/guest/tradingview/history?adjustment=&symbol=" + str(symbol) + "&resolution=" + str(resolution) + "&from=" + str(from_date) + "&to=" + str(to_date)
    response = requests.get(url=url)
    json_file = response.json()
    return json_file

def get_data_period(symbol, from_date, resolution="D"):
    logging.debug("from = %s" %from_date)
    to_date = datetime.now()
    to_date = int(datetime.timestamp(to_date))
    logging.debug(("to = %s" %to_date))
    url =  "https://www.sahamyab.com/guest/tradingview/history?adjustment=&symbol=" + str(symbol) + "&resolution=" + str(resolution) + "&from=" + str(from_date) + "&to=" + str(to_date)
    logging.debug(" URL = %s" %url)
    response = requests.get(url=url)
    json_file = response.json()
    return json_file

def date_convertor(timestapm_columns:pd.DataFrame):
    index = timestapm_columns
    for i in range(len(index)):
        date = int(index[i])
        index[i] = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
    index = index.astype("datetime64")
    return index



# keys = t, c, h, l, v

# def add_to_dataframe(data:dict):
#     df = pd.DataFrame(columns=["time", "close", "high", "low", "open", "value"])
#     df["time"] = data.get("t")
#     df["close"] = data.get("c")
#     df["high"] = data.get("h")
#     df["low"] = data.get("l")
#     df["open"] = data.get("o")
#     df["value"] = data.get("v")
#     return df

# test lines -----------------
# file = "/Users/masoudabedi/Desktop/Sahamyab/prices.json"
#
# with open(file) as j_file:
#     data = json.load(j_file)
#
#
# # Create a table ------------------------
#
# my_cursor.execute("CREATE TABLE prices (symbol VARCHAR(255), "
#                   "time VARCHAR(255), "
#                   "close INTEGER(10), "
#                   "high INTEGER(10), "
#                   "low INTEGER(10), "
#                   "open INTEGER(10), "
#                   "value INTEGER,"
#                   "id INTEGER AUTO_INCREMENT PRIMARY key) ")
# -------------------------------



# ------------------------------ Convert Data from database -----------------------------------------

def get_data_mysql(row):
    command = "SELECT " + row + " FROM prices"
    mycursor.execute(command)
    data = mycursor.fetchall()
    return data

# convert data from database to panda data frame
def database_convertor(data):
    columns = ["Date", "Open", "High", "Low", "Close", "Volume"]

    df = pd.DataFrame(columns=columns)
    for i in data:
        time = i[1]
        close = i[2]
        high = i[3]
        low = i[4]
        open = i[5]
        volume = i[6]
        item = [time, open, high, low, close, volume]
        append_df = pd.DataFrame([item], columns=columns)
        df = df.append(append_df, ignore_index=True)
    date = date_convertor(df["Date"])
    df.index = date
    df = df.drop(columns=["Date"])
    return df

# make data frame
def database_dataframe():
    db_data = get_data_mysql("*")
    database_data = database_convertor(db_data)
    return database_data


# ------------------------------ Convert Data from Sahamyab -----------------------------------------

# convert data from sahamyab to panda data frame
def sahamyab_convertor(data:dict):
    df = pd.DataFrame(index=[],columns=["Date","Open","High","Low","Close","Volume"])

    df["Date"] = data.get("t")
    df["Close"] = data.get("c")
    df["High"] = data.get("h")
    df["Low"] = data.get("l")
    df["Open"] = data.get("o")
    df["Volume"] = data.get("v")

    # set time for index because refference of each record is its date
    # first we should convert timestamp to date time format
    date = date_convertor(df["Date"])
    df.index = date
    df = df.drop(columns=["Date"])
    return df

# make data frame
def sahamyab_dataframe(symbol, months):
    sy_data = get_data(symbol=symbol, history_months=months)
    sahamyab_data = sahamyab_convertor(sy_data)
    return sahamyab_data



if __name__ == "__main__":

    symbol = "وغدیر"
    sahamyab_data = sahamyab_dataframe(symbol, 1)
    # db_data = database_dataframe()

    data = sahamyab_data

    # data = get_data(symbol, 1)

    print(data)

