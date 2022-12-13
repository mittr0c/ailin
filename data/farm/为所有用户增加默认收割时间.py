import os,json

file = os.listdir('土地')

for aaa in file:
    with open(f'土地/{aaa}', 'r+', encoding='utf-8') as f:
        dic = json.load(f)
        dic['pro'] = 4
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)

