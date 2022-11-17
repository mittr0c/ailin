import json,requests,os,random

'''一些基本定义'''

def 加金币(qq_id,num):
    if not os.path.exists(f'data/艾琳/用户/{qq_id}.json'):
        with open(f'data/艾琳/用户/{qq_id}.json', 'w+', encoding='utf-8')as f:
            dic = {"coin": 0, "checkdate": '5' , 'honor':0}
            json.dump(dic, f)  # 写入数据
    with open(f'data/艾琳/用户/{qq_id}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        coin = dic['coin']
        coin += num
        dic['coin'] = int(coin)  # 记录金币变更
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 减金币(qq_id,num):
    if not os.path.exists(f'data/艾琳/用户/{qq_id}.json'):
        with open(f'data/艾琳/用户/{qq_id}.json', 'w+', encoding='utf-8')as f:
            dic = {"coin": 0, "checkdate": '5', 'honor':0}
            json.dump(dic, f)  # 写入数据
    with open(f'data/艾琳/用户/{qq_id}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        coin = dic['coin']
        coin -= num
        dic['coin'] = int(coin)  # 记录金币变更
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 查金币(qq_id):
    if not os.path.exists(f'data/艾琳/用户/{qq_id}.json'):
        with open(f'data/艾琳/用户/{qq_id}.json', 'w+', encoding='utf-8')as f:
            dic = {"coin": 0, "checkdate": '5', "honor": 0}
            json.dump(dic, f)  # 写入数据
    with open(f'data/艾琳/用户/{qq_id}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        return(dic['coin'])

def 查称号(qq_id):
    if not os.path.exists(f'data/艾琳/用户/{qq_id}.json'):
        with open(f'data/艾琳/用户/{qq_id}.json', 'w+', encoding='utf-8')as f:
            dic = {"coin": 0, "checkdate": '5', "honor": 0}
            json.dump(dic, f)  # 写入数据
    with open(f'data/艾琳/用户/{qq_id}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        hn = dic['honor']
        hdic = {0:'默默无闻',1:'国服百强',2:'国服五十强',3:'国服十强',4:'国服殿军',5:'国服季军',6:'国服亚军',7:'国服冠军'}
        result = hdic[hn]
        return(result)

def 改称号(qq_id,num):
    if not os.path.exists(f'data/艾琳/用户/{qq_id}.json'):
        with open(f'data/艾琳/用户/{qq_id}.json', 'w+', encoding='utf-8')as f:
            dic = {"coin": 0, "checkdate": '5', "honor": 0}
            json.dump(dic, f)  # 写入数据
    with open(f'data/艾琳/用户/{qq_id}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic['honor'] = num
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def rank123():
    list = []
    file = os.listdir('data/艾琳/用户')
    for qqi in file:
        with open(f'data/艾琳/用户/{qqi}', 'r', encoding='utf-8') as f:
            dic = json.load(f)
        coin = dic['coin']
        ele = {'qq':qqi,'coin':coin}
        list.append(ele)
    result = sorted(list, key=lambda x: x['coin'], reverse=True)
    result1 = str('rank')
    for res in range (0,10):
        dict = result[res]
        qqn = str(dict['qq']).split('.json')[0]
        result1 += '\r' + qqn + ' $' + str(dict['coin'])
    return result1

def rank101(qs,zz):
    list = []
    file = os.listdir('data/艾琳/用户')
    for qqi in file:
        with open(f'data/艾琳/用户/{qqi}', 'r', encoding='utf-8') as f:
            dic = json.load(f)
        coin = dic['coin']
        ele = {'qq':qqi,'coin':coin}
        list.append(ele)
    result = sorted(list, key=lambda x: x['coin'], reverse=True)
    result1 = str('rank')
    for res in range (qs,zz):
        dict = result[res]
        qqn = str(dict['qq']).split('.json')[0]
        result1 += '\r'+ qqn + ' $' + str(dict['coin'])
    return result1

def 发称号():
    list = []
    file = os.listdir('data/艾琳/用户')
    for qqi in file:
        with open(f'data/艾琳/用户/{qqi}', 'r', encoding='utf-8') as f:
            dic = json.load(f)
        coin = dic['coin']
        ele = {'qq':qqi,'coin':coin}
        list.append(ele)
    list = sorted(list, key=lambda x: x['coin'], reverse=True)
    top = list[0]
    qqid = str(top['qq']).split('.json')[0]  # 返回.json之前的内容
    改称号(qqid,7)   #国服冠军
    top = list[1]
    qqid = str(top['qq']).split('.json')[0]  # 返回.json之前的内容
    hdic = {'默默无闻':0,'国服百强':1,'国服五十强':2,'国服十强':3,'国服殿军':4 ,'国服季军':5,'国服亚军':6,'国服冠军':7}
    if hdic[查称号(qqid)] < 6:
        改称号(qqid,6)   #国服亚军
    top = list[2]
    qqid = str(top['qq']).split('.json')[0]  # 返回.json之前的内容
    if hdic[查称号(qqid)] < 5:
        改称号(qqid,5)   #国服季军
    top = list[3]
    qqid = str(top['qq']).split('.json')[0]  # 返回.json之前的内容
    if hdic[查称号(qqid)] < 4:
        改称号(qqid,4)   #国服殿军
    for num in range (4,9):
        ten = list[num]
        qqid = str(ten['qq']).split('.json')[0]  #返回.json之前的内容
        if hdic[查称号(qqid)] < 3:
            改称号(qqid, 3)  #国服前十
    for num in range (10,49):
        fifty = list[num]
        qqid = str(fifty['qq']).split('.json')[0]  #返回.json之前的内容
        if hdic[查称号(qqid)] < 2:
            改称号(qqid, 2)  #国服前五十
    for num in range (49,99):
        hund = list[num]
        qqid = str(hund['qq']).split('.json')[0]  #返回.json之前的内容
        if hdic[查称号(qqid)] < 1:
            改称号(qqid, 1)  #国服前百

def 查上榜金币():
    list = []
    file = os.listdir('data/艾琳/用户')
    for qqi in file:
        with open(f'data/艾琳/用户/{qqi}', 'r', encoding='utf-8') as f:
            dic = json.load(f)
        coin = dic['coin']
        ele = {'qq':qqi,'coin':coin}
        list.append(ele)
    list = sorted(list, key=lambda x: x['coin'], reverse=True)
    top = list[0]
    top_coin = (top['coin'])
    ten = list[9]
    ten_coin = (ten['coin'])
    fif = list[49]
    fif_coin = (fif['coin'])
    hund = list[99]
    hund_coin = (hund['coin'])
    result = f'国服最强：{top_coin}金币\r国服十强：{ten_coin}金币\r国服五十强：{fif_coin}金币\r国服百强：{hund_coin}金币'
    return (result)

def 随机群():
    file = os.listdir('data/艾琳/群')
    group = random.choice(file)
    group = str(group).split('.json')[0]
    return group

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
