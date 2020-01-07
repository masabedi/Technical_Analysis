import sahamyab.sahamyab_symbol_history as history
symbol = "وغدیر"


if __name__ == "__main__":

    data = history.get_data(symbol, 24)
    history.add_to_database(data, symbol)


































