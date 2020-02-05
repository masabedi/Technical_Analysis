import re
password = input("Enter Your Password:")
find_digit = re.compile(r'\d')
find_lower = re.compile('[a-z]')
find_upper = re.compile('[A-Z]')
if find_digit.search(password) != None and find_lower.search(password) != None and find_upper.search(password) != None and len(password) >= 10 :
    print(True)
else:
    print(False)
