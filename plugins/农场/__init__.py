from nonebot.adapters.onebot.v11 import MessageSegment   #发图片用的
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot import on_command
from nonebot.permission import SUPERUSER

import time,re,random

from plugins.fun import *
from plugins.农场.farm import *

抽奖1 = on_command("抽奖")
挖矿1 = on_command("挖矿",aliases={"淘金","采矿","群里采矿","群里挖矿","群里淘金","沙里淘金","获得金币"})

种植1 = on_command("种植", aliases={"种庄稼"})
喂养1 = on_command("喂养", aliases={"饲养","养殖"})
种1 = on_command("种", aliases={"养","制作"})

农场菜单1 = on_command("农场")
图鉴1 = on_command("图鉴", aliases={"物品大全","植物","动物","建筑","物品"})
土地1 = on_command("我的物品", aliases={"我的背包","背包","我的土地","我的田地","我的农场","查询"})
设置1 = on_command("设置", aliases={"饰品","首饰","服饰","宠物"})

货架1 = on_command("我的货架", aliases={"货架","我的商品","我的店铺"})
商店1 = on_command("商店", aliases={"商铺","店铺","商场","市场","商城","商品"})
购买1 = on_command("购买", aliases={"买"})
出售1 = on_command("出售", aliases={"上架","上新"})

加物品1 = on_command("加物品", permission=SUPERUSER)
丰收1 = on_command("丰收", permission=SUPERUSER)

商品1 = on_command("土地", aliases={

"小麦","玉米","胡萝卜","大豆","甘蔗","木蓝","南瓜","棉花","辣椒","西红柿","草莓","土豆","水稻","生菜","向日葵","洋葱","茶叶","牡丹花","葡萄","高粱","人参","咖啡豆","桑椹",

"母鸡","奶牛","猪","绵羊","孔雀","鱼","牛","貂","蚕","寻回犬","虎斑猫","杜宾犬","三色猫","栗色马","猎犬","燕尾服猫","小白兔","帕洛米诺马","品托马","安达卢西亚马","毛驴","加菲猫",

"蛋","奶","肉","羽毛","羊毛",

"面包","黄油","奶酪","白糖","红糖","糖浆","爆米花","奶油爆米花","煎饼","烤土豆","烤肉","千层面","胡萝卜派","南瓜派","蛋糕","果汁","香草冰淇淋","草莓冰淇淋","雪糕","草莓酱","浆果沙冰","咖啡","白酒","葡萄酒","啤酒","寿司","三明治",

"金条","铁","铜","银","铂金","银项链","银手镯","金项链","金手镯","铂金项链","铂金手镯","钻戒",

"皮革","貂皮","丝绸","皮衣","羊毛衫","旗袍",

"铁矿石","金矿石","银矿石","铜矿石","铂金矿石","钻石",

"面包房","制奶厂","制糖厂","爆米花烤锅","烧烤架","烤炉","织布机","炼金炉","果汁机","冰淇淋机","果酱机","酿酒厂","珠宝店","咖啡亭","寿司吧","三明治店","沙冰机"
                                })

@抽奖1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取签到人qq号
    当前金币 = 查金币(qq_id)
    msg = str(event.message)
    if msg == '抽奖':
        次数 = 1
    elif len(msg.split()) == 2:
        次数 = int(msg.split()[1])
    else:
        次数 = int(msg.split('抽奖')[0])
    if 次数 > 1:
        操作名 = f'{次数}连抽'
    else:
        操作名 = '抽奖'
    需要金币 = 100 * 次数
    if 当前金币 < 需要金币 and qq_id != '3142331296':
        await 抽奖1.send(f"低于{需要金币}金币不得{操作名}，发“签到”或“采矿”获得金币")
        return()
    变更金币 = 0
    礼品集 = []
    for nnn in range(0,次数):
        随机 = random.randint(1, 100)
        if 随机 < 2:
            礼品 = random.choice(查图鉴('builds'))
            礼品集.append(礼品)
            加物品(qq_id,礼品,1)
        else:
            变更金币 += random.randint(-200, 197)
    加金币(qq_id, 变更金币)
    await 抽奖1.send(f"{操作名}获得{变更金币}金币，当前金币：{查金币(qq_id)}")
    if len(礼品集) > 0:
        await 抽奖1.send(f"中大奖，获得{礼品集}，发“农场”查看玩法")
        await 抽奖1.send(f"防刷屏可以采用连抽，例如“抽奖 5”就是5连抽，注意空格")

@挖矿1.handle()
async def _(bot:Bot,event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取qq号
    group_id = event.group_id   # 获取群号
    群人数 = (await bot.get_group_info(group_id=group_id))["member_count"]
    if 群人数 < 100 and group_id != 758643551 and group_id != 468586270 and group_id != 223296112:
        await 挖矿1.send(f"此群人数较少，暂不支持挖矿，发送“功能”查看更多功能")
    else:
        新群(group_id)
        with open(f'data/艾琳/群/{group_id}.json', 'r+', encoding='utf-8')as f:
            dic = json.load(f)
            挖矿人数 = dic['MiningTimes']
            挖矿人数 += 1
            获得金币 = int(群人数 * 0.8 ** 挖矿人数)
            if 获得金币 < 1:
                await 挖矿1.send(f"由于此群挖矿人数太多，金币已枯竭，换其他群试试")
            elif re.search(qq_id, str(dic)) and qq_id != '3142331296':
                await 挖矿1.send(f"你已经采过矿了，同一个群不能重复采矿，邀艾琳到其他群试试")
            else:
                加金币(qq_id,获得金币)
                dic['MiningTimes'] = 挖矿人数
                dic[f'Miner{挖矿人数}'] = qq_id
                f.seek(0)  # 指向文本开头
                f.truncate()  # 清空文本
                json.dump(dic, f)  # 写入数据
                await 挖矿1.send(f"此群{群人数}人，你是第{挖矿人数}个挖矿的，获得金币{获得金币}，当前金币：{查金币(qq_id)}")
                礼品 = random.choice(查图鉴('mines'))
                加物品(qq_id,礼品,1)
                await 抽奖1.send(f"中大奖，获得1{礼品}，发“农场”查看玩法")

@设置1.handle()
async def _(event: GroupMessageEvent):
    qqid = str(event.user_id)
    msg = str(event.message)
    if len(msg.split()) == 1:
        await 设置1.send('指令：\r'
                   '设置饰品/服饰/宠物 xxx\r'
                   '例如：设置服饰 羊毛衫\r'
                    '        设置服饰 随机')
        return()
    指令 = msg.split()[0]
    指令 = 指令.split('设置')[1]
    value1 = msg.split()[1]
    if 指令 == '饰品' or 指令 == '服饰' or 指令 == '宠物':
        if 指令 == '饰品':
            key1 = 'jewelry'
            物品集 = 查珠宝(qqid)
        elif 指令 == '服饰':
            key1 = 'clothes'
            物品集 = 查衣服(qqid)
        elif 指令 == '宠物':
            key1 = 'pet'
            物品集 = list(查动物(qqid).keys())
        if value1 not in 物品集 and value1 != '随机':
            await 设置1.send(f'你的{指令}：{物品集}')
        elif value1 == '随机':
            设置饰物(qqid,key1,'rnd')
            await 设置1.send(f'设置随机完成，查询时显示随机{指令}')
        else:
            设置饰物(qqid,key1,value1)
            await 设置1.send('设置完成，发送“查询”即可查看')

@加物品1.handle()
async def _(event: GroupMessageEvent):
    msg = str(event.message)
    qqid = msg.split()[1]
    good = msg.split()[2]
    num = msg.split()[3]
    加物品(qqid,good,num)
    await 加物品1.send('加物品完成')

@丰收1.handle()
async def _(event: GroupMessageEvent):
    丰收('3142331296')
    await 丰收1.send('丰收完成')

@农场菜单1.handle()
async def _(event: GroupMessageEvent):
    await 农场菜单1.send(MessageSegment.image(r'file:///C:\\Users\\86156\\Desktop\\py\\ailin\\resource\\farmmenu.png'))

@图鉴1.handle()
async def _(event: GroupMessageEvent):
    await 农场菜单1.send(MessageSegment.image(r'file:///C:\\Users\\86156\\Desktop\\py\\ailin\\resource\\list.png'))

@种植1.handle()
async def _(event: GroupMessageEvent):
    await 种植1.send('发送“种xxx + 空格 + 数量”进行种植，例如“种小麦 10”')

@喂养1.handle()
async def _(event: GroupMessageEvent):
    await 喂养1.send('发送“养xxx + 空格 + 数量”进行喂养，例如“养绵羊 10”')

@出售1.handle()
async def _(event: GroupMessageEvent):
    qqid = str(event.user_id)
    msg = (str(event.message)).split()
    物品 = (msg[0]).split('出售')[1]
    if len(msg) == 3:
        价格 = int(msg[1])
        数量 = int(msg[2])
    elif len(msg) == 2:
        价格 = int(msg[1])
        数量 = 1
    elif len(msg) == 1:
        await 出售1.send(f'发送“出售xxx 单价 数量”进行出售，例如“出售小麦 20 1”')
        return()
    if 数量 > 查数量(qqid,物品):
        await 出售1.send(f'你只有{查数量(qqid,物品)}件')
    elif 价格 < 0 or 数量 < 0:
        await 出售1.send('不能为负数')
    else:
        价值 = 查价值(物品)
        if 价格 <= 价值 and 物品 != '土地':
            获得金币 = 价格 * 数量
            加金币(qqid,获得金币)
            加物品(qqid,物品, - 数量)
            await 出售1.send(f'低于标准价，自动售出，获得{获得金币}金币')
        else:
            商品上新(物品,价格,数量,qqid)
            await 出售1.send('上架成功，发送“我的货架”可查看')

@商店1.handle()
async def _(event: GroupMessageEvent):
    商品 = 全部商品()
    第一页 = str()
    第二页 = str()
    for goods in 商品:
        随机 = random.choice([1,2])
        if 随机 == 1:
            第一页 += goods + '，'
        else:
            第二页 += goods + '，'
    await 商店1.send(f'第一页：{第一页}')
    await 商店1.send(f'第二页：{第二页}')
    await 商店1.send('请发送你想查看的商品名，例如“土地”')

@商品1.handle()
async def act_handler(event: GroupMessageEvent):
    msg = str(event.message)
    qqid = str(event.user_id)
    if not 物品查询(msg) is None:
        await 商品1.send(f'•{物品查询(msg)}')
    商品信息 = 查商品(msg)
    if 商品信息[1] > 0:
        await 商品1.send(f'成品：{msg}\r最低价：{商品信息[0]}金币\r库存：{商品信息[1]}\r出售人：{商品信息[2]}')
        await 商店1.send('请发送购买数量，例如：5，不买请发送数字：0')
        准备购买(qqid, msg)

@商品1.got('text')
async def act_handler(event: GroupMessageEvent, state: T_State):
    qqid = str(event.user_id)
    msg = str(state["text"])
    物品类型列表 = 查看图鉴().keys()
    for 物品类型 in 物品类型列表:
        if msg in 查看图鉴()[物品类型]:
            await 商品1.send(f'•{物品查询(msg)}')
            return()
    商品名 = 查订单(qqid)
    购买数量 = int(msg)
    具体信息 = 查商品(商品名)  #return [最低价,库存,出售人]
    购买价格 = 具体信息[0]
    玩家金币 = 查金币(qqid)
    需要金币 = 购买数量 * 购买价格
    if 购买数量 > 具体信息[1]:
        await 商品1.send(f'该价格库存只有{具体信息[1]}件')
    elif 购买数量 < 0:
        await 商品1.send('不能为负数')
    elif 玩家金币 < 需要金币 and qqid != '3142331296':
        await 商品1.send(f'一共需要{需要金币}，你的金币不足，可以售卖物品获得金币')
    else:
        减金币(qqid,需要金币)
        加金币(具体信息[2],需要金币)
        加物品(qqid,商品名,购买数量)
        出售人 = 具体信息[2]
        商品售出(商品名,购买数量,出售人)
        await 商品1.send(f'购买完成，发送“查询”可以查看')

@土地1.handle()
async def _(event: GroupMessageEvent):
    qqid = str(event.user_id)
    if len((str(event.message)).split()) > 1:
        qqid = (str(event.message)).split()[1]
    coin = 查金币(qqid)
    丰收(qqid)

    await 土地1.send(f'用户：{qqid}\r'
                   f'金币：{coin}\r'
                   f'土地：{查空闲土地(qqid)}/{查土地数量(qqid)}'
                   f'{饰品信息(qqid)}'
                   f'{服饰信息(qqid)}'
                   f'{宠物信息(qqid)}')

    for 类型 in ['植物','动物','物品','建筑']:
        物品集 = str()
        if 类型 == '物品':
            mylist = 查物品(qqid)
        elif 类型 == '建筑':
            mylist = 查建筑(qqid)
        elif 类型 == '植物':
            mylist = 查植物(qqid)
        elif 类型 == '动物':
            mylist = 查动物(qqid)
        for 物品 in mylist:
            数量 = 查数量(qqid, 物品)
            if 数量 != 0:
                物品集 += 物品 + str(数量) + '|'
        if len(mylist) > 0:
            await 土地1.send(f'{类型}:{物品集}')

    landic = 查土地(qqid)
    生产列表 = landic.keys()
    生产集 = str()
    if len(生产列表) > 0:
        for 生产 in 生产列表:
            生产集 += 生产 + str(landic[生产]) + ','
        await 土地1.send(f'生产中:{生产集}')

@货架1.handle()
async def _(event: GroupMessageEvent):
    qqid = str(event.user_id)
    我的货架 = 查货架(qqid)
    货架集 = str()
    商品列表 = 我的货架.keys()
    for 商品 in 商品列表:
        货架 = 我的货架[商品]
        货架集 += '\r' + 商品 + ' 单价' + str(货架[0]) + ',' + str(货架[1]) + '件'
    await 货架1.send(f'用户：{qqid}'
                   f'{货架集}')

@种1.handle()
async def _(event: GroupMessageEvent):
    qqid = str(event.user_id)

    '''检测数值'''

    msg = str(event.message)
    if len(msg.split()) == 2:
        数量 = int(msg.split()[1])
        msg = msg.split()[0]
    else:
        数量 = 1

    '''判断操作类型（种、养、制作）'''

    指令 = msg[0]
    if 指令 == '种':
        art = msg.split('种')[1]
    elif 指令 == '养':
        art = msg.split('养')[1]
    elif 指令 == '制':
        art = msg.split('制作')[1]

    '''判断土地是否足够'''

    if 指令 != '制':
        if 查土地数量(qqid) == 0:
            await 种1.send('你还没有土地，发送“商店”购买土地')
            return()
        if 查空闲土地(qqid) < 数量:
            await 种1.send('空闲土地不足，发送“商店”购买土地，发送“我的土地”查看土地')
            return()

    '''判断原料是否足够'''

    if 指令 == '养':
        原料集 = 查原料(art)
        需要数量 = 数量 * 原料集[1]
        原料名 = 原料集[0]
        拥有数量 = 查数量(qqid,原料名)
        if 拥有数量 < 需要数量:
            if 原料名 in 查图鉴('raws'):
                await 种1.send(f'需要{需要数量}个{原料名}，你只有{拥有数量}个，请先“养{查原料(原料名)}”，也可以发“商店”购买')
            elif 原料名 in 查图鉴('plants'):
                await 种1.send(f'需要{需要数量}个{原料名}，你只有{拥有数量}个，请先“种{原料名}”，也可以发“商店”购买')
            elif 原料名 in 查图鉴('as'):
                await 种1.send(f'需要{需要数量}个{原料名}，你只有{拥有数量}个，请先“制作{原料名}”，也可以发“商店”购买')
            return()
    elif 指令 == '制':
        if art == '羊毛衫':
            原料集 = ['羊毛','木蓝']
            for 单个原料 in 原料集:
                拥有数量 = 查数量(qqid,单个原料)
                需要数量 = 8
                if 拥有数量 < 需要数量:
                    原料名 = 单个原料
                    if 原料名 in 查图鉴('builds') and 拥有数量 < 1:
                        await 种1.send(f'需要{原料名}，请先“抽奖”，也可以发“商店”购买')
                        return ()
                    elif 原料名 in 查图鉴('raws'):
                        await 种1.send(f'需要8{原料名}，请先“养{查原料(原料名)}”，也可以发“商店”购买')
                        return ()
                    elif 原料名 in 查图鉴('plants'):
                        await 种1.send(f'需要8{原料名}，请先“种{原料名}”，也可以发“商店”购买')
                        return ()

        else:
            原料集 = 查原料(art)
            for 单个原料 in 原料集:
                拥有数量 = 查数量(qqid,单个原料)
                需要数量 = 数量
                if 拥有数量 < 需要数量:
                    原料名 = 单个原料
                    if 原料名 in 查图鉴('raws'):
                        await 种1.send(f'需要{原料名}，请先“养{查原料(原料名)}”，也可以发“商店”购买')
                        return ()
                    elif 原料名 in 查图鉴('mines'):
                        await 种1.send(f'需要{原料名}，请先“采矿”，也可以发“商店”购买')
                        return ()
                    elif 原料名 in 查图鉴('builds') and 拥有数量 < 1:
                        await 种1.send(f'需要{原料名}，请先“抽奖”，也可以发“商店”购买')
                        return ()
                    elif 原料名 in 查图鉴('plants'):
                        await 种1.send(f'需要{原料名}，请先“种{原料名}”，也可以发“商店”购买')
                        return ()
                    elif 原料名 in 查图鉴('animals'):
                        await 种1.send(f'需要{原料名}，请先“养{原料名}”，也可以发“商店”购买')
                        return ()
                    elif 原料名 in 查图鉴('as'):
                        await 种1.send(f'需要{原料名}，请先“制作{原料名}”，也可以发“商店”购买')
                        return()

    '''判断金币是否足够'''
    if 指令 == '制':
        需要金币 = 0
        需要时间 = int(600 / (1 + 查数量(qqid,查原料(art)[0])))
    else:
        需要金币 = 数量 * 查价格(art)
        需要时间 = str(查时间(art))
    coin = 查金币(qqid)

    if coin < 需要金币:
        await 种1.send(f'需要{需要金币}，你的金币不足，可以售卖物品获得金币')
    else:
        减金币(qqid,需要金币)
        生产(qqid, art, 数量)
        await 种1.send(f'操作完成，等待{需要时间}分钟后收获，发送“我的土地”查看实时情况')
