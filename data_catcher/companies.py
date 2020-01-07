import requests
import mysql.connector

# data links
paye_faraburs = "https://www.sahamyab.com/api/proxy/symbol/stockWatch?v=0.1&namad=&market=4&type=&sector=&page=0&pageSize=2000&sort=&"
faraburs = "https://www.sahamyab.com/api/proxy/symbol/stockWatch?v=0.1&namad=&market=2&type=&sector=&page=0&pageSize=2000&sort=&"
burs = "https://www.sahamyab.com/api/proxy/symbol/stockWatch?v=0.1&namad=&market=1&type=&sector=&page=0&pageSize=2000&sort=&"
links = [burs, faraburs, paye_faraburs]





# connecting to database
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '19@mY%718',
    database = 'sahamyab',
)

my_cursor = mydb.cursor()

# creating a table
# my_cursor.execute("CREATE TABLE companies ("
#                   "sector VARCHAR(255),"
#                   " symbol VARCHAR(255),"
#                   " name VARCHAR(255),"
#                   " isin VARCHAR(255),"
#                   " type INTEGER(10),"
#                   " market VARCHAR(255),"
#                   " id INTEGER AUTO_INCREMENT PRIMARY key)")



keys = ['id', 'InsCode', 'type', 'pushId', 'name', 'title', 'corpName', 'sectionName', 'subSectionName',
        'status', 'date', 'q_status', 'tradeCount', 'tradeVolume', 'tradeTotalPrice', 'maxPrice',
        'minPrice', 'firstPrice', 'closingPrice', 'lastPrice', 'yesterdayPrice', 'bestLimits',
        'sellCountInd', 'sellCountCorp', 'sellVolumeInd', 'sellVolumeCorp', 'buyCountInd',
        'buyCountCorp', 'buyVolumeInd', 'buyVolumeCorp', 'market', 'baseVolume', 'marketValue',
        'totalCount', 'minAllowPrice', 'maxAllowPrice', 'minAllowVolume', 'maxAllowVolume',
        'estimatedEPS', 'PE', 'sectorPE', 'stockholders', 'insCode', 'description', 'namad',
        'flow', 'sector', 'subsector', 'tradeDate', 'price', 'tradeValue', 'priceChange',
        'priceChangeClosing', 'indCount', 'indVolume', 'indValue', 'corpCount', 'corpVolume',
        'corpValue', 'priceChange_1', 'priceChange_7', 'priceChange_30', 'priceChange_91', 'priceChange_182', 'priceChange_365']

# sector = sectionName
# symbol = name
# name = title
# isin = id
# type = type
# market = market

def get_company_data(companies_data, id):
    sector = companies_data[id].get("sectionName")
    symbol = companies_data[id].get("name")
    name = companies_data[id].get("title")
    isin = companies_data[id].get("id")
    type = companies_data[id].get("type")
    market = companies_data[id].get("market")

    records = [sector, symbol, name, isin, type, market]

    return records


def add_to_database(companies):
    # this function add data to symbols table

    sqlstuff = "INSERT INTO companies (sector, symbol, name, isin, type, market) VALUES (%s, %s, %s, %s, %s, %s)"
    records = []
    for i in companies:
        sector = str(i.get("sectionName"))
        symbol = str(i.get("name"))
        name = str(i.get("title"))
        isin = str(i.get("id"))
        type = int(i.get("type"))
        market = str(i.get("market"))

        item = (sector, symbol, name, isin, type, market)
        records.append(item)

    my_cursor.executemany(sqlstuff, records)
    mydb.commit()



def update_companies(links):

    # deleting table content
    my_sql = "DELETE FROM companies"
    my_cursor.execute(my_sql)
    mydb.commit()

    # getting new data
    for i in links:

        response = requests.get(url=i)
        data = response.json()

        companies = data.get("items")

        add_to_database(companies)


if __name__ == "__main__":
    update_companies(links)



