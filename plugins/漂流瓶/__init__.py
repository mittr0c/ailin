import asyncio
import random
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, GROUP, Message
from .data_source import bottle,text_audit
from .config import black_group

from plugins.fun import *

throw = on_command("扔漂流瓶 ", aliases=set(["寄漂流瓶 "]),permission=GROUP, priority=100, block=True)
get = on_command("捡漂流瓶", priority=100, block=True)
report = on_command("举报漂流瓶 ", priority=100, block=True)
comment = on_command("评论漂流瓶 ", priority=100, block=True)
check_bottle = on_command("查看漂流瓶 ", priority=100, block=True)

clear = on_command("清空漂流瓶", permission=SUPERUSER, priority=100, block=True)
remove = on_command("删除漂流瓶 ",permission=SUPERUSER, priority=100, block=True)

@throw.handle()
async def thr(bot: Bot, event: GroupMessageEvent):
    qq_id = event.user_id
    if 查金币(qq_id) < 1:
        await throw.finish("扔漂流瓶需要花费1金币，发“签到”获得金币")
    else:
        减金币(qq_id,1)
        message = str(event.message).split(maxsplit=1)[1]
        message_text = str(event.message.extract_plain_text())[1] or ""
        try:
            message[1]
        except:
            await throw.finish("想说些什么话呢？在指令后边写上吧！")

        audit = text_audit(text=message_text)
        if not audit == 'pass':
            if audit == 'Error':
                await throw.finish("文字审核未通过！原因：调用审核API失败" )
            elif audit['conclusion'] == '不合规':
                await throw.finish("文字审核未通过！原因：" + audit['data'][0]['msg'])

        group_name = await bot.get_group_info(group_id=event.group_id)
        group_name = group_name['group_name']
        user_name = await bot.get_group_member_info(group_id=event.group_id,user_id=event.user_id)
        user_name = user_name['nickname']

        if bottle.add(bot=bot,user=event.user_id, group=event.group_id, text=message, user_name=user_name, group_name=group_name):
            await asyncio.sleep(2)
            await throw.finish(f'你将一个漂流瓶以时速{random.randint(0,100)}km/h的速度扔出去，谁会捡到这个瓶子呢...')
        else:
            await asyncio.sleep(2)
            await throw.finish("你的瓶子以奇怪的方式消失掉了！")

@get.handle()
async def g(bot: Bot, event: GroupMessageEvent):
    qq_id = event.user_id
    if 查金币(qq_id) < 1:
        await throw.finish("捡漂流瓶需要花费1金币，发“签到”获得金币")
    else:
        减金币(qq_id, 1)
        if not bottle.select():
            await get.finish("好像一个瓶子也没有呢..要不要扔一个？")
        else:
            bott = bottle.select()
            data = bott[1]
            try:
                user = await bot.get_group_member_info(group_id=data['group'], user_id=data['user'])
                user = user["nickname"]
            except:
                user = data['user_name']
            try:
                group = await bot.get_group_info(group_id=data['group'])
                group = group["group_name"]
            except:
                group = data['group_name']

            comment_list = bottle.check_comment(bott[0])
            comment:str = ""
            for i in comment_list[-3:]:
                comment += i+"\n"
            await get.finish(f'【漂流瓶No.{bott[0]}|被捡到{data["picked"]}次】来自【{group}】的 {user} ！\n'+Message(data['text']) + (f"\n★评论共 {len(comment_list)} 条★\n{comment.strip()}" if comment else ""))


@report.handle()
async def rep(bot: Bot, event: GroupMessageEvent):
    if event.group_id in black_group:
        await report.finish()

    index = int(str(event.message).split(maxsplit=1)[1])
    result = bottle.report(index)
    if result == 0:
        await report.finish("举报失败！请检查编号")
    if result == 1:
        await report.finish(f"举报成功！关于此漂流瓶已经有 {bottle.check_report(index)} 次举报")
    if result == 2:
        await report.finish("举报成功！已经进行删除该漂流瓶处理！")
    if result == 3:
        await report.finish("该漂流瓶已经被删除！")


@comment.handle()
async def com(bot: Bot, event: GroupMessageEvent):
    if event.group_id in black_group:
        await comment.finish()

    mes = str(event.message.extract_plain_text()).split(maxsplit=2)
    index = int(mes[1])
    data = bottle.check_bottle(index)
    if not data or data['del']:
        await check_bottle.finish("该漂流瓶不存在或已被删除！")
    user = await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id)
    try:
        commen = f"{user['nickname']}：{mes[2]}"
    except:
        await comment.finish("想评论什么呀，在后边写上吧！")
    bottle.comment(index, commen)
    try:
        await bot.send_msg(group_id=bottle.check_bottle(index)['group'], message=Message(f"[CQ:at,qq={bottle.check_bottle(index)['user']}] 你的{index}号漂流瓶被评论啦！\n{commen}"))
        await asyncio.sleep(2)
    finally:
        await comment.finish("回复成功！")


@check_bottle.handle()
async def che(bot: Bot, event: MessageEvent):
    index = int(str(event.message).split(maxsplit=1)[1])
    comment_list = bottle.check_comment(index)
    data = bottle.check_bottle(index)

    if data['del'] == 1:
        await check_bottle.finish("该漂流瓶不存在或已被删除！")
    try:
        user = await bot.get_group_member_info(group_id=data['group'], user_id=data['user'])
        user = user["nickname"]
    except:
        user = data['user_name']
    try:    
        group = await bot.get_group_info(group_id=data['group'])
        group = group["group_name"]
    except:
        group = data['group_name']
    if not comment_list:
        await check_bottle.finish("这个编号的漂流瓶还没有评论哦！")
    comment = ""
    for i in comment_list:
        comment += i+"\n"
    await check_bottle.finish(f"来自【{group}】的 {user} 的第{index}号漂流瓶：\n" + Message(data['text']) + f"\n★评论共 {len(comment_list)} 条★\n{comment}【这个瓶子被捡到了{data['picked']}次！】")


@clear.handle()
async def cle(bot: Bot, event: MessageEvent):
    bottle.clear()
    await clear.finish("所有漂流瓶清空成功！")

@remove.handle()
async def rem(bot:Bot, event: GroupMessageEvent):
    index = int(str(event.message).split()[1])
    if bottle.remove(index):
        await remove.finish(f"成功删除 {index} 号漂流瓶！")
    else:
        await remove.finish('删除失败！请检查编号')
