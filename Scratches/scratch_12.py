import re, os
os = os.name
test = '<td><a target="_blank" href="/instrument/پرداخت1_IRO1PRKT0001.html" class="ng-binding">پرداخت1</a></td>'
if os == 'Darwin':
    file = open('/Users/masoudabedi/PycharmProjects/Web scraping/tsm_data.html', encoding="utf8")
else:
    file = open('C:\Python\data.html', encoding="utf8")
file_read = file.read()
links_compile = re.compile(r'instrument/\w*.html')
names_compile = re.compile(r'"ng-binding">\w*')
links = links_compile.findall(file_read)
names = names_compile.findall(file_read)
namad = []

ids = []
for i in links:
    name = re.compile(r't/\w*_')
    id = re.compile(r'_\w*.')
    namad.append(name.findall(i))
    ids.append(id.findall(i))
print(namad)
print(ids)
print(links)
print(names)
print(len(links))