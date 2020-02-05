def import_data(n):
    file = open("numbers.txt", "r")
    number_file = file.readlines()
    pairs = []
    for i in range(n):
        new_item = number_file[i]
        new_set = list(map(int, new_item.split()))
        pairs.append(new_set)
    file.close()
    return pairs


count = int(input("how many pair do you want to sum? :"))
pairs = import_data(count)
div_list = []
for i in range(count):
    divided_number = int(round(pairs[i][0]/pairs[i][1]))
    div_list.append(divided_number)

for i in div_list:
    print(i)
