import os,json

file = os.listdir('群')

for bbb in file:
    with open(f'群/{bbb}/信息.json', 'r', encoding='utf-8') as f:
        dic = json.load(f)
    with open(f'群/{bbb}.json', 'w+', encoding='utf-8') as f:
        json.dump(dic, f)