from nonebot.adapters.onebot.v11 import MessageSegment   #发图片用的
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot import on_command
from nonebot.permission import SUPERUSER

import time,re

from plugins.fun import *
from plugins.农场.farm import *
from plugins.银行.bank import *

银行1 = on_command("天地银行",aliases={"茗念宝贝","丝绸之路","云茵飞酱","渊郭银行","新丝绸之路","注资银行","宝宝巴士","玛卡银行","美联储","于塗银行","小郭郭银行","抽奖贷","款某银行","利息银行","帅男银行","真·玛卡银行","匿名很行"})
银行列表1 = on_command("银行",aliases={"银行列表"})
存钱1 = on_command("存金币",aliases={"取金币","借金币","还金币"})

我的银行1 = on_command("我的银行")
开银行1 = on_command("开银行")
设置1 = on_command("设置存金币利息",aliases={"设置借金币利息","设置借金币限额"})
查账户2 = on_command("查账户")

注册银行1 = on_command("注册银行", permission=SUPERUSER)
发利息1 = on_command("发利息", permission=SUPERUSER)
查账户1 = on_command("账户", permission=SUPERUSER)
债务减免1 = on_command("债务减免", permission=SUPERUSER)

@债务减免1.handle()
async def _(event: GroupMessageEvent):
    file = os.listdir('data/bank/银行')
    for 银行 in file:
        银行名 = 银行.split('.json')[0]
        with open(f'data/bank/银行/{银行}', 'r+', encoding='utf-8') as f:
            dic = json.load(f)
            账户 = dic['account']
            贷款限额 = dic['loan']
            for qqidb in list(账户.keys()):
                qq_id = qqidb.split('b')[0]
                if qqidb in 账户.keys():
                    负债 = - 账户[qqidb][0]
                else:
                    负债 = 0
                if 负债 > 0 and 负债 > 2 * 贷款限额:
                    应还 = 负债 * 1.5
                    减金币(qq_id, 应还)
                    账户[qqidb][0] = 0
                    await 债务减免1.send(f"{qq_id}在{银行名}的债务已减免")
            dic['account'] = 账户
            f.seek(0)  # 指向文本开头
            f.truncate()  # 清空文本
            json.dump(dic, f)  # 写入数据

@开银行1.handle()
async def _(event: GroupMessageEvent):
    qqid = str(event.user_id)
    msg = str(event.message)
    if 查金币(qqid) < 100000:
        await 开银行1.send('开银行需要10万金币')
    elif msg == '开银行':
        await 开银行1.send('指令：开银行 + 空格 + 银行名字')
    elif 查银行名(qqid) != 'no':
        await 开银行1.send('你已经有银行了')
    else:
        减金币(qqid,100000)
        bank = msg.split()[1]
        注册银行(qqid, bank)
        await 开银行1.send('已花费10万金币注册银行，正在审核中，如果名字违规会被关闭\r'
                         '发送“我的银行”开始设置银行')

@发利息1.handle()
async def _(event: GroupMessageEvent):
    判定利息()
    await 存钱1.send('完毕')

@银行列表1.handle()
async def _(event: GroupMessageEvent):
    银行大全 = 银行列表()
    第一页 = str()
    第二页 = str()
    for 单个银行 in 银行大全:
        随机 = random.randint(1,2)
        if 随机 == 1:
            第一页 += '\r' + 单个银行
        else:
            第二页 += '\r' + 单个银行
    await 银行列表1.send(f'第一页：'
                   f'{第一页}')
    await 银行列表1.send(f'第二页：'
                   f'{第二页}')
    await 银行列表1.send('指令：\r'
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
    第一页 = str()
    第二页 = str()
    for 单个银行 in 银行大全:
        随机 = random.randint(1,2)
        if 随机 == 1:
            第一页 += '\r' + 单个银行
        else:
            第二页 += '\r' + 单个银行
    await 存钱1.send(f'第一页：'
                   f'{第一页}')
    await 存钱1.send(f'第二页：'
                   f'{第二页}')
    await 存钱1.send('请选择银行')


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
            if 数额 > 20000:
                await 存钱1.send('存金币成功，超过20000的部分不产生利息')
            else:
                await 存钱1.send('存金币成功')
        elif 指令 == 'q':
            if 数额 > 存款 and qqid != 董事长:
                await 存钱1.send(f'你只在该银行存了{存款}金币')
                return()
            if 数额 > 资金:
                await 存钱1.send(f'该银行只剩{资金}资金了！发送“银行”查询其他银行试试')
                return()
            取金币(qqid,数额,bank)
            await 存钱1.send('取金币成功')
        elif 指令 == 'j':
            总数额 = 数额 + 贷款
            if 总数额 > 限额 and qqid != 董事长:
                await 存钱1.send(f'该银行最多出借每人{限额}金币！发送“银行”查询其他银行试试')
                return()
            if 查土地数量(qqid) < 10 or len(查建筑(qqid)) < 1:
                await 存钱1.send(f'你需要有至少10个土地、1个建筑，才可以借金币。发送“商店”购买')
                return()
            if 数额 > 资金:
                await 存钱1.send(f'该银行只剩{资金}资金了！发送“银行”查询其他银行试试')
                return()
            借金币(qqid,数额,bank)
            await 存钱1.send('借金币成功')
        elif 指令 == 'h':
            if 数额 > 拥有金币:
                await 存钱1.send(f'你只有{拥有金币}金币')
                return()
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

@查账户2.handle()
async def _(event: GroupMessageEvent):
    qqid = str(event.user_id)
    bank = 查银行名(qqid)
    结果 = 查账户(bank)
    await 查账户2.send(f'#{结果[0]}')
    await 查账户2.send(f'#{结果[1]}')

@查账户1.handle()
async def _(event: GroupMessageEvent):
    msg = str(event.message)
    bank = msg.split()[1]
    结果 = 查账户(bank)
    await 查账户1.send(f'#{结果[0]}')
    await 查账户1.send(f'#{结果[1]}')

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
                   f'资金：{总资金}金币\r'
                   f'开户人数：{开户人数}')
    await 银行1.send(f'银行：{bank}\r'
                   f'存金币利息：{利息}%/h\r'
                   f'借金币利息：{贷款利息}%/h\r'
                   f'借金币限额：{贷款上限}金币\r'
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
                     '设置借金币限额 数值\r'
                     '查账户\r\r'
                     '例如：\r'
                     '设置存金币利息 3.2\r'
                     '—存金币每小时3.2%利息')

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
            if value1 >= 10:
                await 设置1.send('利息不能高于10%')
                return()
            key1 = 'interest'
            await 设置1.send(f'已设置每小时{value1}%金币利息')
        elif 指令 == '借金币利息':
            if value1 >= 10:
                await 设置1.send('利息不能高于10%')
                return()
            key1 = 'loan_interest'
            await 设置1.send(f'已设置每小时{value1}%金币利息')
        elif 指令 == '借金币限额':
            if value1 >= 5000:
                await 设置1.send('限额不能高于5000')
                return()
            key1 = 'loan'
            value1 = int(value1)
            await 设置1.send(f'已设置限额{value1}，借金币高于{1.5*value1}的部分将被减免')
        设置银行数据(bank, key1, value1)