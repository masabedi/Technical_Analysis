def import_count():
    file = open("numbers.txt", "r")
    count_read = file.readlines(0)
    count = int(count_read[0])
    file.close()
    return count
def import_data(n):
    file = open("numbers.txt", "r")
    number_file = file.readlines()
    pairs = []
    for i in range(n):
        new_item = number_file[i+1]
        new_set = list(map(int, new_item.split()))
        pairs.append(new_set)
    file.close()
    return pairs

count = import_count()
pairs = import_data(count)
result_list = []

for item in pairs:
    num = item[2]
    first_number = item[0]
    steps = item[1]

    # making arithmetic sequence
    num_list = []
    for n in range(num):
        digit = first_number+(steps*n)
        num_list.append(digit)
    print(num_list)

    # sum of first digits in each member of sequence
    digit_sum = 0
    for d in num_list:
        str_digit = str(d)
        digit_sum += int(str_digit[0])
    print(digit_sum)

    result_list.append(digit_sum)

for i in result_list:
    print(i)
