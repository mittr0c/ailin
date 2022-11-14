# -*- coding: utf-8 -*-
# @Author  : 子龙君
# @Email   :  1435608435@qq.com
# @Github    : Kaguya
# @Software: PyCharm

import httpx
import datetime,time
import json

import nonebot
from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11 import NetworkError as networkError

from plugins.fun import *

daily_yoli = on_command("daily_yoli", aliases={"光遇今日攻略"})

try:
    BotName = nonebot.get_driver().config.nickname
except Exception as e:
    logger.error(e)
    logger.warning('您还没有配置bot的昵称，请先进入env文件配置')

class SkyDaily:
    """光遇类"""

    def __init__(self):
        self.url = 'https://weibo.com/ajax/statuses/mymblog?uid=7360748659&page=1&feature=0'
        self.longtext = 'https://weibo.com/ajax/statuses/longtext?id='
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                          '/62.0.3202.9 Safari/537.36',
            'cookie': 'SUB=_2AkMUd3SHf8NxqwFRmP8Ty2Pna4VwywzEieKiK4VcJRMxHRl'
                      '-yT9jqnAOtRB6P_daaLXfdvYkPfvZhXy3bTeuLdBjWXF9;'
        }
        self.copyright_ = ('------------'
                           '\r【数据来源：微博@今天游离翻车了吗】\n'
                           '--本插件仅做数据展示之用，著作权归原文作者所有。'
                           '转载或转发请附文章作者微博--')

    @staticmethod
    def get_today():
        """获取今日日期"""
        date = datetime.date.today().timetuple()
        today = str(date.tm_mon) + '月' + str(date.tm_mday) + '日'
        today_format = str(date.tm_mon) + '.' + str(date.tm_mday)
        print('今天是：{}'.format(today))
        return today_format
    async def get_mblog_id(self):
        """获取微博 @今天游离翻车了吗 顶置文章详情"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=self.url,
                headers=self.headers)
            content = json.loads(response.text)
            overhead = content['data']['list'][0]
            return overhead

    async def get_longtext(self, mblog_id: str):
        """获取微博 @今天游离翻车了吗 顶置文章长文本"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=self.longtext + mblog_id,
                headers=self.headers)
            content = json.loads(response.text)
            longtext = content['data']['longTextContent']
            return longtext

    async def get_data(self):
        """获取今日攻略数据"""
        results = MessageSegment.text('')
        today = self.get_today()
        overhead = await self.get_mblog_id()
        mblog_id = overhead['mblogid']
        longtext = await self.get_longtext(mblog_id)
        # if today in longtext:
        results += MessageSegment.text(longtext)
        pic_infos = overhead['pic_infos']
        for pic in pic_infos:
            large_url = pic_infos[pic]['large']['url']
            img = MessageSegment.image(large_url)
            results += img
        results += self.copyright_  # 附加版权信息
        # else:
        #     notice = '今日数据还未更新，请耐心等候'
        #     logger.warning('今日数据还未更新，请耐心等候')
        #     results += MessageSegment.text(notice)
        return results

# 转发消息用：
# async def chain_reply(
#         # 构造聊天记录转发消息，参照了塔罗牌插件
#         bot: Bot,
#         msg: MessageSegment
# ):
#     chain = []
#     nick = ''
#     for name in BotName:
#         nick = name
#     data = {
#         "type": "node",
#         "data": {
#             "name": nick,
#             "uin": f"{bot.self_id}",
#             "content": msg
#         },
#     }
#     chain.append(data)
#     return chain

@daily_yoli.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id   # 获取群号
    qq_id = str(event.user_id)  # 获取qq号
    新用户(qq_id)
    新群(group_id)
    with open(f'data/艾琳/群/{group_id}/信息2.json', 'r', encoding='utf-8')as f:
        dic = json.load(f)
    查询日期 = dic['Skydate']
    当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    if 查询日期 == 123090123:   #if 查询日期 == 当前日期:
        await daily_yoli.send("【光遇今日攻略】本群已经有人查询过了，请明天再来~")
    elif 查金币(qq_id) < 15:
        await daily_yoli.send("需花费15金币，发送“签到”或“群里淘金”获得金币")
    else:
        减金币(qq_id,15)
        with open(f'data/艾琳/群/{group_id}/信息2.json', 'r+', encoding='utf-8')as f:
            dic = json.load(f)
            dic['Skydate'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            dic['SkyTimes'] = dic['SkyTimes'] + 1
            f.seek(0)  # 指向文本开头
            f.truncate()  # 清空文本
            json.dump(dic, f)   #写入数据
        try:
            sky = SkyDaily()

            #图像版：
            results = await sky.get_data()
            光遇结果 = str(results).split('[CQ:image,file=')
            for sky in range(1, 6):
                result = 光遇结果[sky]
                result = str(result).split(',cache=true,proxy=true]')[0]
                await daily_yoli.send(MessageSegment.image(result))

            #文字版：
            # results = await sky.get_data()
            # 光遇结果 = str(results).split('\n', maxsplit=39)
            #
            # for sky in range(0, 40):
            #     result = 光遇结果[sky]
            #     await daily_yoli.send(result)

            #消息转发版：
            # chain = await chain_reply(bot, results)
            # await bot.send_group_forward_msg(
            #     group_id=event.group_id,
            #     messages=chain
            # )

        except networkError:
            logger.error('NetworkError: 网络环境较差，调用发送信息接口超时')
            await daily_yoli.send(
                message='网络环境较差，调用发送信息接口超时'
            )
