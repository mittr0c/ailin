import os,json

file = os.listdir('用户')

for aaa in file:
    with open(f'用户/{aaa}', 'r+', encoding='utf-8') as f:
        dic = json.load(f)
        dic['pet'] = 0
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)

