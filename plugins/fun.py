import json,os,requests

'''一些基本定义'''

def 新用户(qq_id):  #判断是否为新用户，是就创建一个用户文件夹
    if not os.path.exists(f'data/艾琳/用户/{qq_id}'):
        os.makedirs(f'data/艾琳/用户/{qq_id}')
        with open(f'data/艾琳/用户/{qq_id}/信息.json', 'w+', encoding='utf-8')as f:
            dic = {'coin': int('0'), 'checkdate': int('5')}
            json.dump(dic, f)

def 新群(group_id):  # 判断是否为新群，是就创建一个群文件夹，挖矿功能用
    if not os.path.exists(f'data/艾琳/群/{group_id}'):
        os.makedirs(f'data/艾琳/群/{group_id}')
        with open(f'data/艾琳/群/{group_id}/信息.json', 'w+', encoding='utf-8')as f:
            dic = {'MiningTimes': int('0'), 'Miner0': int('0')}
            json.dump(dic, f)

def 加金币(qq_id,num):
    with open(f'data/艾琳/用户/{qq_id}/信息.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        coin = dic['coin']
        coin += num
        dic['coin'] = int(coin)  # 记录金币变更
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 减金币(qq_id,num):
    with open(f'data/艾琳/用户/{qq_id}/信息.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        coin = dic['coin']
        coin -= num
        dic['coin'] = int(coin)  # 记录金币变更
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 查金币(qq_id):
    with open(f'data/艾琳/用户/{qq_id}/信息.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        return(dic['coin'])

def 取英雄号(name):
    with open('wzry/英雄词典.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
        return(dic[name])

def 生成英雄列表():
    list = requests.get('http://pvp.qq.com/web201605/js/herolist.json')
    list = json.loads(list.content)
    英雄列表 = []
    for dic in list:
        英雄代码 = dic['ename']
        英雄列表.append(英雄代码)
    with open('wzry/英雄列表.json', 'w+', encoding='utf-8')as f:
        json.dump(英雄列表, f)

def 生成英雄词典():
    list = requests.get('http://pvp.qq.com/web201605/js/herolist.json')
    list = json.loads(list.content)
    英雄词典 = {}
    for dic in list:
        英雄代码 = dic['ename']
        英雄名 = dic['cname']
        英雄词典[英雄名] = 英雄代码
    with open('wzry/英雄词典.json', 'w+', encoding='utf-8')as f:
        json.dump(英雄词典, f)
