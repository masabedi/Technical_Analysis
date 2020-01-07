import data_catcher.history as history
import json

import mysql.connector
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '19@mY%718',
    database = 'sahamyab',
)

mycursor = mydb.cursor()

def add_to_database(data, symbol):
    # this function add data to symbols table

    sqlstuff = "INSERT INTO prices (symbol, time, close, high, low, open, value) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    records = []
    for i in range(len(data.get("t"))):
        symbol = symbol
        time = data.get("t")[i]
        close = data.get("c")[i]
        high = data.get("h")[i]
        low = data.get("l")[i]
        open = data.get("o")[i]
        value = data.get("v")[i]

        item = (symbol, time, close, high, low, open, value)
        records.append(item)

    my_cursor.executemany(sqlstuff, records)
    mydb.commit()

def get_data_mysql(row):
    command = "SELECT " + row + " FROM prices"
    mycursor.execute(command)
    data = mycursor.fetchall()
    return data

def get_last_data(row):
    command = "SELECT " + row + " FROM prices ORDER BY id DESC LIMIT 1"
    mycursor.execute(command)
    data = mycursor.fetchall()
    return data[0][0]


#TODO add update database process




if __name__ == "__main__":

    last_data = get_last_data("time")
    symbol = "وغدیر"
    data = history.get_data_period(symbol=symbol, from_date=last_data)
    # data = history.get_data(symbol, 1)
    print(data)