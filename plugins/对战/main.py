
from nonebot.adapters.onebot.v11 import MessageSegment  # 发图片用的
from nonebot.adapters.onebot.v11 import Bot  #发消息用的
import os,json,random,time

def 台词(qqid):
    hero = 查玩家英雄(qqid)
    with open(f'resource/对战/lines/{hero}.json', 'r', encoding='utf-8')as f:
        lines = json.load(f)  #英雄台词集
    lines = random.choice(lines)
    return lines

def 英雄台词(hero):
    with open(f'resource/对战/lines/{hero}.json', 'r', encoding='utf-8')as f:
        lines = json.load(f)  #英雄台词集
    lines = random.choice(lines)
    return lines

def 结算(desk):  #返回：[结算语,名次],[结算语,名次],……
    playlist = 取玩家列表(desk)
    结算list = []
    for player in playlist:
        if 查玩家血量(player) <= 0 and 取游戏房间(player) != 0:
            改玩家状态(player,'die')
            vilist = 取存活玩家列表(desk)
            no = len(vilist) + 1
            mess = 发放奖励(player,no)
            结算list.append(mess)
    return 结算list

def 下一位(desk):  #设置轮次，返回一个判定集、一个回合开始语

    判定list = []
    结算list = []
    应该判断 = True

    while 应该判断 == True or 跳过回合 == True:

        跳过回合 = False

        '''先结算所有阵亡玩家（将结算语写入判定list）'''

        结算list = 结算list + 结算(desk) #返回：[结算语,名次],[结算语,名次],……
        if len(结算list) != 0:  #如果有人结算
            if len(取存活玩家列表(desk)) <= 1:
                return 结算list
            else:
                for 结算语 in 结算list:
                    判定list.append(结算语)

        '''找下一位存活玩家（赋值player和turn）'''

        turn = 取当前行动轮(desk)
        turn += 1
        if turn > 8:
            turn = 1
        player = 查看指定轮玩家(desk,turn)

        while 查玩家血量(player) <= 0:
            turn += 1
            if turn > 8:
                turn = 1
            player = 查看指定轮玩家(desk,turn)

        '''设置新轮次'''

        改玩家状态(player,'act')
        改技能类别(player, 0)
        设置当前行动轮(desk, turn)
        开始行动计时(player)

        '''新玩家回合开始前判定（将判定语写入判定list）'''

        '''伤害效果判定'''

        qqid = 查看指定轮玩家(desk,turn)
        buff = 查玩家buff(qqid)
        if '🛰️' in buff:
            判定 = random.randint(1,100)
            if 判定 <= 30:
                移除buff(qqid,'🛰️')
                name = '河豚飞艇'
                判定list.append(f'{qqid}受到河豚飞艇的{其他伤害(str(name),str(qqid))}点物理伤害。')
            else:
                移除buff(qqid, '🛰️')
                tar = turn + 1
                if tar > 8:
                    tar = 1
                tarqq = 查看指定轮玩家(desk,tar)
                while 查玩家状态(tarqq) == 'die':
                    tar += 1
                    if tar > 8:
                        tar = 1
                    tarqq = 查看指定轮玩家(desk,tar)
                加buff(tarqq, '🛰️')
                判定list.append(f'{qqid}未受到河豚飞艇伤害，河豚飞艇移至下家。')

        '''控制效果判定'''

        if '🥏' in buff:
            移除buff(qqid, '🥏')
            跳过回合 = True
            判定list.append(f'{qqid}被击飞，跳过本回合。')
        if '🧊' in buff:
            bing = random.randint(0,100)
            if bing > 50:
                移除buff(qqid, '🧊')
            else:
                跳过回合 = True
                判定list.append(f'{qqid}被冰冻，跳过本回合。')

        '''判定结束后，只查看当前玩家是否存活（不看其他人）'''

        if 查玩家血量(player) > 0:
            应该判断 = False   #如果他存活，就结束循环，否则跳回开头进行结算

    '''如果判定list有内容，则生成判定语'''

    if len(判定list) != 0:  #有内容
        判定语 = str()
        for 判定句 in 判定list:
            判定语 = 判定语 + 判定句
    else:
        判定语 = '无'

    '''回合开始时执行装备回血'''

    加血 = 查玩家属性(player)[8] # return [物攻,法强,护甲,法抗,破甲,法穿,物理吸血,法术吸血,加血]
    加玩家血量(player,加血)

    '''回合正式开始'''

    hero = 查玩家英雄(player)
    开始语 = f'当前行动玩家：{turn}号，{player}' + 取头像(hero) + '请ta发送【主动技】或【限定技】或【跳过】'
    图 = 取卡图(hero)

    return [判定语,开始语,图]

def 改技能类别(qqid,cate):
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        playdic = json.load(f)  #英雄属性
        playdic['cate'] = cate
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(playdic, f)  # 写入数据
    return cate

def 查技能类别(qqid):
    with open(f'data/game/players/{qqid}.json', 'r', encoding='utf-8')as f:
        playdic = json.load(f)  #英雄属性
    return playdic['cate']

def 其他伤害(name,tarqq):

    tar护甲 = 查玩家属性(tarqq)[3]  # return [物攻,法强,护甲,法抗,破甲,法穿,物理吸血,法术吸血,加血]
    tar法抗 = 查玩家属性(tarqq)[3]

    if name == '河豚飞艇':
        hurt = 1000 - tar护甲
        if 查玩家英雄(tarqq) == '鲁班七号':
            hurt = hurt * 0.5

    if hurt < 30:
        hurt = 30
    加玩家血量(tarqq, - hurt)
    return hurt

def 查主动技距离(hero):
    with open(f'resource/对战/heroes/{hero}.json', 'r', encoding='utf-8')as f:
        herodic = json.load(f)  #英雄属性
    return (herodic['主动距离'])

def 查限定技距离(hero):
    with open(f'resource/对战/heroes/{hero}.json', 'r', encoding='utf-8')as f:
        herodic = json.load(f)  #英雄属性
    return (herodic['限定距离'])

def 查主动伤害(hero):
    with open(f'resource/对战/heroes/{hero}.json', 'r', encoding='utf-8')as f:
        herodic = json.load(f)
    return herodic['主动伤害']

def 查主动类型(hero):
    with open(f'resource/对战/heroes/{hero}.json', 'r', encoding='utf-8')as f:
        herodic = json.load(f)
    return herodic['主动类型']

def 查主动加成类型(hero):
    with open(f'resource/对战/heroes/{hero}.json', 'r', encoding='utf-8')as f:
        herodic = json.load(f)
    return herodic['主动加成类型']

def 查主动加成比例(hero):
    with open(f'resource/对战/heroes/{hero}.json', 'r', encoding='utf-8')as f:
        herodic = json.load(f)
    return herodic['主动加成比例']

def 查限定类型(hero):
    with open(f'resource/对战/heroes/{hero}.json', 'r', encoding='utf-8')as f:
        herodic = json.load(f)
    return herodic['限定类型']

def 查限定加成类型(hero):
    with open(f'resource/对战/heroes/{hero}.json', 'r', encoding='utf-8')as f:
        herodic = json.load(f)
    return herodic['限定加成类型']

def 查限定加成比例(hero):
    with open(f'resource/对战/heroes/{hero}.json', 'r', encoding='utf-8')as f:
        herodic = json.load(f)
    return herodic['限定加成比例']

def 查限定伤害(hero):
    with open(f'resource/对战/heroes/{hero}.json', 'r', encoding='utf-8')as f:
        herodic = json.load(f)
    return herodic['限定伤害']

def 普通伤害(qqid,tarqq,cate):   #返回伤害值
    hero = 查玩家英雄(qqid)
    tarhero = 查玩家英雄(tarqq)

    物攻 = 查玩家属性(qqid)[0]  # return [物攻,法强,护甲,法抗,破甲,法穿,物理吸血,法术吸血,加血]
    法强 = 查玩家属性(qqid)[1]
    破甲 = 查玩家属性(qqid)[5]
    法穿 = 查玩家属性(qqid)[6]
    物理吸血 = 查玩家属性(qqid)[7]
    法术吸血 = 查玩家属性(qqid)[8]

    tar护甲 = 查玩家属性(tarqq)[3]  # return [物攻,法强,护甲,法抗,破甲,法穿,物理吸血,法术吸血,加血]
    tar法抗 = 查玩家属性(tarqq)[3]

    if hero == '孙策':
        加印记(qqid, 1)

    if tarhero == '孙策':
        if 查印记(tarqq) < 9:
            加印记(tarqq, 1)
        sig = 查印记(tarqq)
        tar护甲 += sig * 30
        tar法抗 += sig * 30

    if cate == '主动技':
        主动伤害 = 查主动伤害(hero)
        伤害类型 = 查主动类型(hero)
        加成类型 = 查主动加成类型(hero)
        加成比例 = 查主动加成比例(hero)
        if 伤害类型 == 'AD' and 加成类型 == 'AD':
            hurt = 主动伤害 + 加成比例 * 物攻 - tar护甲 * ( 1 - 破甲 )
        elif 伤害类型 == 'AP' and 加成类型 == 'AD':
            hurt = 主动伤害 + 加成比例 * 物攻 - tar法抗 * ( 1 - 法穿 )
        elif 伤害类型 == 'AD' and 加成类型 == 'AP':
            hurt = 主动伤害 + 加成比例 * 法强 - tar护甲 * ( 1 - 破甲 )
        elif 伤害类型 == 'AP' and 加成类型 == 'AP':
            hurt = 主动伤害 + 加成比例 * 法强 - tar法抗 * ( 1 - 法穿 )
        elif 伤害类型 == 'T' and 加成类型 == 'AD':
            hurt = 主动伤害 + 加成比例 * 物攻
        elif 伤害类型 == 'T' and 加成类型 == 'AP':
            hurt = 主动伤害 + 加成比例 * 法强

    if cate == '限定技':
        限定伤害 = 查限定伤害(hero)
        伤害类型 = 查限定类型(hero)
        加成类型 = 查限定加成类型(hero)
        加成比例 = 查限定加成比例(hero)
        if 伤害类型 == 'AD' and 加成类型 == 'AD':
            hurt = 限定伤害 + 加成比例 * 物攻 - tar护甲 * (1 - 破甲)
        elif 伤害类型 == 'AP' and 加成类型 == 'AD':
            hurt = 限定伤害 + 加成比例 * 物攻 - tar法抗 * (1 - 法穿)
        elif 伤害类型 == 'AD' and 加成类型 == 'AP':
            hurt = 限定伤害 + 加成比例 * 法强 - tar护甲 * (1 - 破甲)
        elif 伤害类型 == 'AP' and 加成类型 == 'AP':
            hurt = 限定伤害 + 加成比例 * 法强 - tar法抗 * (1 - 法穿)
        elif 伤害类型 == 'T' and 加成类型 == 'AD':
            hurt = 限定伤害 + 加成比例 * 物攻
        elif 伤害类型 == 'T' and 加成类型 == 'AP':
            hurt = 限定伤害 + 加成比例 * 法强

    if hurt < 30:
        hurt = 30

    if 伤害类型 == 'AD':
        suck = 物理吸血 * hurt
    elif 伤害类型 == 'AP':
        suck = 法术吸血 * hurt
    else:
        suck = 0

    加玩家血量(tarqq, - hurt)
    加玩家血量(qqid, suck)
    return hurt

def 可用目标(qqid,cate):  # num:1是主动，2是限定
    hero = 查玩家英雄(qqid)
    nb = 查玩家编号(qqid)
    desk = 取游戏房间(qqid)
    if cate == 1:
        dd = 查主动技距离(hero)
    else:
        dd = 查限定技距离(hero)
    vilist = 取存活玩家列表(desk)
    dn = dd * 2 + 1
    tarlist = []
    if dn >= len(vilist):
        for player in vilist:
            tarlist.append(查玩家编号(player))
        if nb in tarlist:
            tarlist.remove(nb)
        return tarlist
    else:
        target = nb
        tarlist1 = []
        while len(tarlist1) < dd:
            target += 1
            if target > 8:
                target -= 8
            tarplayer = 查看指定轮玩家(desk,target)
            while 查玩家状态(tarplayer) == 'die':
                target += 1
                if target > 8:
                    target -= 8
                tarplayer = 查看指定轮玩家(desk,target)
            tarlist1.append(target)
        target = nb
        tarlist2 = []
        while len(tarlist2) < dd:
            target -= 1
            if target < 1:
                target += 8
            tarplayer = 查看指定轮玩家(desk,target)
            while 查玩家状态(tarplayer) == 'die':
                target -= 1
                if target < 1:
                    target += 8
                tarplayer = 查看指定轮玩家(desk,target)
            tarlist2.append(target)
        tarlist = tarlist1 + tarlist2
        return tarlist

def 查印记(qqid):
    with open(f'data/game/players/{qqid}.json', 'r', encoding='utf-8')as g:
        playdic = json.load(g)
    return playdic['signet']

def 加印记(qqid,num):
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        playdic = json.load(f)
        signet = playdic['signet']
        signet += num
        playdic['signet'] = signet
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(playdic, f)  # 写入数据

def 主动技能(qqid,tar):    #tar是数字

    desk = 取游戏房间(qqid)
    tarqq = 查看指定轮玩家(desk,tar)
    hurt = 普通伤害(qqid,tarqq,'主动技')

    nb = 查玩家编号(qqid)
    hero = 查玩家英雄(qqid)
    tarhero = 查玩家英雄(tarqq)

    if hero == '王昭君':
        加buff(tarqq,'🧊')
    elif hero == '孙策':
        加buff(tarqq,'🥏')
    elif hero == '眩晕':
        加buff(tarqq,'💫')

    评价 = f'{nb}.{hero}使用主动技，对{tar}.{tarhero}造成{hurt}伤害'

    return(评价)

def 限定技能(qqid,tar):    #tar是数字
    times = 查限定技次数(qqid)
    nb = 查玩家编号(qqid)
    hero = 查玩家英雄(qqid)
    desk = 取游戏房间(qqid)
    tarqq = 查看指定轮玩家(desk,tar)
    tarhero = 查玩家英雄(tarqq)
    if times < 1:
        return(f'{nb}.{hero}的限定技已用尽，跳过回合')
    else:
        减限定技次数(qqid,1)
        if hero == '鲁班七号':
            加buff(tarqq,'🛰️')
            return(f'{nb}.{hero}对{tar}.{tarhero}使用了限定技')
        elif hero == '王昭君':
            for tartar in 可用目标(qqid,2):
                tartarqq = 查看指定轮玩家(desk,tartar)
                if '🧊' in 查玩家buff(tartarqq):
                    普通伤害(qqid,tarqq,'限定技')
        elif hero == '孙策':
            普通伤害(qqid,tarqq,'限定技')
        return(f'{nb}.{hero}使用了限定技')

def 查玩家装备(qqid): #return [arm1,arm2,arm3]
    with open(f'data/game/players/{qqid}.json', 'r', encoding='utf-8')as f:
        armdic = json.load(f)  #英雄属性
        arm1 = armdic['arm1']
        arm2 = armdic['arm2']
        arm3 = armdic['arm3']
    return [arm1,arm2,arm3]

def 选装备(qqid,name): #return [arm1,arm2,arm3]
    with open(f'resource/对战/arms/物理1星.json', 'r', encoding='utf-8')as f:
        物理1星 = json.load(f)
    with open(f'resource/对战/arms/法术1星.json', 'r', encoding='utf-8')as f:
        法术1星 = json.load(f)
    with open(f'resource/对战/arms/防御1星.json', 'r', encoding='utf-8')as f:
        防御1星 = json.load(f)
    with open(f'resource/对战/arms/物理2星合成表.json', 'r', encoding='utf-8')as f:
        物理2星 = json.load(f)
    with open(f'resource/对战/arms/法术2星合成表.json', 'r', encoding='utf-8')as f:
        法术2星 = json.load(f)
    with open(f'resource/对战/arms/防御2星合成表.json', 'r', encoding='utf-8')as f:
        防御2星 = json.load(f)
    with open(f'resource/对战/arms/物理3星.json', 'r', encoding='utf-8')as f:
        物理3星 = json.load(f)
    with open(f'resource/对战/arms/法术3星.json', 'r', encoding='utf-8')as f:
        法术3星 = json.load(f)
    with open(f'resource/对战/arms/防御3星.json', 'r', encoding='utf-8')as f:
        防御3星 = json.load(f)
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        armdic = json.load(f)  #英雄属性
        arm1 = armdic['arm1']
        arm2 = armdic['arm2']
        arm3 = armdic['arm3']
        if name in 物理1星 or name in 物理2星.values() or name in 物理3星:
            arm1.append(name)
            armdic['arm1'] = arm1
        elif name in 法术1星 or name in 法术2星.values() or name in 法术3星:
            arm2.append(name)
            armdic['arm2'] = arm2
        elif name in 防御1星 or name in 防御2星.values() or name in 防御3星:
            arm3.append(name)
            armdic['arm3'] = arm3
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(armdic, f)  # 写入数据
    return name

def 合成2星(arm1,arm2,qqid):
    with open(f'resource/对战/arms/物理1星.json', 'r', encoding='utf-8')as f:
        物理1星 = json.load(f)
    with open(f'resource/对战/arms/法术1星.json', 'r', encoding='utf-8')as f:
        法术1星 = json.load(f)
    with open(f'resource/对战/arms/防御1星.json', 'r', encoding='utf-8')as f:
        防御1星 = json.load(f)
    with open(f'resource/对战/arms/物理2星合成表.json', 'r', encoding='utf-8')as f:
        物理2星 = json.load(f)
    with open(f'resource/对战/arms/法术2星合成表.json', 'r', encoding='utf-8')as f:
        法术2星 = json.load(f)
    with open(f'resource/对战/arms/防御2星合成表.json', 'r', encoding='utf-8')as f:
        防御2星 = json.load(f)
    if arm1 in 物理1星:
        newarm = 物理2星[f'{arm1}_{arm2}']
    if arm1 in 法术1星:
        newarm = 法术2星[f'{arm1}_{arm2}']
    if arm1 in 防御1星:
        newarm = 防御2星[f'{arm1}_{arm2}']
    删装备(qqid, arm1)
    删装备(qqid, arm2)
    选装备(qqid, newarm)
    return newarm

def 合成3星(arm1,arm2,arm3,qqid):
    with open(f'resource/对战/arms/物理1星.json', 'r', encoding='utf-8')as f:
        物理1星 = json.load(f)
    with open(f'resource/对战/arms/法术1星.json', 'r', encoding='utf-8')as f:
        法术1星 = json.load(f)
    with open(f'resource/对战/arms/防御1星.json', 'r', encoding='utf-8')as f:
        防御1星 = json.load(f)
    with open(f'resource/对战/arms/物理3星.json', 'r', encoding='utf-8')as f:
        物理3星 = json.load(f)
    with open(f'resource/对战/arms/法术3星.json', 'r', encoding='utf-8')as f:
        法术3星 = json.load(f)
    with open(f'resource/对战/arms/防御3星.json', 'r', encoding='utf-8')as f:
        防御3星 = json.load(f)
    if arm1 in 物理1星:
        newarm = random.choice(物理3星)
    if arm1 in 法术1星:
        newarm = random.choice(法术3星)
    if arm1 in 防御1星:
        newarm = random.choice(防御3星)
    删装备(qqid, arm1)
    删装备(qqid, arm2)
    删装备(qqid, arm3)
    选装备(qqid, newarm)
    return newarm

def 删装备(qqid,name):
    with open(f'resource/对战/arms/物理1星.json', 'r', encoding='utf-8')as f:
        物理1星 = json.load(f)
    with open(f'resource/对战/arms/法术1星.json', 'r', encoding='utf-8')as f:
        法术1星 = json.load(f)
    with open(f'resource/对战/arms/防御1星.json', 'r', encoding='utf-8')as f:
        防御1星 = json.load(f)
    with open(f'resource/对战/arms/物理2星合成表.json', 'r', encoding='utf-8')as f:
        物理2星 = json.load(f)
    with open(f'resource/对战/arms/法术2星合成表.json', 'r', encoding='utf-8')as f:
        法术2星 = json.load(f)
    with open(f'resource/对战/arms/防御2星合成表.json', 'r', encoding='utf-8')as f:
        防御2星 = json.load(f)
    with open(f'resource/对战/arms/物理3星.json', 'r', encoding='utf-8')as f:
        物理3星 = json.load(f)
    with open(f'resource/对战/arms/法术3星.json', 'r', encoding='utf-8')as f:
        法术3星 = json.load(f)
    with open(f'resource/对战/arms/防御3星.json', 'r', encoding='utf-8')as f:
        防御3星 = json.load(f)

    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        armdic = json.load(f)  #英雄属性

        if name in 物理1星 or name in 物理2星.values() or name in 物理3星:
            armlist = armdic['arm1']
            cate = 1
        elif name in 法术1星 or name in 法术2星.values() or name in 法术3星:
            armlist = armdic['arm2']
            cate = 2
        elif name in 防御1星 or name in 防御2星.values() or name in 防御3星:
            armlist = armdic['arm3']
            cate = 3

        armlist.remove(name)
        (armdic[f'arm{cate}']) = armlist
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(armdic, f)  # 写入数据
    return name

def 查玩家属性(qqid):   # return [物攻,法强,护甲,法抗,破甲,法穿,物理吸血,法术吸血,回血]
    arms = 查玩家装备(qqid)
    arms = arms[0] + arms[1] + arms[2]
    物攻 = 0   #没有攻速、没有暴击
    法强 = 0   #没有蓝条
    护甲 = 0
    法抗 = 0
    破甲 = 0
    法穿 = 0
    物理吸血 = 0
    法术吸血 = 0
    回血 = 0

    '''1星（物理、法术、防御各5件）'''

    if '暴风剑' in arms:
        物攻 += 150
    if '步月弓' in arms:
        物攻 += 50
        破甲 += 0.1
    if '鬼斧' in arms:
        物攻 += 100
        法抗 += 50
    if '流岩' in arms:
        物攻 += 100
        护甲 += 50
    if '赤血刀' in arms:
        物攻 += 50
        物理吸血 += 0.1

    if '魔法杖' in arms:
        法强 += 150
    if '火炬' in arms:
        法强 += 50
        法穿 += 0.1
    if '智慧法书' in arms:
        法强 += 100
        法抗 += 50
    if '神采之石' in arms:
        法强 += 100
        护甲 += 50
    if '水晶碎片' in arms:
        法强 += 50
        法术吸血 += 0.1

    if '骑士铠甲' in arms:
        护甲 += 150
    if '神隐面纱' in arms:
        法抗 += 150
    if '雪橇靴' in arms:
        护甲 += 75
        法抗 += 75
    if '火山圆盾' in arms:
        法抗 += 50
        回血 += 10
    if '高科技腰带' in arms:
        护甲 += 50
        回血 += 10

    '''2星（物理、法术、防御各10件，由1星装备两两合成）'''
    if '霜之哀伤' in arms:
        物攻 += 400
    if '联芒之剑' in arms:
        物攻 += 300
        护甲 += 100
    if '海妖三叉戟' in arms:
        物攻 += 300
        法抗 += 100
    if '仁义之力' in arms:
        物攻 += 200
        护甲 += 100
        法抗 += 100
    if '暗影切割者' in arms:
        物攻 += 200
        破甲 += 0.2
    if '鸣凤梳头' in arms:
        物攻 += 100
        破甲 += 0.3
    if '逐影双刃' in arms:
        物攻 += 200
        回血 += 20
    if '偃月刀' in arms:
        物攻 += 300
        物理吸血 += 0.1
    if '血月之镰' in arms:
        物攻 += 100
        物理吸血 += 0.3
    if '灭龙弩枪' in arms:
        物攻 += 300
        法强 += 200

    if '万圣节女巫帽' in arms:
        法强 += 400
    if '慈悲面具' in arms:
        法强 += 300
        护甲 += 100
    if '圣契宝典' in arms:
        法强 += 300
        法抗 += 100
    if '天使之赐' in arms:
        法强 += 200
        护甲 += 100
        法抗 += 100
    if '炙热熔炉' in arms:
        法强 += 200
        法穿 += 0.2
    if '火星图腾' in arms:
        法强 += 100
        法穿 += 0.3
    if '预言水晶球' in arms:
        法强 += 200
        回血 += 20
    if '回音法杖' in arms:
        法强 += 300
        法术吸血 += 0.1
    if '水龙杖' in arms:
        法强 += 100
        法术吸血 += 0.3
    if '神谕法刀' in arms:
        法强 += 300
        物攻 += 200

    if '铁板一块' in arms:
        护甲 += 400
    if '隐身斗篷' in arms:
        法抗 += 400
    if '亡者战甲' in arms:
        护甲 += 200
        法抗 += 200
    if '凛冬之甲' in arms:
        护甲 += 100
        法抗 += 100
        回血 += 20
    if '霜火之盾' in arms:
        护甲 += 300
        物攻 += 100
    if '破魔之盾' in arms:
        法强 += 100
        法抗 += 300
    if '飞行斗篷' in arms:
        回血 += 10
        护甲 += 300
    if '涂鸦之眼' in arms:
        回血 += 10
        法抗 += 300
    if '振奋铠甲' in arms:
        回血 += 40
    if '皇家守卫' in arms:
        护甲 += 100
        法抗 += 100
        物攻 += 100
        法强 += 100
        回血 += 10

    '''3星（共6个）'''
    if '烈阳弓' in arms:
        物攻 += 200
        破甲 += 0.4
        加buff(qqid,'🏹')
    if '斩炎' in arms:
        物攻 += 400
        物攻 = 物攻 * 1.2
        加buff(qqid,'⚔')

    if '灵魂魔匣' in arms:
        法强 += 600
        加buff(qqid,'📦')
    if '月之沙漏' in arms:
        法强 += 300
        法强 = 法强 * 1.3
        加buff(qqid,'⌛')

    if '长者的庇护' in arms:
        护甲 += 300
        法抗 += 300
        加buff(qqid,'🧓')
    if '治疗图腾' in arms:
        回血 += 60
        加buff(qqid,'📌')

    return [物攻,法强,护甲,法抗,破甲,法穿,物理吸血,法术吸血,回血]

def 查玩家buff(qqid):
    with open(f'data/game/players/{qqid}.json', 'r', encoding='utf-8')as f:
        herodic = json.load(f)  #英雄属性
    return(herodic['buff'])

def 查限定技总次数(hero):
    with open(f'resource/对战/heroes/{hero}.json', 'r', encoding='utf-8')as f:
        herodic = json.load(f)  #英雄属性
    return (herodic['x'])

def 战场(qqid,desk):
    playerlist = 取存活玩家列表(desk)
    field = f'desk:{desk}'
    for player in playerlist:
        if 查玩家编号(player) == 查玩家编号(qqid):
            num = '你'
        else:
            num = 查玩家编号(player)
        hero = 查玩家英雄(player)
        buff = str()
        for bbb in 查玩家buff(player):
            buff += bbb
        field += f'\r{num}—🩸{查玩家血量(player)}' + buff + 取头像(hero)
    return field

def 查行动时间(qqid):
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        playdic = json.load(f)
    actime = playdic['act_time']
    now = int(time.time())
    asd = now - actime
    return asd

def 开始行动计时(qqid):
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        playdic = json.load(f)
        playdic['act_time'] = int(time.time())
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(playdic, f)  # 写入数据

def 开始选英雄计时(desk):
    with open(f'data/game/游戏{desk}.json', 'r+', encoding='utf-8')as f:
        playdic = json.load(f)
        playdic['time'] = int(time.time())
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(playdic, f)  # 写入数据

def 进入选装备(desk):
    with open(f'data/game/游戏{desk}.json', 'r+', encoding='utf-8')as f:
        playdic = json.load(f)
        actimes = playdic['actimes']
        actimes += 1
        playdic['actimes'] = actimes
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(playdic, f)  # 写入数据
    if actimes > 7:
        with open(f'data/game/游戏{desk}.json', 'r+', encoding='utf-8')as f:
            playdic = json.load(f)
            playdic['actimes'] = 0
            f.seek(0)  # 指向文本开头
            f.truncate()  # 清空文本
            json.dump(playdic, f)  # 写入数据
        return True
    else:
        return False

def 结束选英雄(desk):
    with open(f'data/game/游戏{desk}.json', 'r', encoding='utf-8')as f:
        playdic = json.load(f)
    time1 = playdic['time']
    timenow = int(time.time())
    dtime = timenow - time1
    if dtime > 45:
        return True
    else:
        return False

def 取游戏群列表(desk,groupid):   #取该局群列表，加上当前观战群
    gamegroup = [str(groupid)]
    for players in 取玩家列表(desk):
        group = 取玩家群(players)
        gamegroup.append(group)
    return (list(set(gamegroup)))

def 生成装备库(desk):
    with open(f'resource/对战/arms/物理1星.json', 'r', encoding='utf-8')as f:
        物理1星 = json.load(f)
    with open(f'resource/对战/arms/法术1星.json', 'r', encoding='utf-8')as f:
        法术1星 = json.load(f)
    with open(f'resource/对战/arms/防御1星.json', 'r', encoding='utf-8')as f:
        防御1星 = json.load(f)

    armlist = 物理1星 + 法术1星 + 防御1星
    arms = random.choices(armlist,k=10)

    with open(f'data/game/游戏{desk}.json', 'r+', encoding='utf-8')as f:
        playdic = json.load(f)
        playdic['armlist'] = arms
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(playdic, f)  # 写入数据

    return arms

def 取装备库(desk):
    with open(f'data/game/游戏{desk}.json', 'r', encoding='utf-8')as f:
        playdic = json.load(f)
    return playdic['armlist']

def 开始选装备(desk):  #返回开始选秀公告
    for players in 取玩家列表(desk):
        设置玩家选装状态(players,0)
        if 查玩家英雄(players) == '未选择':
            选玩家英雄(players,'鲁班七号')
    mes1 = f'本轮随机装备：{生成装备库(desk)}'
    return mes1

def 开始对战(desk):  #返回开始对战公告
    for players in 取玩家列表(desk):
        改玩家状态(players,'vivi')
        改技能类别(players,0)
        if 查玩家英雄(players) == '未选择':
            帮选玩家英雄(players)
    turn = random.randint(1, 8)
    设置当前行动轮(desk,turn)
    player = 查看当前轮玩家(desk)
    hero = 查玩家英雄(player)
    mes1 = f'当前行动玩家：{turn}号，{player}' + 取头像(hero) + '请ta发送【主动技】或【限定技】或【跳过】'
    return mes1

def 取头像(name):
    img = MessageSegment.image(f'file:///C:\\Users\\86156\\Desktop\\py\\ailin\\resource\\对战\\head\\{name}.jpg')
    return (img)

def 取卡图(name):
    img = MessageSegment.image(f'file:///C:\\Users\\86156\\Desktop\\py\\ailin\\resource\\对战\\heroes\\{name}.png')
    return (img)

def 取等候群列表():
    with open('data/game/等候群.json', 'r', encoding='utf-8')as g:
        playdic = json.load(g)
    wait = playdic.values()
    wait = list(set(wait))
    return (wait)

def 取玩家群(qqid):
    with open(f'data/game/players/{qqid}.json', 'r', encoding='utf-8')as g:
        playdic = json.load(g)
    return (playdic['group'])

def 取游戏房间(qqid):
    with open(f'data/game/players/{qqid}.json', 'r', encoding='utf-8')as g:
        playdic = json.load(g)
    return (playdic['desk'])

def 取最新房间():
    with open(f'data/game/数据.json', 'r', encoding='utf-8')as g:
        playdic = json.load(g)
        desk = playdic['gametimes']
    return (desk)

def 查看玩家选装状态(qqid): #1是不可选装
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
    return dic['armstate']

def 设置玩家选装状态(qqid,state): #1是不可选装
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic['armstate'] = state
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 改玩家状态(qqid,state):
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic['state'] = state
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 查玩家英雄(qqid):  #返回英雄名
    with open(f'data/game/players/{qqid}.json', 'r', encoding='utf-8')as f:
        playdic = json.load(f)
    return(playdic['hero'])

def 帮选玩家英雄(qqid):  #返回英雄名
    if not os.path.exists(f'data/艾琳/卡包/{qqid}.json'):
        with open(f'data/艾琳/卡包/{qqid}.json', 'w+', encoding='utf-8')as f:
            cardlist = ['鲁班七号']
            json.dump(cardlist, f)  # 写入数据
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        playdic = json.load(f)
        cardlist = 查卡包(qqid)
        hero = random.choice(cardlist)
        playdic['hero'] = hero
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(playdic, f)  # 写入数据

def 查玩家编号(qqid):
    with open(f'data/game/players/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return(dic['nb'])

def 查玩家血量(qqid):
    with open(f'data/game/players/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return(dic['hp'])

def 查限定技次数(qqid):
    with open(f'data/game/players/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return(dic['x'])

def 减限定技次数(qqid,num):
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic['x'] -= num
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 改限定技次数(qqid,num):
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic['x'] = num
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据

def 加玩家血量(qqid,num):
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        hp = dic['hp']
        dic['hp'] = int(hp + num)
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据
    return(dic['hp'])

def 加buff(qqid,name):
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        buff = dic['buff']
        buff.append(name)
        dic['buff'] = buff
        if len(buff) > 1:
            dic['buff'] = list(set(dic['buff']))
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据
    return(dic['buff'])

def 移除buff(qqid,name):
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        buff = dic['buff']
        buff.remove(name)
        dic['buff'] = buff
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据
    return(dic['buff'])

def 选玩家英雄(qqid,hero):
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic['hero'] = hero
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据
    return(hero)

def 查玩家状态(qqid):  #返回状态名
    with open(f'data/game/players/{qqid}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return(dic['state'])

def 查看当前轮玩家(desk):  #返回qq号
    turn = 取当前行动轮(desk)
    playerlist = 取玩家列表(desk)
    player = playerlist[turn - 1]
    return (player)

def 查看指定轮玩家(desk , tar):  #返回qq号
    playerlist = 取玩家列表(desk)
    tarr = int(str(tar)) - 1
    player = playerlist[tarr]
    return player

def 设置当前行动轮(desk,turn):  #设置轮次，返回无
    with open(f'data/game/游戏{desk}.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic['turn'] = turn
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据
    qqid = 查看当前轮玩家(desk)
    改玩家状态(qqid, 'act')

def 取当前行动轮(desk):   #只返回轮数
    with open(f'data/game/游戏{desk}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
        player = dic['turn']
    return player

def 取玩家名单(desk):
    with open(f'data/game/游戏{desk}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    playerlist = 'playerslist\r'
    for pl in range (0,8):
        playerqq = dic[f'player{pl + 1}']
        playerlist = playerlist + f'{pl + 1}：{playerqq}\r'
    return playerlist

def 取玩家列表(desk):
    with open(f'data/game/游戏{desk}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    return(dic['playerlist'])

def 取存活玩家列表(desk):
    with open(f'data/game/游戏{desk}.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    playlist = dic['playerlist']
    for num in range(len(playlist) - 1, -1, -1):
        player = playlist[num]
        if 查玩家状态(player) == 'die':
            playlist.remove(player)
    return(playlist)

def 取当前匹配队列():
    with open('data/game/匹配队列.json', 'r', encoding='utf-8')as f:  #清空队列
        playerlist = json.load(f)
    return(playerlist)

def 开始游戏():
    with open('data/game/数据.json', 'r+', encoding='utf-8')as f: #写入游戏局数信息
        dic = json.load(f)
        gametimes = str(dic['gametimes'])
        dic['gametimes'] = int(gametimes) + 1
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据
    with open('data/game/匹配队列.json', 'r+', encoding='utf-8')as f:  #清空匹配队列
        playerlist = json.load(f)
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump([], f)  # 写入空集
    with open(f'data/game/游戏{gametimes}.json', 'w+', encoding='utf-8')as f:  #写入该局游戏信息
        for pl in range (0,8):
            dic[f'player{pl + 1}'] = playerlist[pl]  #玩家qq
            with open(f'data/game/players/{playerlist[pl]}.json', 'w+', encoding='utf-8')as g: #写入玩家信息
                playerdata = {'desk':gametimes,'hp':1000,'hero':'未选择','x':1,'arm1':[],'arm2':[],'arm3':[],'buff':[],'state':'pre','armstate':0,'nb':pl + 1,'cate':0,'signet':0}
                with open(f'data/game/等候群.json', 'r+', encoding='utf-8')as h:   #抽空等候群字典
                    playerdic = json.load(h)
                    if playerlist[pl] in playerdic:
                        group = playerdic[playerlist[pl]]
                        del playerdic[playerlist[pl]]
                    else:
                        group = '758643551'
                    h.seek(0)  # 指向文本开头
                    h.truncate()  # 清空文本
                    json.dump(playerdic, h)  # 挖空
                playerdata['group'] = group
                json.dump(playerdata, g)  # 写入玩家信息
        dic['playerlist'] = playerlist
        dic['actimes'] = 0
        json.dump(dic, f)  # 写入游戏局信息
    return '请所有玩家在45秒内选择英雄，直接发英雄名字即可，发送【卡包】查看自己已有英雄'

def 发放奖励(qqid,no):
    with open(f'data/game/players/{qqid}.json', 'r+', encoding='utf-8')as f:  #修改玩家房间信息
        playerdata = json.load(f)
        playerdata['desk'] = 0
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(playerdata, f)  # 写入数据
    if no > 2:
        if no == 8:
            coin = 50
        elif no == 7:
            coin = 100
        elif no == 6:
            coin = 150
        elif no == 5:
            coin = 200
        elif no == 4:
            coin = 250
        elif no == 3:
            coin = 300
        return f'{qqid}第{no}名，获得{coin}金币。'
    if no <= 2:
        coin = 350
        wincoin = 400
        desk = 取游戏房间(qqid)
        vilist = 取存活玩家列表(desk)
        winid = vilist[0]
        改玩家状态(winid, 'win')
        return f'{qqid}第2名，获得{coin}金币；{winid}第1名，获得{wincoin}金币。'

def 加入匹配队列(qqid,groupid):
    if os.path.exists(f'data/game/players/{qqid}.json'):
        with open(f'data/game/players/{qqid}.json', 'r', encoding='utf-8')as f:
            playerdata = json.load(f)
            if playerdata['desk'] != 0 and qqid != '3142331296':
                return f'{qqid}已在游戏中，请专心游戏'
    with open('data/game/匹配队列.json', 'r+', encoding='utf-8')as f:
        playerlist = json.load(f)
        if qqid in playerlist and qqid != '3142331296':
            return f'{qqid}已在匹配队列，当前队列人数：{len(playerlist)}/8'
        else:
            playerlist.append(qqid)  # 加入
            f.seek(0)  # 指向文本开头
            f.truncate()  # 清空文本
            json.dump(playerlist, f)  # 写入数据
    with open('data/game/等候群.json', 'r+', encoding='utf-8')as f:
        dic = json.load(f)
        dic[qqid] = groupid # 标记群
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据
    if len(playerlist) < 8:
        return f'{qqid}已加入匹配队列，当前队列人数：{len(playerlist)}/8'
    else:
        return f'{qqid}已加入匹配队列，人够了，请发送“开始游戏”！'

def 随机卡():
    with open('resource/对战/英雄奖池.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
        card = random.choice(dic)
    return card

def 抽卡(qqid, num):
    if not os.path.exists(f'data/艾琳/卡包/{qqid}.json'):
        with open(f'data/艾琳/卡包/{qqid}.json', 'w+', encoding='utf-8')as f:
            playerlist = []
            json.dump(playerlist, f)  # 写入数据
    with open(f'data/艾琳/卡包/{qqid}.json', 'r+', encoding='utf-8')as f:
        playerlist = json.load(f)
        cardlist = []
        for ii in range (0,num):
            card = 随机卡()
            if not card in playerlist:
                playerlist.append(card)   #放入卡包（如果卡包里没有）
            cardlist.append(card)  #记录抽到的卡
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(playerlist, f)  # 写入数据
    return(cardlist)

def 查卡包(qqid):
    if not os.path.exists(f'data/艾琳/卡包/{qqid}.json'):
        with open(f'data/艾琳/卡包/{qqid}.json', 'w+', encoding='utf-8')as f:
            cardlist = []
            json.dump(cardlist, f)  # 写入数据
    with open(f'data/艾琳/卡包/{qqid}.json', 'r', encoding='utf-8')as f:
        cardlist = json.load(f)
    return (cardlist)