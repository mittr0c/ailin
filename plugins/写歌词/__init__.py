#!/usr/bin/env python3
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot import on_command

from plugins.fun import *
from plugins.AI写歌词.main import *

import jieba

歌词1 = on_command("歌词",aliases={"写歌词", "AI写歌词" ,"ai写歌词"})

debug = False

embed_size = 128         #128
hidden_size = 1024        #1024
lr = 0.001
lstm_layers = 2
batch_size = 2
epochs = 15
seq_len = 48

@歌词1.handle()
async def _(event: GroupMessageEvent):
    qq_id = str(event.user_id)  # 获取qq号
    当前金币 = 查金币(qq_id)
    if 当前金币 < 2:
        await 歌词1.send("需花费2金币，发送“签到”或“群里淘金”获得金币")
    elif str(event.message) == '写歌词' or str(event.message) == 'AI写歌词' or str(event.message) == 'ai写歌词' or str(event.message) == '歌词':
        await 歌词1.send("发送“歌词 你想说的话”，注意空一格")
    else:
        await 歌词1.send('正在生成中...')
        text = str(event.message).split(maxsplit=1)[1]  #返回空格之后的内容
        cut = jieba.lcut(text)
        qsc = str()
        for words in cut:
            qsc = qsc + '/' + words
        result = str(xiegeci(qsc))
        #time.sleep(10)
        await 歌词1.send(result)
