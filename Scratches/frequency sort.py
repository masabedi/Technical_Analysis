import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s -  %(levelname)s -  %(message)s')
a = [1,2,1,2]
b = [4,6,2,2,6,4,4,4]
c = ['bob','bob','carl','alex','bob']
d = [17,99,42]
def count_items(item : list):
    items_sets = []
    for i in item:
        items_sets.append((item.count(i)))
    items_sets = set(items_sets)
    return items_sets

def frequency_sort(items):
    for i in items:
        if items.count(i)==1:
            items = items
        elif len(count_items(items)) ==1 :
                items = sorted(items, key=lambda x: (items.count(x), x))

        else:
            items = sorted(items,key=lambda x: (items.count(x), x), reverse=True)


    return items

print(frequency_sort(a))
print(frequency_sort(b))
print(frequency_sort(c))
print(frequency_sort(d))






