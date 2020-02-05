import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s -  %(levelname)s -  %(message)s')
# import sys
# list = sys.stdin.read().split()


def fibonacci(n):
    fibo = []

    for i in range(n):
        if i == 0:
            fibo.insert(0,1)
        elif i == 1:
            fibo.insert(1,1)
        else:
            fibo.insert(i, fibo[i-1]+fibo[i-2])

    for n in fibo:
        print(n)
fibonacci(5)





