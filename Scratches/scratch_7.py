import re
def time_converter(time):
    timeregex = re.compile(r'(\d\d):(\d\d)')
    group_time = timeregex.search(time)
    hour = group_time.group(1)
    minutes = group_time.group(2)

    if int(hour) > 12:
        time = str(int(hour) - 12) + ':' + minutes + ' p.m.'
    elif int(hour) == 12:
        time =  hour + ':' + minutes + ' p.m.'
    elif int(hour) == 0:
        time =  '12' + ':' + minutes + ' a.m.'
    else:
        time =  hour[1] + ':' + minutes + ' a.m.'
    return time
print(time_converter('09:30'))
