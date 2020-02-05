import pandas as pd

file = "/Users/masoudabedi/PycharmProjects/Technical Analysis/result.csv"
data = pd.read_csv(file)

if __name__ =="__main__":
    print(data.index)