import json,requests,os,random,time

'''农场模块'''

def 查珠宝(qqid):
    查金币(qqid)
    with open(f'data/farm/物品/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    物品 = dic['as']
    珠宝集 = []
    for 单个物品 in list(物品.keys()):
        if 单个物品 in 查图鉴('jews'):
            珠宝集.append(单个物品)
    return 珠宝集

def 查衣服(qqid):
    查金币(qqid)
    with open(f'data/farm/物品/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    物品 = dic['as']
    衣服集 = []
    for 单个物品 in list(物品.keys()):
        if 单个物品 in 查图鉴('clos'):
            衣服集.append(单个物品)
    return 衣服集

def 查价值(msg):
    if msg == '土地':
        价值 = 10
    elif msg in 查图鉴('builds'):
        价值 = 150
    elif msg in 查图鉴('raws'):
        价值 = int(查价值(查原料(msg)) / 100)
    elif msg in 查图鉴('mines'):
        价值 = 100
    elif msg in 查图鉴('plants'):
        价格 = 查价格(msg)
        时间 = 查时间(msg)
        价值 = int(价格 + 时间 * 100 / 1440)  #一天1440分钟
    elif msg in 查图鉴('animals'):
        价格 = 查价格(msg)
        时间 = 查时间(msg)
        原料价格 = 查价值(查原料(msg)[0]) * 查原料(msg)[1]
        价值 = int(价格 + 原料价格 + 时间 * 100 / 1440)  #一天1440分钟
    elif msg == '羊毛衫':
        价值 = int(8 * ((查价值('羊毛') + 查价值('木蓝')) + 30000 / 1440))  #一天1440分钟
    elif msg in 查图鉴('as'):
        原料价格 = 0
        原料列表 = 查原料(msg)
        for 原料 in 原料列表:
            if 原料 not in 查图鉴('builds'):
                原料价格 += 查价值(原料)
        价值 = int(原料价格 + 30000 / 1440)  #一天1440分钟

    return 价值

def 物品查询(msg):
    if msg == '土地':
        return(f'基本物品：土地\r'
                f'作用：提供土地空间，种植植物、饲养动物')
    elif msg in 查图鉴('plants'):
        return(f'植物：{msg}\r'
               f'种植成本：{查价格(msg)}金币\r'
               f'成熟时间：{查时间(msg)}分钟\r'
               f'估价：{查价值(msg)}金币出售')
    elif msg in 查图鉴('animals'):
        附加品 = 查附加品(msg)
        if 附加品 != ['no', 0]:
            附加信息 = f'生产：{附加品[0]}{附加品[1]}/h\r'
        else:
            附加信息 = str()
        return(f'动物：{msg}\r'
               f'幼崽价格：{查价格(msg)}金币\r'
               f'成长时间：{查时间(msg)}分钟\r'
               f'需要食物：{查原料(msg)[0]}{查原料(msg)[1]}\r'
               f'{附加信息}'
               f'估价：{查价值(msg)}金币出售')
    elif msg in 查图鉴('raws'):
        return(f'原料：{msg}\r'
                f'获得方式：养{查原料(msg)}获得\r'
               f'估价：{查价值(msg)}金币出售')
    elif msg in 查图鉴('mines'):
        return(f'矿石：{msg}\r'
                f'获得方式：采矿有概率获得\r'
               f'估价：{查价值(msg)}金币出售')
    elif msg in 查图鉴('as'):
        原料集 = str()
        原料列表 = 查原料(msg)
        for 原料 in 原料列表:
            原料集 += 原料 + ','
        return(f'物品：{msg}\r'
               f'制作成本：0金币\r'
               f'需要：{原料集}\r'
               f'估价：{查价值(msg)}金币出售')
    elif msg in 查图鉴('builds'):
        return(f'建筑：{msg}\r'
                f'功能：{查功能(msg)}\r'
               f'估价：{查价值(msg)}金币出售')

def 全部商品():
    全部商品 = []
    file = os.listdir('data/farm/商人')
    for 商人 in file:
        with open(f'data/farm/商人/{商人}', 'r', encoding='utf-8') as f:
            商品信息 = json.load(f)
        商品列表 = 商品信息.keys()
        全部商品 += 商品列表
    return list(set(全部商品))

def 查货架(qqid): #return {'商品':[最低价,库存]...}
    查金币(qqid)
    with open(f'data/farm/商人/{qqid}.json', 'r', encoding='utf-8') as f:
        货架 = json.load(f)
    return 货架

def 查商品(name):   #return [最低价,库存,出售人]
    最低价 = 9999
    库存 = 0
    出售人 = '无商品'
    file = os.listdir('data/farm/商人')
    for 商人 in file:
        qqid = str((str(商人)).split('.json')[0])
        with open(f'data/farm/商人/{商人}', 'r', encoding='utf-8') as f:
            商品信息 = json.load(f)
        商品列表 = 商品信息.keys()
        if name in 商品列表:
            具体商品 = 商品信息[name]
            商品价格 = 具体商品[0]
            if 商品价格 < 最低价:
                最低价 = 商品价格
                库存 = 具体商品[1]
                出售人 = qqid
    return [最低价,库存,出售人]

def 商品上新(good,price,num,qqid):  #品名，价格，数量，出售人
    查货架(qqid)
    with open(f'data/farm/商人/{qqid}.json', 'r+', encoding='utf-8')as f:
        商品信息 = json.load(f)
        if good not in 商品信息.keys():
            商品信息[good] = [0,0]
        具体商品 = 商品信息[good]
        具体商品[0] = price
        具体商品[1] += num
        商品信息[good] = 具体商品
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(商品信息, f)  # 写入数据
    加物品(qqid,good, - num)

def 商品退回(good,num,qqid):  #品名，数量，出售人
    with open(f'data/farm/商人/{qqid}.json', 'r+', encoding='utf-8')as f:
        商品信息 = json.load(f)
        具体商品 = 商品信息[good]
        具体商品[1] -= num
        if 具体商品[1] <= 0:
            del 商品信息[good]
        else:
            商品信息[good] = 具体商品
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(商品信息, f)  # 写入数据
    加物品(qqid,good,num)

def 商品售出(good, num, qqid):  # 品名，数量，出售人
    with open(f'data/farm/商人/{qqid}.json', 'r+', encoding='utf-8')as f:
        商品信息 = json.load(f)
        具体商品 = 商品信息[good]
        具体商品[1] -= num
        if 具体商品[1] <= 0:
            del 商品信息[good]
        else:
            商品信息[good] = 具体商品
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(商品信息, f)  # 写入数据

def 查价格(name):
    with open('resource/farm/价格.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return dic[name]

def 查时间(name):
    with open('resource/farm/时间.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return dic[name]

def 查原料(name):
    with open('resource/farm/原料.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return dic[name]

def 查功能(name):
    with open('resource/farm/功能.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return dic[name]

def 查土地(qqid):  # 返回土地具体情况dic
    查金币(qqid)
    with open(f'data/farm/土地/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return dic['land']

def 准备购买(qqid,name):
    with open(f'data/farm/物品/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic['pre'] = name
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 查订单(qqid):
    查金币(qqid)
    with open(f'data/farm/物品/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return dic['pre']

def 生产(qqid, name, num):  # 用户，物品名，数量  （也可以是养动物、制作食品）
    if name == '羊毛衫':
        加物品(qqid,'羊毛', - 8 * num)
        加物品(qqid,'木蓝', - 8 * num)
    elif name in 查图鉴('animals'):
        原料 = 查原料(name)
        加物品(qqid,原料[0], - 原料[1] * num)
    elif name in 查图鉴('as'):
        原料集 = 查原料(name)
        for 原料 in 原料集:
            加物品(qqid,原料, - num)
        加物品(qqid,原料集[0],num) #建筑不需要减
    with open(f'data/farm/土地/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        land = dic['land']
        if name not in land.keys():
            land[name] = 0
        land[name] += num
        dic['land'] = land
        inf = dic['inf']
        now = time.time()
        inf[now] = [name,num]
        dic['inf'] = inf

        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 丰收(qqqq):   #如果qqqq=='3142331296'就是强制
    土地用户 = os.listdir('data/farm/土地')
    # 土地用户 = os.listdir('data/farm/物品')
    for qq in 土地用户:
    #     with open(f'data/farm/物品/{qq}', 'r', encoding='utf-8') as f:
    #         dic = json.load(f)
    #     建筑集 = dic['builds']
    #     建筑列表 = list(建筑集.keys())
    #     for 单个建筑 in 建筑列表:
    #         数量 = 建筑集[单个建筑]
    #         加金币(qqid,50 * 数量)
    #         加物品(qqid,单个建筑,- 数量)
    #     print(f'已处理{qqid}')
        qqid = str((str(qq)).split('.json')[0])
        with open(f'data/farm/土地/{qq}', 'r+', encoding='utf-8') as f:
            dic = json.load(f)
            inf = dic['inf']
            land = dic['land']
            pro = dic['pro']
            now = time.time()
            infkey = list(inf.keys())

            for time1 in infkey:
                作物名 = (inf[time1])[0]
                time2 = float(time1)
                past = (now - time2) / 60
                if 作物名 in 查图鉴('as'):
                    需要时间 = int(600 / (1 + 查数量(qqid,查原料(作物名)[0])))
                else:
                    需要时间 = 查时间(作物名)
                if past > 需要时间 or qqqq == '3142331296':
                    作物数 = (inf[time1])[1]
                    加物品(qqid,作物名,作物数)
                    del inf[time1]

                    land[作物名] -= 作物数
                    if land[作物名] <= 0:
                        del land[作物名]

            if qqid == qqqq or qqqq == '3142331296':   #只给查询人pro
                past2 = (now - pro) / 60
                if past2 > 60 or qqqq == '3142331296':
                    dic['pro'] = now
                    动物集 = 查动物(qqqq)
                    for 动物 in list(动物集.keys()):
                        附加品 = 查附加品(动物)
                        if 附加品 != ['no',0]:
                            数量 = 附加品[1] * 动物集[动物]
                            加物品(qqqq,附加品[0],数量)

            dic['land'] = land
            dic['inf'] = inf
            f.seek(0)  # 指向文本开头
            f.truncate()  # 清空文本
            json.dump(dic, f)

def 查附加品(name):
    with open('resource/farm/附加品.json', 'r+', encoding='utf-8') as f:
        附加品 = json.load(f)
    if name in 附加品.keys():
        return 附加品[name]
    else:
        return ['no',0]

def 查背包(qqid):    #返回全信息
    查金币(qqid)
    with open(f'data/farm/物品/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return dic

def 查物品(qqid):    #返回物品dic
    查金币(qqid)
    with open(f'data/farm/物品/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return dic['as']

def 查建筑(qqid):  # 返回建筑dic
    查金币(qqid)
    with open(f'data/farm/物品/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return dic['builds']

def 查植物(qqid):  # 返回植物dic
    查金币(qqid)
    with open(f'data/farm/物品/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return dic['plants']

def 查动物(qqid):  # 返回动物dic
    查金币(qqid)
    with open(f'data/farm/物品/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return dic['animals']

def 查土地数量(qqid):  # 返回土地数值
    查金币(qqid)
    with open(f'data/farm/物品/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        if dic['land'] > 500:
            dic['land'] = int(0.9999 * (dic['land'] - 500) + 500)
            f.seek(0)  # 指向文本开头
            f.truncate()  # 清空文本
            json.dump(dic, f)  # 写入数据
    return dic['land']

def 查空闲土地(qqid):  # 返回土地数值
    查金币(qqid)
    with open(f'data/farm/土地/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    土地信息 = dic['land']
    作物列表 = list(土地信息.keys())
    建筑信息 = 查建筑(qqid)
    建筑列表 = list(建筑信息.keys())
    占用土地 = 0
    for 作物 in 作物列表:
        if 作物 not in 查图鉴('as'):
            占用土地 += 土地信息[作物]
    for 建筑 in 建筑列表:
        占用土地 += 建筑信息[建筑]
    空闲土地 = 查土地数量(qqid) - 占用土地
    return 空闲土地

def 有物品(qqid,name):
    if 查数量(qqid,name) > 0:
        return True
    else:
        return False

def 查数量(qqid,name):
    mydic = {**查物品(qqid), **查建筑(qqid) , **查植物(qqid) , **查动物(qqid)}
    mydic['土地'] = 查空闲土地(qqid)
    if name in mydic.keys():
        return mydic[name]
    else:
        return 0

def 有空闲土地(qqid):
    if 查空闲土地(qqid) >0:
        return True
    else:
        return False

def 有空闲建筑(qqid,name):
    if 查空闲建筑(qqid,name) >0:
        return True
    else:
        return False

def 加物品(qqid,arts,num):   #用户，物品名，数量
    我的物品 = 查背包(qqid)
    if arts == '土地':
        加土地(qqid,num)
    else:
        图鉴 = 查看图鉴()
        for 物品类型 in 图鉴.keys():
            if arts in 图鉴[物品类型]:
                一类物品 = 我的物品[物品类型]
                if arts not in 一类物品.keys():
                    一类物品[arts] = 0
                一类物品[arts] += int(num)
                with open(f'data/farm/物品/{qqid}.json', 'r+', encoding='utf-8')as f:
                    dic = json.load(f)
                    dic[物品类型] = 一类物品
                    f.seek(0)  # 指向文本开头
                    f.truncate()  # 清空文本
                    json.dump(dic, f)  # 写入数据
                return 物品类型

def 加土地(qqid, num):  # 用户，数量
    land = 查土地数量(qqid) + int(num)
    with open(f'data/farm/物品/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic['land'] = land
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 设置物品(qqid,arts,num):   #用户，物品名，数量
    我的物品 = 查背包(qqid)
    图鉴 = 查看图鉴()
    for 物品类型 in 图鉴.keys():
        if arts in 图鉴[物品类型]:
            一类物品 = 我的物品[物品类型]
            一类物品[arts] = num
            with open(f'data/farm/物品/{qqid}.json', 'r+', encoding='utf-8')as f:
                dic = json.load(f)
                dic[物品类型] = 一类物品
                f.seek(0)  # 指向文本开头
                f.truncate()  # 清空文本
                json.dump(dic, f)  # 写入数据
            return 物品类型

def 查图鉴(name):  #物品？建筑？植物？动物？
    with open(f'resource/farm/图鉴.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return dic[name]

def 查看图鉴():
    with open(f'resource/farm/图鉴.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return dic

'''一些基本定义'''

def 新群(group_id):
    if not os.path.exists(f'data/艾琳/群/{group_id}.json'):  # 注册群
        with open(f'data/艾琳/群/{group_id}.json', 'w+', encoding='utf-8')as f:
            dic = {"MiningTimes": 0, "Miner0": '5'}
            json.dump(dic, f)  # 写入数据

def 查金币(qq_id):
    if not os.path.exists(f'data/艾琳/用户/{qq_id}.json'):  #注册账户
        with open(f'data/艾琳/用户/{qq_id}.json', 'w+', encoding='utf-8')as f:
            dic = {"coin": 0, "checkdate": '5', "honor": 0, "chess": 0,"jewelry":0,"clothes":0,"pet": 0,"deposit":{}}
            json.dump(dic, f)  # 写入数据0
    if not os.path.exists(f'data/farm/物品/{qq_id}.json'):  #注册农场
        with open(f'data/farm/物品/{qq_id}.json', 'w+', encoding='utf-8')as f:
            dic = {"as":{},"builds":{},"land":0,"plants": {},"animals":{},"honors": []}
            json.dump(dic, f)  # 写入数据0
    if not os.path.exists(f'data/farm/商人/{qq_id}.json'):  #注册货架
        with open(f'data/farm/商人/{qq_id}.json', 'w+', encoding='utf-8')as f:
            货架 = {}
            json.dump(货架, f)  # 写入数据0
    if not os.path.exists(f'data/farm/土地/{qq_id}.json'):  #注册土地
        with open(f'data/farm/土地/{qq_id}.json', 'w+', encoding='utf-8')as f:
            dic = {"land":{},"inf":{},"pro":5}
            json.dump(dic, f)  # 写入数据0
    with open(f'data/艾琳/用户/{qq_id}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        if dic['coin'] > 20000:
            dic['coin'] = int(0.9999 * (dic['coin'] - 20000) + 20000)
            f.seek(0)  # 指向文本开头
            f.truncate()  # 清空文本
            json.dump(dic, f)  # 写入数据

    return int(dic['coin'])

def 服饰信息(qqid):
    服饰 = str()
    服饰集 = 查衣服(qqid)
    if 查服饰(qqid) == 0 and len(服饰集) >= 1:   #没选择服饰，有衣服，随机
        服饰 = '\r服饰：' + random.choice(服饰集)
    elif 查服饰(qqid) == 'rnd' and len(服饰集) >= 1:   #设置随机
        服饰 = '\r服饰：' + random.choice(服饰集)
    elif 查服饰(qqid) != 0:   #有服饰
        服饰 = '\r服饰：' + 查服饰(qqid)
    return 服饰

def 饰品信息(qqid):
    饰品 = str()
    饰品集 = 查珠宝(qqid)
    if 查饰品(qqid) == 0 and len(饰品集) >= 1:   #没选择饰品，有珠宝，随机
        饰品 = '\r饰品：' + random.choice(饰品集)
    elif 查饰品(qqid) == 'rnd' and len(饰品集) >= 1:   #设置随机
        饰品 = '\r饰品：' + random.choice(饰品集)
    elif 查饰品(qqid) != 0:   #有饰品
        饰品 = '\r饰品：' + 查饰品(qqid)
    return 饰品

def 宠物信息(qqid):
    宠物 = str()
    动物集 = 查动物(qqid)
    if 查宠物(qqid) == 0 and len(动物集) >= 1: #没宠物，有动物，随机宠物
        宠物 = '\r宠物：' + random.choice(list(动物集.keys()))
    elif 查宠物(qqid) == 'rnd' and len(动物集) >= 1: #随机宠物
        宠物 = '\r宠物：' + random.choice(list(动物集.keys()))
    elif 查宠物(qqid) != 0:   #有宠物
        宠物 = '\r宠物：' + 查宠物(qqid)
    return 宠物

def 查宠物(qq_id):
    with open(f'data/艾琳/用户/{qq_id}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return(dic['pet'])

def 查饰品(qq_id):
    with open(f'data/艾琳/用户/{qq_id}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return(dic['jewelry'])

def 查服饰(qq_id):
    with open(f'data/艾琳/用户/{qq_id}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return(dic['clothes'])

def 设置饰物(qq_id,key1,value1):
    with open(f'data/艾琳/用户/{qq_id}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic[key1] = value1
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 加金币(qq_id,num):
    查金币(qq_id)
    with open(f'data/艾琳/用户/{qq_id}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        coin = dic['coin']
        coin += num
        dic['coin'] = int(coin)  # 记录金币变更
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 减金币(qq_id,num):
    查金币(qq_id)
    with open(f'data/艾琳/用户/{qq_id}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        coin = dic['coin']
        coin -= num
        dic['coin'] = int(coin)  # 记录金币变更
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 改金币(qq_id,num):
    查金币(qq_id)
    with open(f'data/艾琳/用户/{qq_id}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        coin = dic['coin']
        coin = num
        dic['coin'] = int(coin)  # 记录金币变更
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据


def 查称号(qq_id):
    查金币(qq_id)
    with open(f'data/艾琳/用户/{qq_id}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
        hn = dic['honor']
        hdic = {0:'默默无闻',1:'国服两百强',2:'国服百强',3:'国服五十强',4:'国服十强',5:'国服殿军',6:'国服季军',7:'国服亚军',8:'国服冠军'}
        result = hdic[hn]
    return(result)

def 改称号(qq_id,num):
    查金币(qq_id)
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
    rlist = []
    file = os.listdir('data/艾琳/用户')
    for qqi in file:
        with open(f'data/艾琳/用户/{qqi}', 'r', encoding='utf-8') as f:
            dic = json.load(f)
        coin = dic['coin']
        ele = {'qq':qqi,'coin':coin}
        rlist.append(ele)
    result = sorted(rlist, key=lambda x: x['coin'], reverse=True)
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
    改称号(qqid,8)   #国服冠军
    top = list[1]
    qqid = str(top['qq']).split('.json')[0]  # 返回.json之前的内容
    hdic = {'默默无闻':0,'国服两百强':1,'国服百强':2,'国服五十强':3,'国服十强':4,'国服殿军':5,'国服季军':6,'国服亚军':7,'国服冠军':8}
    if hdic[查称号(qqid)] < 7:
        改称号(qqid,7)   #国服亚军
    top = list[2]
    qqid = str(top['qq']).split('.json')[0]  # 返回.json之前的内容
    if hdic[查称号(qqid)] < 6:
        改称号(qqid,6)   #国服季军
    top = list[3]
    qqid = str(top['qq']).split('.json')[0]  # 返回.json之前的内容
    if hdic[查称号(qqid)] < 5:
        改称号(qqid,5)   #国服殿军
    for num in range (4,9):
        ten = list[num]
        qqid = str(ten['qq']).split('.json')[0]  #返回.json之前的内容
        if hdic[查称号(qqid)] < 4:
            改称号(qqid, 4)  #国服前十
    for num in range (10,49):
        fifty = list[num]
        qqid = str(fifty['qq']).split('.json')[0]  #返回.json之前的内容
        if hdic[查称号(qqid)] < 3:
            改称号(qqid, 3)  #国服前五十
    for num in range (49,99):
        hund = list[num]
        qqid = str(hund['qq']).split('.json')[0]  #返回.json之前的内容
        if hdic[查称号(qqid)] < 2:
            改称号(qqid, 2)  #国服前百
    for num in range (100,199):
        hund = list[num]
        qqid = str(hund['qq']).split('.json')[0]  #返回.json之前的内容
        if hdic[查称号(qqid)] < 1:
            改称号(qqid, 1)  #国服前2百

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
    hund2 = list[199]
    hund2_coin = (hund2['coin'])
    result = f'国服最强：{top_coin}金币\r国服十强：{ten_coin}金币\r国服五十强：{fif_coin}金币\r国服百强：{hund_coin}金币\r国服两百强：{hund2_coin}金币'
    return (result)

def 随机群():
    file = os.listdir('data/艾琳/群')
    group = random.choice(file)
    group = str(group).split('.json')[0]
    return group

def 取英雄号(name):
    with open('resource/wzry/英雄词典.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
        return(dic[name])

def 生成英雄列表():
    list = requests.get('http://pvp.qq.com/web201605/js/herolist.json')
    list = json.loads(list.content)
    英雄列表 = []
    for dic in list:
        英雄代码 = dic['ename']
        英雄列表.append(英雄代码)
    with open('resource/wzry/英雄列表.json', 'w+', encoding='utf-8')as f:
        json.dump(英雄列表, f)

def 生成英雄词典():
    list = requests.get('http://pvp.qq.com/web201605/js/herolist.json')
    list = json.loads(list.content)
    英雄词典 = {}
    for dic in list:
        英雄代码 = dic['ename']
        英雄名 = dic['cname']
        英雄词典[英雄名] = 英雄代码
    with open('resource/wzry/英雄词典.json', 'w+', encoding='utf-8')as f:
        json.dump(英雄词典, f)

'''chess模块'''

def chess信息(qq_id):
    if 查chess段位(qq_id) != '棋手🏅':
        return '\r' + 查chess段位(qq_id)
    else:
        return str()

def 查chess排位分(qqid):
    查金币(qqid)
    with open(f'data/艾琳/用户/{qqid}.json', 'r', encoding='utf-8')as f:
        chessdic = json.load(f)
    return chessdic['chess']

def 查chess段位(qqid):
    score = 查chess排位分(qqid)
    ranklist = ['棋手🏅','青铜棋手🏅','白银棋手🏅','黄金棋手🏅','铂金棋手🏅','钻石棋手🏅','星耀棋手🏅','大师棋手🏅','宗师棋手🏅']
    score1 = int(pow(score,0.5))
    return ranklist[score1]

def 加chess排位分(qqid,num):
    查金币(qqid)
    with open(f'data/艾琳/用户/{qqid}.json', 'r+', encoding='utf-8')as f:
        chessdic = json.load(f)
        score = chessdic['chess']
        score += num
        chessdic['chess'] = score
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(chessdic, f)  # 写入数据


'''银行模块'''

def 查存款(bank,qqid):
    with open(f'data/bank/银行/{bank}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        账户 = dic['account']   #所有人账户dic
        if qqid not in list(账户.keys()):
            账户[qqid] = [0,0]
            f.seek(0)  # 指向文本开头
            f.truncate()  # 清空文本
            json.dump(dic, f)  # 写入数据
    with open(f'data/bank/银行/{bank}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    账户 = dic['account']   #所有人账户dic
    return 账户[qqid][0]

def 查贷款(bank,qqid):
    with open(f'data/bank/银行/{bank}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        账户 = dic['account']   #所有人账户dic
        qqid = f'{qqid}b'
        if qqid not in list(账户.keys()):
            账户[qqid] = [0,0]
            f.seek(0)  # 指向文本开头
            f.truncate()  # 清空文本
            json.dump(dic, f)  # 写入数据
    with open(f'data/bank/银行/{bank}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    账户 = dic['account']   #所有人账户dic
    return - 账户[qqid][0]

def 存金币(qqid,num,bank):
    减金币(qqid,num)
    董事长 = 查银行数据(bank,'chairman')
    with open(f'data/bank/银行/{bank}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        账户 = dic['account']   #所有人账户dic
        if qqid == 董事长:
            dic['coin'] += num
        else:
            if qqid not in list(账户.keys()):
                账户[qqid] = [num,time.time()]
            else:
                账户[qqid][0] += num
                账户[qqid][1] = time.time()
        dic['account'] = 账户
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 取金币(qqid,num,bank):
    加金币(qqid,num)
    董事长 = 查银行数据(bank,'chairman')
    with open(f'data/bank/银行/{bank}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        if qqid == 董事长:
            dic['coin'] -= num
        else:
            账户 = dic['account']   #所有人账户dic
            账户[qqid][0] -= num
            dic['account'] = 账户
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 借金币(qqid,num,bank):
    加金币(qqid,num)
    qqidb = f'{qqid}b'
    董事长 = 查银行数据(bank,'chairman')
    with open(f'data/bank/银行/{bank}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic['coin'] -= num
        if qqid != 董事长:
            账户 = dic['account']   #所有人账户dic
            if qqidb not in list(账户.keys()):
                账户[qqidb] = [num,5]
            else:
                账户[qqidb][0] -= num
                账户[qqidb][1] = 5

        dic['account'] = 账户
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 还金币(qqid,num,bank):
    减金币(qqid,num)
    qqidb = f'{qqid}b'
    with open(f'data/bank/银行/{bank}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic['coin'] += num
        账户 = dic['account']   #所有人账户dic
        账户[qqidb][0] += num
        dic['account'] = 账户
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 准备(qqid,num,name):
    with open(f'data/艾琳/用户/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        if name == '存金币':
            dic['￥'] = 'c'
        elif name == '取金币':
            dic['￥'] = 'q'
        elif name == '借金币':
            dic['￥'] = 'j'
        elif name == '还金币':
            dic['￥'] = 'h'
        dic['pre'] = num
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 查准备(qqid):
    with open(f'data/艾琳/用户/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
    return [dic['pre'],dic['￥']]

def 银行列表():
    with open(f'data/bank/银行列表.json', 'r', encoding='utf-8')as f:
        llll = json.load(f)
    return llll

def 注册银行(qqid,bank):
    设置银行名(qqid,bank)
    if not os.path.exists(f'data/bank/银行/{bank}.json'):  #注册
        with open(f'data/bank/银行/{bank}.json', 'w+', encoding='utf-8')as f:
            dic = {}
            json.dump(dic, f)  # 写入数据
    if not os.path.exists(f'data/bank/银行列表.json'):  #初始化
        with open(f'data/bank/银行列表.json', 'w+', encoding='utf-8')as f:
            dic = []
            json.dump(dic, f)  # 写入数据
    with open(f'data/bank/银行列表.json', 'r+', encoding='utf-8')as f:
        bank_list = json.load(f)
        bank_list.append(bank)
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(bank_list, f)  # 写入数据
    设置银行数据(bank,'chairman',qqid)
    设置银行数据(bank,'coin',0)
    设置银行数据(bank,'interest',0)
    设置银行数据(bank,'loan_interest',0)
    设置银行数据(bank,'loan',0)
    设置银行数据(bank,'account',{})

def 查银行名(qqid):
    with open(f'data/艾琳/用户/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    if 'bank_name' in list(dic.keys()):
        return dic['bank_name']
    else:
        return 'no'

def 设置银行名(qqid,name):
    with open(f'data/艾琳/用户/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic['bank_name'] = name
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 查银行数据(bank,name):
    with open(f'data/bank/银行/{bank}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return(dic[name])

def 设置银行数据(bank,name,num):
    with open(f'data/bank/银行/{bank}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic[name] = num
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 开户(qqid,bank):
    账户 = 查银行数据(bank,'account')
    账户[qqid] = {}
    设置银行数据(bank,'account',账户)

def 查开户人数(bank):
    开户 = 查银行数据(bank,'account')
    开户列表 = list(开户.keys())
    return len(开户列表)

def 查银行资金(bank):
    with open(f'data/bank/银行/{bank}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        账户 = dic['account']
        缓冲资金 = dic['coin']
        资金 = 0
        for 单个账户 in list(账户.values()):
            if 单个账户[-1] != 'b':
                资金 += 单个账户[0]
        真实资金 = 资金 + 缓冲资金
        if 真实资金 < 0:
            qqid = 查银行数据(bank,'chairman')
            加金币(qqid,真实资金)   #资金是负数
            dic['coin'] -= 真实资金
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据
    return int(资金 + 缓冲资金)

def 查账户(银行):
    with open(f'data/bank/银行/{银行}.json', 'r+', encoding='utf-8') as f:
        dic = json.load(f)
        账户 = dic['account']
        用户列表 = list(账户.keys())
        存款 = 'deposits:'
        借款 = 'loans:'
        for qqid in 用户列表:
            if 账户[qqid][0] != 0:
                if qqid[-1] == 'b':
                    借款 += f'\r{qqid}:{账户[qqid][0]}'
                else:
                    存款 += f'\r{qqid}:{账户[qqid][0]}'
        return [存款,借款]

def 判定利息():
    file = os.listdir('data/bank/银行')
    for 银行 in file:
        with open(f'data/bank/银行/{银行}', 'r+', encoding='utf-8') as f:
            dic = json.load(f)
            账户 = dic['account']
            用户列表 = list(账户.keys())
            利息 = dic['interest']
            贷款利息 = dic['loan_interest']
            for qqid in 用户列表:
                time1 = 账户[qqid][1]
                now = time.time()
                past = (now - time1) / 60
                if past > 60:
                    账户[qqid][1] = now
                    数额 = 账户[qqid][0]
                    if qqid[-1] == 'b':
                        账户[qqid][0] = int((1 + 贷款利息 / 100) * 数额)
                    else:
                        if 数额 > 20000:
                            账户[qqid][0] = int(数额 + 20000 * 利息 / 100)
                            dic['coin'] -= int(20000 * 利息 / 100)
                        else:
                            账户[qqid][0] = int((1 + 利息 / 100) * 数额)
                            dic['coin'] -= int(数额 * 利息 / 100)
            dic['account'] = 账户
            f.seek(0)  # 指向文本开头
            f.truncate()  # 清空文本
            json.dump(dic, f)  # 写入数据