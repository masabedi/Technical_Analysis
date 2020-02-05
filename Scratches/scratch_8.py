import json
from collections import defaultdict
from collections import Counter
from pandas import DataFrame, Series
import pandas as pd

path = '/Users/masoudabedi/PycharmProjects/Exercise/Data Analysis Files/ch02/usagov_bitly_data2012-03-16-1331923249.txt'
records = [json.loads(line) for line in open(path)]
def printing(item):
    for i in item:
        print(i)
time_zones = [rec['tz'] for rec in records if 'tz' in rec]
def get_counts(sequence):
    counts = defaultdict(int)
    for x in sequence:
        counts[x] += 1
    return counts
counts = get_counts(time_zones)

def top_counts(count_dict, n=10):
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]
count = Counter(time_zones)
print(count.most_common(10))