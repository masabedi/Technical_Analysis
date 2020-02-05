import pandas as pd
import json

file = "/Users/masoudabedi/Desktop/Sahamyab/sectors.json"

with open(file) as j_file:
    data = json.load(j_file)


data_keys = ['id', 'name', 'data', 'children', 'markets', 'sectors', 'success']
# type of each key
#
# 0 id : string
# 1 name: string
# 2 data: dictionary
# 3 children: list
# 4 markets: list
# 5 sectors: list
# 6 success: boolean

children = data.get("children")
markets = data.get("markets")
sectors = data.get("sectors")

# -------------- children

children_keys = ['id', 'name', 'children', 'data']
# type of each key
#
# 0 id : string
# 1 name: string
# 2 children: list
# 3 data: dictionary


# -------------- children -----> children
child_child = children[0].get(children_keys[2])[2]

child_child_keys = ['id', 'name', 'children', 'data']
# type of each key
#
# 0 id : string
# 1 name: string
# 2 children: list
# 3 data: dictionary

child_child_name = child_child.get(child_child_keys[1])



# -------------- children -----> data
children_data_keys = ['$area', 'tradeValue', 'tradeVolume', 'marketValue', '$color']
child_data_area = children[0].get(children_keys[3]).get(children_data_keys[0])
child_data_tradeval = children[0].get(children_keys[3]).get(children_data_keys[1])
child_data_tradevol = children[0].get(children_keys[3]).get(children_data_keys[2])
child_data_marketval = children[0].get(children_keys[3]).get(children_data_keys[3])
child_data_color = children[0].get(children_keys[3]).get(children_data_keys[4])


def get_child_name(data):
    children = data.get("children")
    for i in range(len(children)):
        child_name = children[i].get(children_keys[1])
        print(child_name)

# def sector_companies(sector:str):

    # for i in range(len(child_child)):
if __name__ == "__main__":
    for i in range(len(children)+1):
        # child_inside = children[].get(children_keys[2])[i]
        # print(child_inside.get(child_child_keys[1]))
        print(i)
