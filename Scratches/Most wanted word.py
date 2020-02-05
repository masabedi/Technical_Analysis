import re
password = input("Enter Your Word:")
find_lower = re.compile('[a-zA-Z]')
words = find_lower.findall(password)
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
count_list = []
for i in range(len(words)):
    words[i] = str(words[i]).lower()

print(words)
for i in alphabet:
    count = words.count(i)
    count_list.append(count)
print(count_list)
print(alphabet[count_list.index(max(count_list))])

