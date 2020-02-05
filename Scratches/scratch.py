numbers = int(input("how many numbers :"))
number_list = []
i = 0
while i < numbers :
    i += 1
    num1 = int(input("Whats num 1?: "))
    num2 = int(input("whats num 2?: "))
    number_list.append(min(num1,num2))
    print(number_list)


numbers = list(map(int, input('Enter numbers: ').split()))
print(numbers)