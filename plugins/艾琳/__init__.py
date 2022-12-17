from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11 import GROUP_ADMIN, GROUP_OWNER
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment   #发图片用的

from plugins.fun import *
from plugins.农场.farm import *

import random,json,os,re,requests,jieba
import datetime,time

#测试
测试超管1 = on_command("测试超管", permission=SUPERUSER)
测试1 = on_command("测试", permission=SUPERUSER)
测试权限1 = on_command("测试权限")
时间1 = on_command("时间",aliases={"当前时间"})
加金币1 = on_command("加金币", permission=SUPERUSER)
减金币1 = on_command("减金币", permission=SUPERUSER)
改称号1 = on_command("改称号", permission=SUPERUSER)
发称号1 = on_command("发称号", permission=SUPERUSER)
随机群1 = on_command("随机群", permission=SUPERUSER)
语音1 = on_command("语音", permission=SUPERUSER)
jieba1 = on_command("jieba",aliases={"结巴","拆分","拆词"}, permission=SUPERUSER)
全排名1 = on_command("全排名",aliases={"全部排名","全部排行榜","全部排行"}, permission=SUPERUSER)

#目录
菜单1 = on_command("菜单",aliases={"功能", "帮助" ,"主菜单" ,"目录" , "@艾琳"})
开发人员1 = on_command("开发人员",aliases={"关于", "开发者"})

#常用功能
签到1 = on_command("签到",aliases={"打卡", "冒泡", "早", "中午", "午", "晚","获得金币"})
金币1 = on_command("金币",aliases={"查看金币","金币查询","查看背包","我的金币"})
喊话1 = on_command("大喇叭",aliases={"喊话"})
金币排名1 = on_command("金币排名",aliases={"排名","排行榜","金币排行"})

#api
战力1 = on_command("战力",aliases={"查战力", "查战区" , "战区","查看战力","查看战区"})
查皮肤1 = on_command("查皮肤",aliases={"查看皮肤", "皮肤"})
查出装1 = on_command("查出装",aliases={"查看出装", "出装"})
百科1 = on_command("百科",aliases={"查百科"})
天气1 = on_command("天气",aliases={"查天气"})
一言1 = on_command("一言",aliases={"随机一言"})
猜英雄1 = on_command("猜英雄")

#插件相关
点歌台1 = on_command("点歌台")
AI对联1 = on_command("AI对联",aliases={"ai对联"})
漂流瓶1 = on_command("漂流瓶")

'''api类'''

@猜英雄1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.user_id)
    当前金币 = 查金币(qq_id)
    if 当前金币 < 1:
        await 猜英雄1.send("需花费1金币，发送“签到”或“采矿”获得金币")
    else:
        减金币(qq_id,1)
        group_id = event.group_id   # 获取群号
        if str(event.message) == '猜英雄':
            结果 = requests.get(f'https://xiaoapi.cn/API/game_cyx.php?id={group_id}&msg=开始游戏')
            await 猜英雄1.send('发“猜英雄 英雄名”进行回答')
        else:
            值 = str(event.message).split(maxsplit=1)[1]  #返回空格之后的内容
            结果 = requests.get(f'https://xiaoapi.cn/API/game_cyx.php?id={group_id}&msg=答{值}')
        结果 = bytes(结果.content)
        结果 = 结果.decode('utf-8')
        结果 = str(结果).split('。')  #返回空格之后的内容
        for guess in range (0,10):
            消息 = 结果[guess]
            await 猜英雄1.send(消息)
        await 猜英雄1.send(消息)

@查皮肤1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取qq号
    当前金币 = 查金币(qq_id)
    if 当前金币 < 1:
        await 查皮肤1.send("查询需花费1金币，发送“签到”或“采矿”获得金币")
    elif str(event.message) == '查皮肤' or str(event.message) == '皮肤':
        await 查皮肤1.send("发送“查皮肤 英雄名”进行查询，注意空一格")
    else:
        减金币(qq_id,1)
        值 = str(event.message).split(maxsplit=1)[1]  #返回空格之后的内容
        英雄号 = 取英雄号(值)
        for 皮肤号 in range(1,10):
            #图 = f'https://game.gtimg.cn/images/yxzj/img201606/heroimg/{英雄号}/{英雄号}-mobileskin-{皮肤号}.jpg'
            #图 = f'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info{英雄号}/{英雄号}-mobileskin-{皮肤号}.jpg'
            #图 = f'http://game.gtimg.cn/images/yxzj/img201606/heroimg/{英雄号}/{英雄号}-bigskin-{皮肤号}.jpg'
            图 = f'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{英雄号}/{英雄号}-bigskin-{皮肤号}.jpg'
            await 查皮肤1.send(MessageSegment.image(图))

@查出装1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取qq号
    当前金币 = 查金币(qq_id)
    if 当前金币 < 3:
        await 查皮肤1.send("查询需花费3金币，发送“签到”或“采矿”获得金币")
    elif str(event.message) == '查出装' or str(event.message) == '出装':
        await 查皮肤1.send("发送“查出装 英雄名”进行查询，注意空一格")
    else:
        减金币(qq_id,3)
        值 = str(event.message).split(maxsplit=1)[1]  #返回空格之后的内容
        图 = f'http://xiaoapi.cn/API/wzry_pic.php?msg={值}'
        await 查出装1.send(MessageSegment.image(图))

@战力1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取qq号
    当前金币 = 查金币(qq_id)
    if 当前金币 < 5:
        await 战力1.send("查询需花费5金币，发送“签到”或“采矿”获得金币")
    elif str(event.message) == '战力' or str(event.message) == '查战力':
        await 查皮肤1.send("发送“战力 英雄名”进行查询，注意空一格")
    else:
        减金币(qq_id,5)
        值 = str(event.message).split(maxsplit=1)[1]  #返回空格之后的内容
        平台词典 = {'aqq':'安卓QQ','awx':'安卓微信','iqq':'iosQQ','iwx':'ios微信'}
        for 平台 in ['aqq','awx','iqq','iwx']:
            结果 = requests.get(f'https://www.sapi.run/hero/select.php?hero={值}&type={平台}')
            结果 = json.loads(结果.content)
            结果 = 结果['data']
            区 = 结果['area']
            市 = 结果['city']
            省 = 结果['province']
            区战力 = 结果['areaPower']
            市战力 = 结果['cityPower']
            省战力 = 结果['provincePower']
            #小国标 = 结果['guobiao']
            更新时间 = 结果['updatetime']
            平台名 = 平台词典[平台]
            await 战力1.send(f"{平台名}\r区标：{区}（战力{区战力}）\r市标：{市}（战力{市战力}）\r省标：{省}（战力{省战力}）\r时间：{更新时间}")

@百科1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取qq号
    当前金币 = 查金币(qq_id)
    if 当前金币 < 10:
        await 战力1.send("查询需花费10金币，发送“签到”或“采矿”获得金币")
    elif str(event.message) == '天气' or str(event.message) == '查天气':
        await 查皮肤1.send("发送“天气 城市名”进行查询，注意空一格")
    else:
        减金币(qq_id,10)
        值 = str(event.message).split(maxsplit=1)[1]  #返回空格之后的内容
        结果 = requests.get(f'https://xiaoapi.cn/API/bk.php?m=json&type=bd&msg={值}')
        结果 = json.loads(结果.content)
        内容 = 结果['msg']
        内容 = str(内容).split('。',maxsplit=4)  #返回空格之后的内容
        for 号 in range (0,4):
            await 百科1.send(内容[号])

@天气1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取qq号
    当前金币 = 查金币(qq_id)
    if 当前金币 < 2:
        await 战力1.send("查询需花费2金币，发送“签到”或“采矿”获得金币")
    elif str(event.message) == '天气' or str(event.message) == '查天气':
        await 查皮肤1.send("发送“天气 城市名”进行查询，注意空一格")
    else:
        减金币(qq_id,2)
        值 = str(event.message).split(maxsplit=1)[1]  #返回空格之后的内容
        结果 = requests.get(f'https://xiaoapi.cn/API/zs_tq.php?type=zgtq&msg={值}&num=20&n=1')
        结果 = json.loads(结果.content)
        地点 = 结果['name']
        天气情况 = 结果['data']
        空气情况 = 结果['shzs']
        await 天气1.send(f"【{地点}】\r天气：{天气情况}")
        await 天气1.send(f"【{地点}】\r{空气情况}")

@一言1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取qq号
    当前金币 = 查金币(qq_id)
    if 当前金币 < 1:
        await 战力1.send("一言需花费1金币，发送“签到”或“采矿”获得金币")
    else:
        减金币(qq_id,1)
        结果 = requests.get('https://xiaoapi.cn/API/yiyan.php')
        结果 = (结果.content).decode('utf-8')
        await 一言1.send(结果)

'''常规'''

@菜单1.handle()
async def _():
    await 菜单1.send(MessageSegment.image(r'file:///C:\\Users\\86156\\Desktop\\py\\ailin\\resource\\menu.png'))

@语音1.handle()
async def _():
    await 语音1.send(MessageSegment.record(r'file:///C:\\Users\\86156\\Desktop\\py\\ailin\\resource\\ldjh.mp3'))

@喊话1.handle()
async def _(bot:Bot):
    群列表 = await bot.get_group_list()
    随机100群 = random.choices(群列表,k=1)
    for group in 随机100群:
        groupid = group['group_id']
        新群(str(groupid))
        await bot.send_group_msg(groupid=groupid, message=f'测试{groupid}，发信人：3142331296')
        await 喊话1.send(f'已喊话{groupid}')

@jieba1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取签到人qq号
    当前金币 = 查金币(qq_id)
    if 当前金币 < 1:
        await jieba1.send("需要花费1金币，发“签到”或“采矿”获得金币")
    else:
        减金币(qq_id,1)
        text = str(event.message).split(maxsplit=1)[1]  #返回空格之后的内容
        cut = jieba.lcut(text)
        mes = ''
        for words in cut:
            mes = mes + ',' + words
        await jieba1.send(mes)

@签到1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取签到人qq号
    当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    查金币(qq_id)
    判定利息()
    with open(f'data/艾琳/用户/{qq_id}.json', 'r+', encoding='utf-8')as f:  #获取签到人信息
        dic = json.load(f)
        签到日期 = dic['checkdate']
    if 签到日期 == 当前日期 and qq_id != '3142331296':
        return()
    with open(f'data/艾琳/用户/{qq_id}.json', 'r+', encoding='utf-8')as f:  # 获取签到人信息
        dic = json.load(f)
        dic['checkdate'] = 当前日期   #记录签到日期
        f.seek(0)  # 指向文本开头
        f.truncate()  # 清空文本
        json.dump(dic, f)  # 写入数据
    获得金币 = random.randint(100,200)
    加金币(qq_id,获得金币)
    评价 = f'+{获得金币}'

    礼品集 = 查图鉴('raws') + 查图鉴('plants')
    礼品 = random.choices(礼品集,k=2)
    加物品(qq_id,礼品[0],1)
    加物品(qq_id,礼品[1],1)

    await 签到1.send(f"获得{礼品[0]}、{礼品[1]}，发“农场”查看玩法")

    await 签到1.send(f"用户：{qq_id}\r"
               f"金币：{查金币(qq_id)}（{评价}）\r"
               f"称号：{查称号(qq_id)}"
               f"{饰品信息(qq_id)}"
               f"{服饰信息(qq_id)}"
               f"{宠物信息(qq_id)}"
               f"{chess信息(qq_id)}")

    '''债务减免'''

    file = os.listdir('data/bank/银行')
    for 银行 in file:
        银行名 = 银行.split('.json')[0]
        with open(f'data/bank/银行/{银行}', 'r+', encoding='utf-8') as f:
            dic = json.load(f)
            账户 = dic['account']
            贷款限额 = dic['loan']
            qqidb = qq_id + 'b'
            if qqidb in 账户.keys():
                负债 = - 账户[qqidb][0]
            else:
                负债 = 0
            if 负债 > 0 and 负债 > 2 * 贷款限额:
                应还 = 负债 * 1.5
                减金币(qq_id, 应还)
                账户[qqidb][0] = 0
                await 签到1.send(f"你在{银行名}的债务已减免")
            dic['account'] = 账户
            f.seek(0)  # 指向文本开头
            f.truncate()  # 清空文本
            json.dump(dic, f)  # 写入数据

@金币1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取签到人qq号
    if str(event.message) == '金币' or str(event.message) == '金币查询' or str(event.message) == '查金币' or str(event.message) == '查询':
        await 金币1.send(f"用户：{qq_id}\r金币：{查金币(qq_id)}\r称号：{查称号(qq_id)}")
    else:
        qq_id = str(event.message).split(maxsplit=1)[1]  #返回空格之后的内容
        if 查金币(qq_id) == 0:
            await 金币1.send("此人还没有金币，发送“签到”或“挖矿”获得金币")
        else:
            await 金币1.send(f"用户：{qq_id}\r"
                           f"金币：{查金币(qq_id)}\r"
                           f"称号：{查称号(qq_id)}"
                            f"{宠物信息(qq_id)}"
                           f"{chess信息(qq_id)}")

'''插件相关'''

@点歌台1.handle()
async def _():
    await 点歌台1.send("点歌/qq点歌/网易点歌/酷我点歌/酷狗点歌/咪咕点歌/b站点歌 + 关键词")

@AI对联1.handle()
async def _():
    await AI对联1.send("对联 + 想说的内容 ， 或 对联 + 内容 + 数字 ，可生成多条对联")

@漂流瓶1.handle()
async def _():
    await 漂流瓶1.send("扔漂流瓶 + 想说的内容，还可发送：捡漂流瓶/举报漂流瓶/评论漂流瓶/查看漂流瓶")

'''测试类'''

@随机群1.handle()
async def _(event: GroupMessageEvent):
    await 发称号1.send(随机群())

@发称号1.handle()
async def _(event: GroupMessageEvent):
    发称号()
    await 发称号1.send("完毕")

@加金币1.handle()
async def _(event: GroupMessageEvent):
    qq_id= str(event.message).split(maxsplit=2)[1]  #返回空格之后的内容
    num = int(str(event.message).split(maxsplit=2)[2])  #返回空格之后的内容
    加金币(qq_id,num)
    await 加金币1.send(f"加金币完成，此人当前金币：{查金币(qq_id)}")

@减金币1.handle()
async def _(event: GroupMessageEvent):
    qq_id= str(event.message).split(maxsplit=2)[1]  #返回空格之后的内容
    num = int(str(event.message).split(maxsplit=2)[2])  #返回空格之后的内容
    减金币(qq_id,num)
    await 减金币1.send(f"减金币完成，此人当前金币：{查金币(qq_id)}")

@改称号1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.message).split(maxsplit=2)[1]  #返回空格之后的内容
    num = int(str(event.message).split(maxsplit=2)[2])  #返回空格之后的内容
    改称号(qq_id,num)
    await 改称号1.send(f"改称号完成，此人当前称号：{查称号(qq_id)}")

@测试1.handle()
async def _(event: GroupMessageEvent):
    # text = event.message  #返回消息全文
    # text = str(event.message).split(maxsplit=1)[1]  #返回空格之后的内容
    # 群人数 = (await bot.get_group_info(group_id=event.group_id))["member_count"]#返回群人数
    await 测试1.send(f"结果：{event.message}")

@测试超管1.handle()
async def _():
    await 测试超管1.send("超管命令测试成功")

@测试权限1.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if await GROUP_ADMIN(bot, event):
        await 测试权限1.send("管理员测试成功")
    elif await GROUP_OWNER(bot, event):
        await 测试权限1.send("群主测试成功")
    else:
        await 测试权限1.send("群员测试成功")

@时间1.handle()
async def _():
    当前时间 = str(datetime.datetime.now())
    await 时间1.send(f"当前时间：{当前时间}")

@金币排名1.handle()
async def _(event: GroupMessageEvent):
    改金币('3142331296',100)
    发称号()
    rank1 = rank123()
    await 金币排名1.send(str(rank1))
    await 金币排名1.send(查上榜金币())

@全排名1.handle()
async def _(event: GroupMessageEvent):
    qs =  str(event.message).split(maxsplit=2)[1]  #返回空格之后的内容
    zz =  str(event.message).split(maxsplit=2)[2]  #返回空格之后的内容
    rank1 = rank101(int(qs),int(zz))
    await 全排名1.send(str(rank1))
    await 全排名1.send(查上榜金币())

@开发人员1.handle()
async def _():
    await 开发人员1.send("机器人名称：艾琳\r"
                    "开发者：3142331296\r"
                     "开发语言：Python\r"
                     "开发框架：Nonebot2/go-cqhttp\r")
    await 开发人员1.send("开源证书：AGPL-3.0\r" 
                    "源码：github.com/mittr0c/ailin")