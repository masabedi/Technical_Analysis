import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -  %(levelname)s -  %(message)s')
logging.disable()
data = [10,9,10,10,9,8]
remove_data=[]
for i in data:
    if data.count(i) == 1:
        remove_data.append(i)
logging.debug('remove_data = %s' %remove_data)
for i in remove_data:
    data.remove(i)
print(data)


