from typing import List
import time

from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Message
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11.helpers import Numbers
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot import on_command

from plugins.fun import *
from plugins.对战.main import *

查卡1 = on_command("英雄名",aliases={"鲁班七号","小鱼","周瑜","小乔","大乔","诸葛亮","庄周","孙策","艾琳","孙尚香","王昭君","鲁班大师","妲己","亚瑟","瑶","戈娅","武则天"})
选装备1 = on_command("装备名",aliases={"流岩","暴风剑","鬼斧","步月弓","赤血刀","魔法杖","神采之石","智慧法书","水晶碎片","火炬","高科技腰带","火山圆盾","神隐面纱","骑士铠甲","雪橇靴"})
查看装备1 = on_command("查装备",aliases={"查看装备","我的装备"})
合成表1 = on_command("合成表",aliases={"合成大全","装备大全"})

抽卡1 = on_command("抽卡",aliases={"抽英雄", "获得卡牌" ,"获得英雄"})
查卡包1 = on_command("查卡包",aliases={"我的英雄","我的卡包","卡包"})
加入1 = on_command("开始匹配",aliases={"对战","匹配","加入对战"})
玩家名单1 = on_command("玩家名单",aliases={"玩家","准备","匹配名单","玩家列表"})
存活玩家1 = on_command("存活名单",aliases={"存活玩家"})
开始游戏1 = on_command("开始游戏",aliases={"开始"})

主动技可用目标1 = on_command('主动技可用目标', aliases={'主动技范围'})
限定技可用目标1 = on_command('限定技可用目标', aliases={'限定技范围'})
行动1 = on_command('主动技', aliases={'小技能','主动技能','限定技','大招'})
跳过1 = on_command('跳过', aliases={'过'})
战场1 = on_command('战场', aliases={'查看战场'})
当前游戏群1 = on_command('当前游戏群', aliases={'查看当前游戏群'})

查玩家1 = on_command("查玩家",aliases={"查看玩家"}, permission=SUPERUSER)
群人数1 = on_command('群人数', aliases={'当前群人数'}, permission=SUPERUSER)
帮选1 = on_command('帮选', permission=SUPERUSER)
设置群名1 = on_command('设置群名', permission=SUPERUSER)
开始对战1 = on_command("开始对战",aliases={"开战"}, permission=SUPERUSER)
开始选装1 = on_command("开始选装",aliases={"选秀","选装"}, permission=SUPERUSER)

@合成表1.handle()
async def _():
    图 = r'file:///C:\\Users\\86156\\Desktop\\py\\ailin\\data\\game\\arms\\合成表.png'
    await 合成表1.send(MessageSegment.image(图))

@设置群名1.handle()
async def _(bot:Bot ,event: GroupMessageEvent):
    name = str(event.message).split()[1]
    await bot.set_group_name(group_id = event.group_id , group_name = name)

@帮选1.handle()
async def _(bot:Bot ,event: GroupMessageEvent):
    qqid = str(event.user_id)
    turn = str(event.message).split()[1]
    hero = str(event.message).split()[2]
    desk = 取游戏房间(qqid)
    qqid = 查看指定轮玩家(desk,turn)
    选玩家英雄(qqid,hero)
    await 帮选1.send('完毕')

@查看装备1.handle()
async def _(bot:Bot ,event: GroupMessageEvent):
    if str(event.message) == '我的装备' or str(event.message) == '查看装备' or str(event.message) == '查装备':
        qqid = event.user_id
        arms = 查玩家装备(qqid)
        arms = arms[0] + arms[1] + arms[2]
        属性 = 查玩家属性(qqid)   # return [物攻,法强,护甲,法抗,破甲,法穿,物理吸血,法术吸血,回血]
        await 查看装备1.send(f'{qqid}当前装备：{arms}')
        await 查看装备1.send(f'{qqid}\r物攻：{属性[0]}\r法强：{属性[1]}\r护甲：{属性[2]}\r法抗：{属性[3]}\r破甲：{属性[4]*100}%\r法穿：{属性[5]*100}%\r物理吸血：{属性[6]*100}%\r法术吸血：{属性[7]*100}%\r回血：{属性[8]}')
    else:
        qqid = str(event.message).split()[1]
        arms = 查玩家装备(qqid)
        arms = arms[0] + arms[1] + arms[2]
        属性 = 查玩家属性(qqid)  # return [物攻,法强,护甲,法抗,破甲,法穿,物理吸血,法术吸血,回血]
        await 查看装备1.send(f'{qqid}当前装备：{arms}')
        await 查看装备1.send(
            f'{qqid}\r物攻：{属性[0]}\r法强：{属性[1]}\r护甲：{属性[2]}\r法抗：{属性[3]}\r破甲：{属性[4] * 100}%\r法穿：{属性[5] * 100}%\r物理吸血：{属性[6] * 100}%\r法术吸血：{属性[7] * 100}%\r回血：{属性[8]}')

@当前游戏群1.handle()
async def _(bot:Bot ,event: GroupMessageEvent):
    qqid = event.user_id
    desk = 取游戏房间(qqid)
    group = 取游戏群列表(desk, str(event.group_id))
    await 当前游戏群1.send(f'当前游戏群：{group}')

@群人数1.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    群人数 = (await bot.get_group_info(group_id=event.group_id))["member_count"]
    await 当前游戏群1.send(f'当前群人数：{群人数}')

@战场1.handle()
async def _(bot:Bot ,event: GroupMessageEvent):
    qqid = event.user_id
    desk = 取游戏房间(qqid)
    field = 战场(qqid,desk)
    await 战场1.send(field)

@开始游戏1.handle()
async def start(bot:Bot ,event: GroupMessageEvent, state: T_State, msg: Message = CommandArg(), num: List[float] = Numbers()):
    qqid = str(event.user_id)
    if len(取当前匹配队列()) < 8 and qqid != '3142331296':
        await 开始游戏1.send('少于8人无法开，发送“加入”即可加入队列')
    else:
        message1 = 开始游戏()
        desk = 取最新房间() - 1
        for group in 取游戏群列表(desk, event.group_id):
            await bot.send_group_msg(group_id=group, message=message1)
        开始选英雄计时(desk)

@行动1.handle()
async def act_handler(event: GroupMessageEvent, state: T_State):
    qqid = str(event.user_id)
    desk = 取游戏房间(qqid)
    turnplayer = 查看当前轮玩家(desk)
    if 查玩家状态(qqid) != 'act' and qqid != '3142331296':
        await 行动1.send(f'当前不该你行动，当前该{turnplayer}行动，发送【战场】查看战况')
    else:
        em = str(event.message)
        if em == '主动技' or em == '主动' or em == '主动技能' or em == '小技能':
            cate = 改技能类别(turnplayer,1)
            await 行动1.send(f'请选择主动技目标：{可用目标(turnplayer,cate)}')
        elif em == '限定技' or em == '限定' or em == '限定技能' or em == '大招':
            cate = 改技能类别(turnplayer,2)
            await 行动1.send(f'请选择限定技目标：{可用目标(turnplayer,cate)}')

@行动1.got('text')
async def act_handler(bot:Bot, event: GroupMessageEvent, state: T_State):
    qqid = event.user_id
    desk = 取游戏房间(qqid)
    qqid = 查看当前轮玩家(desk)
    #qqid = event.user_id
    groupid = event.group_id
    if 查玩家状态(qqid) == 'act' or str(event.user_id) == '3142331296':
        cate = 查技能类别(qqid)
        目标集 = 可用目标(qqid,cate)
        if len(目标集) < 1:
            await 行动1.send(f'无可用目标，已为您跳过回合')
            message1 = '该玩家跳过回合'
        elif int(str(state["text"])) not in 目标集 and 查技能类别(qqid) == 1:
            tar = random.choice(目标集)
            await 行动1.send(f'目标无效，已为你随机选择目标：{tar}')
            message1 = 主动技能(qqid, tar)
        elif int(str(state["text"])) not in 目标集 and 查技能类别(qqid) == 2:
            tar = random.choice(目标集)
            await 行动1.send(f'目标无效，已为你随机选择目标：{tar}')
            message1 = 限定技能(qqid, tar)
        elif 查技能类别(qqid) == 1:
            tar = state["text"]
            await 行动1.send(f'已选择目标：{tar}')
            message1 = 主动技能(qqid, tar)
        elif 查技能类别(qqid) == 2:
            tar = state["text"]
            await 行动1.send(f'已选择目标：{tar}')
            message1 = 限定技能(qqid, tar)

        message2 = 台词(qqid)  # 这是英雄台词

        if 进入选装备(desk):

            messageA = 开始选装备(desk)

            for group in 取游戏群列表(desk, groupid):
                if (await bot.get_group_info(group_id=group))["member_count"] != 0:
                    await bot.send_group_msg(group_id=group, message='所有人可在本轮领取一件装备！直接发装备名即可。没想好可以等会再选，本轮任何时候都可选')
                    await bot.send_group_msg(group_id=group, message=messageA)

        messagelist = 下一位(desk)
        if len(messagelist) == 3:
            message3 = messagelist[0]  # 这是判定语或游戏结束语
            message4 = messagelist[1]  # 这是开始语
            picture = messagelist[2]  # 这是图
        else:
            message3 = '无'  # 这是判定语或游戏结束语
            message4 = '游戏结束，感谢各位参与！如有bug请反馈至3142331296，会第一时间修复'
        for group in 取游戏群列表(desk, groupid):
            if (await bot.get_group_info(group_id=group))["member_count"] != 0:
                await bot.send_group_msg(group_id=group, message=message1)
                await bot.send_group_msg(group_id=group, message=message2)
                await bot.send_group_msg(group_id=group, message=picture)
                if message3 != '无':
                    await bot.send_group_msg(group_id=group, message=message3)
                await bot.send_group_msg(group_id=group, message=message4)

@跳过1.handle()
async def act(bot:Bot, event: GroupMessageEvent, state: T_State):
    qqid = event.user_id
    desk = 取游戏房间(qqid)
    qqid = 查看当前轮玩家(desk)
    #qqid = event.user_id
    groupid = event.group_id
    if 查玩家状态(qqid) == 'act' or str(event.user_id) == '3142331296' or 查行动时间(qqid) > 60:
        message1 = '该玩家跳过回合'
        message2 = 台词(qqid)  # 这是英雄台词

        if 进入选装备(desk):

            messageA = 开始选装备(desk)

            for group in 取游戏群列表(desk, groupid):
                if (await bot.get_group_info(group_id=group))["member_count"] != 0:
                    await bot.send_group_msg(group_id=group, message='所有人领一件装备！直接发装备名即可。没想好可以等会再选，本轮任何时候都可选')
                    await bot.send_group_msg(group_id=group, message=messageA)

        messagelist = 下一位(desk)
        message3 = messagelist[0]  # 这是判定语或游戏结束语
        picture = messagelist[2]  # 这是图
        if isinstance(messagelist[0], str):  #如果m3是字符串
            message4 = messagelist[1]  # 这是开始语
        else:
            message4 = '游戏结束，感谢各位参与，若发现bug请反馈至3142331296，会第一时间修复'
        grouplist = 取游戏群列表(desk, groupid)
        for group in grouplist:
            if (await bot.get_group_info(group_id=group))["member_count"] != 0:
                await bot.send_group_msg(group_id=group, message=message1)
                await bot.send_group_msg(group_id=group, message=message2)
                await bot.send_group_msg(group_id=group, message=picture)
                if message3 != '无':
                    await bot.send_group_msg(group_id=group, message=message3)
                await bot.send_group_msg(group_id=group, message=message4)

@查玩家1.handle()
async def couplets_handler(bot: Bot, event: GroupMessageEvent, state: T_State):
    qqid = event.user_id
    desk =  取游戏房间(qqid)
    turn = str(event.message).split()[1]
    qqqq = 查看指定轮玩家(desk,int(turn))
    await 查玩家1.send(f'该玩家：{qqqq}')

@存活玩家1.handle()
async def _(event: GroupMessageEvent):
    qqid = str(event.user_id)
    desk = 取游戏房间(qqid)
    mes = 取存活玩家列表(desk)
    await 存活玩家1.send(f'存活玩家：{mes}')

@玩家名单1.handle()
async def _(event: GroupMessageEvent):
    num = int(str(event.message).split(maxsplit=1)[1])  #返回空格之后的内容
    await 玩家名单1.send(取玩家名单(num))

@加入1.handle()
async def _(bot:Bot,event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取qq号
    if len(查卡包(qq_id)) < 1:
        await 加入1.send('你还没有英雄，请先【抽卡】')
    elif len(取当前匹配队列()) >= 8:  #开始游戏
        await 加入1.send('当前队列已满人，请稍候加入！')
        message1 = 开始游戏()
        desk = 取最新房间() - 1
        for group in 取游戏群列表(desk, event.group_id):
            await bot.send_group_msg(group_id=group, message=message1)
        开始选英雄计时(desk)
    else:
        group_id = str(event.group_id)  # 获取群号
        message1 = 加入匹配队列(qq_id,group_id)
        waitlist = 取等候群列表()
        for group in waitlist:
            await bot.send_group_msg(group_id=group, message=message1)

@选装备1.handle()
async def _(bot:Bot ,event: GroupMessageEvent):
    # 图 = 取装备图(event.message)
    # await 选装备1.send()
    qqid = str(event.user_id)
    desk = 取游戏房间(qqid)
    state = 查玩家状态(qqid)
    if state != 'vivi' and state != 'act' and state != 'pre' and qqid != '3142331296':
        await 选装备1.send('你不在游戏中，发送“加入”即可参加游戏')  #没玩
    if 查看玩家选装状态(qqid) == 1 and qqid != '3142331296':
        await 选装备1.send('你已经选过装备了，请等待下一轮选装')  #没玩
    else:
        选择装备 = str(event.message)
        if not 选择装备 in 取装备库(desk):
            await 选装备1.send(f'目前可选装备：{取装备库(desk)}')
        else:
            设置玩家选装状态(qqid,1)
            await 选装备1.send(f'你已领取：{选装备(qqid,选择装备)}，可以发送“我的装备”进行查看')
            改玩家状态(qqid,'vivi')
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

            玩家装备 = 查玩家装备(qqid)

            for arms in 玩家装备:  #遍历所有装备类型

                临时装备 = arms   #某一装备类型的全部装备
                高级装备 = []
                for 单个装备 in 临时装备:
                    if 单个装备 in 物理2星.values() or 单个装备 in 法术2星.values() or 单个装备 in 防御2星.values() or 单个装备 in 物理3星 or 单个装备 in 法术3星 or 单个装备 in 防御3星:
                        高级装备.append(单个装备)
                for 单个装备 in 高级装备:
                    临时装备.remove(单个装备)

                if len(临时装备) == 2 and 临时装备[0] != 临时装备[1]:  #两件不同1星装备
                    new = 合成2星(临时装备[0],临时装备[1],qqid)
                    await 选装备1.send(f'{临时装备[0]}+{临时装备[1]}={new}')
                elif len(临时装备) == 3:
                    new = 合成3星(临时装备[0],临时装备[1],临时装备[2],qqid)
                    await 选装备1.send(f'{临时装备[0]}+{临时装备[1]}+{临时装备[2]}={new}')

@查卡1.handle()
async def _(bot:Bot ,event: GroupMessageEvent):
    图 = 取卡图(event.message)
    await 查卡1.send(图)
    qqid = event.user_id
    if 查玩家状态(qqid) != 'pre':
        await 查卡1.send('发送“功能”查看更多功能')  #没玩
    else:
        hero = str(event.message)
        if not hero in 查卡包(qqid):
            await 查卡1.send('你没有这张卡牌，发送‘卡包’查看你有的卡牌')
        else:
            await 查卡1.send(f'你已选择：{选玩家英雄(qqid, hero)}')
        desk = 取游戏房间(qqid)
        if 结束选英雄(desk):
            field = 战场('3142331296',desk)
            message2 = 开始选装备(desk)
            for group in 取游戏群列表(desk,event.group_id):
                await bot.send_group_msg(group_id=group, message=field)
                await bot.send_group_msg(group_id=group, message='所有人领一件装备！直接发装备名即可。没想好可以等会再选，本轮任何时候都可以选')
                await bot.send_group_msg(group_id=group, message=message2)

            field = 战场('3142331296', desk)
            message2 = 开始对战(desk)
            for group in 取游戏群列表(desk, str(event.group_id)):
                await bot.send_group_msg(group_id=group, message=field)
                await bot.send_group_msg(group_id=group, message='对战开始！发【战场】查看战况，发【我的装备】查看自己装备。每个人行动时间1分钟，如果别人太久没行动，你可以发【跳过】帮ta跳过')
                await bot.send_group_msg(group_id=group, message=message2)

@开始对战1.handle()
async def _(event: GroupMessageEvent):
    qqid = event.user_id
    desk = 取游戏房间(qqid)
    message2 = 开始对战(desk)
    await 开始对战1.send(message2)

@开始选装1.handle()
async def start(event: GroupMessageEvent):
    qqid = event.user_id
    desk = 取游戏房间(qqid)
    message2 = 开始选装备(desk)
    await 开始选装1.send('所有人领一件装备！直接发装备名即可。没想好可以等会再选，本轮任何时候都可选')
    await 开始选装1.send(message2)

@抽卡1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取qq号
    当前金币 = 查金币(qq_id)
    if str(event.message) == '抽卡' or str(event.message) == '抽英雄' or str(event.message) == '获得卡牌' or str(event.message) == '获得英雄':
        num = 1
    else:
        num = int(str(event.message).split(maxsplit=1)[1])  #返回空格之后的内容
    需要金币 = int(num) * 10
    if 当前金币 < 需要金币:
        await 抽卡1.send(f"每张卡10金币，发送“签到”或“群里淘金”获得金币")
    else:
        减金币(qq_id,需要金币)
        card = 抽卡(qq_id,num)
        await 抽卡1.send(f"获得：{card}")

@查卡包1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取qq号
    if str(event.message) == '查卡包' or str(event.message) == '我的英雄' or str(event.message) == '我的卡包' or str(event.message) == '卡包':
        card = 查卡包(qq_id)
        await 查卡包1.send(f"你的卡包：{card}")
    else:
        qq_id = int(str(event.message).split(maxsplit=1)[1])  #返回空格之后的内容
        card = 查卡包(qq_id)
        await 查卡包1.send(f"你的卡包：{card}")