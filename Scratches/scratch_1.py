count = int(input("how many numbers do you want to sum? :"))
numbers = list(map(int, input('Enter numbers: ').split()))
sum_of_numbers = 0
while len(numbers) > count :
    print("Your numbers are exceeded %s" %count)
    numbers = list(map(int, input('Enter numbers: ').split()))

for i in numbers:
    sum_of_numbers += i

print(sum_of_numbers)

# new line o f code

count = int(input("how many pair do you want to sum? :"))
numbers = list(map(int, input('Enter pairs numbers: ').split()))
firts_pair = numbers[::2]
second_pair = [x for x in numbers if x not in firts_pair]
new_list = []

while len(numbers)/2 > count :
    print("Your numbers are exceeded %s" %count)
    numbers = list(map(int, input('Enter numbers: ').split()))
i = 0
for item in firts_pair:
    new_list.append(min(firts_pair[i],second_pair[i]))
    i += 1

print(new_list)



