from nonebot.adapters.onebot.v11 import MessageSegment   #发图片用的
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot import on_command
from nonebot.permission import SUPERUSER

import time,re

from plugins.fun import *
from plugins.农场.farm import *
from plugins.银行.bank import *

银行1 = on_command("天地银行",aliases={"靓仔银行","茗念宝贝","丝绸之路","于塗银行","云茵飞酱"})
银行列表1 = on_command("银行",aliases={"银行列表"})
存钱1 = on_command("存金币",aliases={"取金币","借金币","还金币"})

我的银行1 = on_command("我的银行")
设置1 = on_command("设置存金币利息",aliases={"设置借金币利息","设置借金币限额"})

注册银行1 = on_command("注册银行", permission=SUPERUSER)
发利息1 = on_command("发利息", permission=SUPERUSER)

@发利息1.handle()
async def _(event: GroupMessageEvent):
    判定利息()
    await 存钱1.send('完毕')

@银行列表1.handle()
async def _(event: GroupMessageEvent):
    银行大全 = 银行列表()
    银行 = str()
    for 单个银行 in 银行大全:
        银行 += '\r' + 单个银行
    await 存钱1.send(f'所有银行：'
                   f'{银行}')
    await 存钱1.send('指令：\r'
                   '存金币 50\r'
                   '取金币 50\r'
                   '借金币 50\r'
                   '还金币 50')

@存钱1.handle()
async def _(event: GroupMessageEvent):
    msg = str(event.message)
    qqid = str(event.user_id)
    数额 = int(msg.split()[1])
    指令 = msg.split()[0]
    准备(qqid,数额,指令)
    银行大全 = 银行列表()
    银行 = str()
    for 单个银行 in 银行大全:
        银行 += '\r' + 单个银行
    await 存钱1.send(f'请选择银行：'
                   f'{银行}\r'
                   f'取消')

@存钱1.got('text')
async def act_handler(event: GroupMessageEvent, state: T_State):
    qqid = str(event.user_id)
    bank = str(state["text"])
    数额 = 查准备(qqid)[0]
    指令 = 查准备(qqid)[1]
    拥有金币 = 查金币(qqid)
    存款 = 查存款(bank,qqid)
    贷款 = 查贷款(bank,qqid)
    限额 = 查银行数据(bank,'loan')
    董事长 = 查银行数据(bank,'chairman')
    资金 = 查银行资金(bank) + 查金币(董事长)
    if bank == '取消':
        await 存钱1.send('已取消')
    elif bank not in 银行列表():
        await 存钱1.send(f'没有此银行')
    elif 数额 < 0:
        await 存钱1.send('不能为负数')
    else:
        if 指令 == 'c':
            if 数额 > 拥有金币:
                await 存钱1.send(f'你只有{拥有金币}金币')
                return()
            存金币(qqid,数额,bank)
            await 存钱1.send('存金币成功')
        elif 指令 == 'q':
            if 数额 > 存款 and qqid != 董事长:
                await 存钱1.send(f'你只在该银行存了{存款}金币')
                return()
            取金币(qqid,数额,bank)
            await 存钱1.send('取金币成功')
        elif 指令 == 'j':
            总数额 = 数额 + 贷款
            if 总数额 > 限额 and qqid != 董事长:
                await 存钱1.send(f'该银行最多出借每人{限额}金币！发送“银行”查询其他银行试试')
                return()
            elif 查土地数量(qqid) < 10 or len(查建筑(qqid)) < 1:
                await 存钱1.send(f'你需要有至少10个土地、1个建筑，才可以借金币。发送“商店”购买')
                return()
            elif 数额 > 资金:
                await 存钱1.send(f'该银行只剩{资金}资金了！发送“银行”查询其他银行试试')
                return()
            借金币(qqid,数额,bank)
            await 存钱1.send('借金币成功')
        elif 指令 == 'h':
            if 数额 > 贷款:
                await 存钱1.send(f'你只需要还{贷款}金币')
                return()
            还金币(qqid,数额,bank)
            await 存钱1.send('还金币成功')

@注册银行1.handle()
async def _(event: GroupMessageEvent):
    msg = str(event.message)
    qqid = msg.split()[1]
    bank = msg.split()[2]
    注册银行(qqid, bank)
    await 注册银行1.send('注册完成')

@银行1.handle()
async def _(event: GroupMessageEvent):
    qqid = str(event.user_id)
    msg = str(event.message)
    bank = msg
    董事长 = 查银行数据(bank,'chairman')
    总资金 = 查银行资金(bank) + 查金币(董事长)
    利息 = 查银行数据(bank,'interest')
    贷款利息 = 查银行数据(bank,'loan_interest')
    贷款上限 = 查银行数据(bank,'loan')
    开户人数 = 查开户人数(bank)
    存款 = 查存款(bank,qqid)
    贷款 = 查贷款(bank,qqid)
    await 银行1.send(f'银行：{bank}\r'
                   f'董事长：{董事长}\r'
                   f'总资金：{总资金}金币\r'
                   f'存金币利息：{利息}%/h\r'
                   f'借金币利息：{贷款利息}%/h\r'
                   f'借金币限额：{贷款上限}金币\r'
                   f'开户人数：{开户人数}\r'
                   f'你存了：{存款}金币\r'
                   f'你借了：{贷款}金币')

@我的银行1.handle()
async def _(event: GroupMessageEvent):
    qqid = str(event.user_id)
    bank = 查银行名(qqid)
    董事长 = 查银行数据(bank,'chairman')
    总资金 = 查银行资金(bank) + 查金币(qqid)
    利息 = 查银行数据(bank,'interest')
    贷款利息 = 查银行数据(bank,'loan_interest')
    贷款上限 = 查银行数据(bank,'loan')
    开户人数 = 查开户人数(bank)
    await 我的银行1.send(f'银行：{bank}\r'
                     f'董事长：{董事长}\r'
                   f'银行资金：{总资金}金币\r'
                   f'存金币利息：{利息}%/h\r'
                   f'借金币利息：{贷款利息}%/h\r'
                   f'借金币限额：{贷款上限}金币\r'
                   f'开户人数：{开户人数}')
    await 我的银行1.send('指令：\r'
                     '设置存金币利息 数值\r'
                     '设置借金币利息 数值\r'
                     '设置借金币限额 数值\r\r'
                     '例如：\r'
                     '设置存金币利息 3.2\r'
                     '—存金币每小时3.2%利息')
    await 我的银行1.send('对于自己银行，董事长无需存金币，可以随意取金币。注意不要让你的银行破产，否则银行会被回收或被其他用户接管')

@设置1.handle()
async def _(event: GroupMessageEvent):
    qqid = str(event.user_id)
    bank = 查银行名(qqid)
    董事长 = 查银行数据(bank,'chairman')
    总资金 = 查银行资金(bank) + 查金币(qqid)
    利息 = 查银行数据(bank,'interest')
    贷款利息 = 查银行数据(bank,'loan_interest')
    贷款上限 = 查银行数据(bank,'loan')
    开户人数 = 查开户人数(bank)

    msg = str(event.message)
    指令 = msg.split()[0]
    指令 = 指令.split('设置')[1]
    value1 = msg.split()[1]
    value1 = float(value1)
    if value1 < 0:
        await 设置1.send(f'不能是负数')
        return ()
    if 指令 == '存金币利息' or 指令 == '借金币利息' or 指令 == '借金币限额':
        if 指令 == '存金币利息':
            key1 = 'interest'
        elif 指令 == '借金币利息':
            key1 = 'loan_interest'
        elif 指令 == '借金币限额':
            key1 = 'loan'
            value1 = int(value1)
        设置银行数据(bank, key1, value1)
        await 设置1.send('设置完成，发送“我的银行”查询')