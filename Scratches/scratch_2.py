numbers = list(map(int, input('Enter numbers: ').split()))
print(numbers)
firts_pair = numbers[::2]
second_pair = [x for x in numbers if x not in firts_pair]


count = int(input("how many pair do you want to sum? :"))
numbers = list(map(int, input('Enter pairs numbers: ').split()))
firts_pair = numbers[::2]
second_pair = [x for x in numbers if x not in firts_pair]
sum_of_numbers = []

while len(numbers)/2 > count :
    print("Your numbers are exceeded %s" %count)
    numbers = list(map(int, input('Enter numbers: ').split()))
i = 0
for item in firts_pair:
    new_list = [min(firts_pair[i],second_pair[1])]

    i += 1

print(sum_of_numbers)


