import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s -  %(levelname)s -  %(message)s')

array = [[[[[[[[[[4294967295]]]]]]]]]]
def appending(array):
    empty_list = []
    for i in array:
        if type(i) != int :
            for n in range(len(i)):
                empty_list.append(i[n])
        else:
            empty_list.append(i)
    array = empty_list
    return array
def flat_list(array):
    for i in range(20):
        array = appending(array)
    return array
print(flat_list(array))
logging.debug('end process')









