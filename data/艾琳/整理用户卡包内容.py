import os,json

file = os.listdir('卡包')

for bbb in file:
    with open(f'卡包/{bbb}', 'w+', encoding='utf-8') as f:
        卡包 = ['鲁班七号','王昭君','孙策']
        json.dump(卡包, f)