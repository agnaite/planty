import json
from pprint import pprint

with open('plant_results_loop.json') as data_file:
        data = json.load(data_file)

count = 0
for plant in data:
    pprint(plant)
    print " "
    print " "
    # print "*************{}*************".format(count)
    # if 'value' in plant:
    #     for val in plant['value']:
    #         print val
    #         print " "
    #         print " "
    #         print '*' * 60
    # count += 1
# print data[0]
