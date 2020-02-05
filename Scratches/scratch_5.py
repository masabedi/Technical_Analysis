file = open("text.txt", "r")
text_list = []
for i in range(15):
    reading_file = file.readlines(i+1)
    text_list.append(str(reading_file[0]))

print(text_list)
count_list = []
for i in text_list:
    count_a = i.count("a")
    count_o = i.count("o")
    count_u = i.count("u")
    count_i = i.count("i")
    count_e = i.count("e")
    count_y = i.count("y")
    count_sum = int(count_a) + int(count_o) + int(count_u) + int(count_i) + int(count_e) + int(count_y)
    count_list.append(count_sum)

for i in count_list:
    print(i)

# BMI test

for item in pairs:
    bmi = float(i[0]/(i[1]^2))
    if bmi < 18.5:
        result = "under"

    elif 18.5 <= bmi < 25.5:
        result = "normal"

    elif 25.5 <= bmi < 30.0:
        result = "over"

    elif 30.0 <= bmi :
        result = "obese"
    result_list.append(result)


for i in result_list:
    print(i)