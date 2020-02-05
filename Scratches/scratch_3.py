def import_data(n):
    file = open("numbers.txt", "r")
    number_file = file.readlines()
    pairs = []
    for i in range(n):
        new_item = number_file[i]
        new_set = list(map(str, new_item.split()))
        pairs.append(new_set)
    file.close()
    return pairs


count = import_data(1)
print(count[0][0])
pairs = import_data(count[0][0])
print(pairs)



f_data = list(map(int, input('Enter data: ').split()))
i = 0
c_list = []
for i in range(count):
    c_item = (f_data[i]-32)/1.8
    c_list.append(int(round(c_item)))

for i in c_list:
    print(i)