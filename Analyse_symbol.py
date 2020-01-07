import sahamyab.sahamyab_symbol_history as history
import mysql.connector
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '19@mY%718',
    database = 'sahamyab',
)

mycursor = mydb.cursor()

# ------------------------------ MySql Guide -----------------------------------------

# SELECT (column) FROM (table) WHERE




if __name__ == "__main__":

    last_data = int(get_last_data("time"))
    print(last_data)

    symbol = 'وغدیر'
    data = history.get_data_period(symbol, from_date=last_data)
    print(data)



