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






def going_past(month):
    time = datetime.now()
    month_count = month
    relative_month = time - relativedelta(months=month_count)
    relative_month_timestamp = datetime.timestamp(relative_month)
    return relative_month_timestamp


def get_data(symbol, history_months, resolution="D"):
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




if __name__ == "__main__":

    symbol = "وغدیر"
    data = get_data(symbol, 1)
    print(data)


