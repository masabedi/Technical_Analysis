from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen('http://tse.ir/listing.html?cat=cash&section=alphabet')
bsObj = BeautifulSoup(html,features='lxml')

for child in bsObj.find("div",{"id":"alphabetView"}).tr.next_siblings:
    print(child)