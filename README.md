<p align="center" >
  <a href="https://github.com/CMHopeSunshine/LittlePaimon/tree/nonebot2"><img src="http://q.qlogo.cn/headimg_dl?dst_uin=1279605045&spec=640&img_type=jpg" width="256" height="256" alt="LittlePaimon"></a>
</p>
<h1 align="center">艾琳 | Irene</h1>
<h3 align="center">QQ聊天机器人 | 王者荣耀查询</h3>
<h4 align="center">基于<a href="https://github.com/nonebot/nonebot2" target="_blank">NoneBot2</a>和<a href="https://github.com/Mrs4s/go-cqhttp" target="_blank">go-cqhttp</a></h4>

![maven](https://img.shields.io/badge/python-3.8%2B-blue)
![maven](https://img.shields.io/badge/nonebot-2.0.0-yellow)
![maven](https://img.shields.io/badge/go--cqhttp-1.0.0-red)

## 丨简介

艾琳，群聊天互动机器人，实现查战力、查出装、查皮肤等功能，并设置了金币查询机制，用户花金币进行查询，通过签到、群里淘金、小游戏等方式获取金币。所有用户数据储存在本地文件夹。

持续更新中。如有问题或建议/意见，可以发送issues或加入<strong>[艾琳bot测试群](https://jq.qq.com/?_wv=1027&k=ExnAAm1V) </strong>

## | 功能

<summary>常规类</summary>

- [x] 签到
- 发送“签到”或“打卡”，随机获得50-100金币，每人每天限一次。

- [x] 金币查询
- 发送“金币”查自己金币，发送“金币 qq号”查他人金币。

<summary>查询类</summary>

- [x] 查战力
- 发送“查战力 英雄名”查进行查询。

- [x] 查出装
- 发送“查出装 英雄名”查进行查询。

- [x] 查皮肤
- 发送“查皮肤 英雄名”查进行查询。

- [x] 天气
- 发送“天气 城市名”查进行查询。

<summary>娱乐类</summary>

- [x] 群里淘金
- 群里发送“淘金”，获得金币数取决于该群人数和该群淘金人数，每个群每人限一次。

- [x] 抽奖
- 发送“抽奖”，输赢各50%机会，随机50-100金币。

- [x] AI对联
- 发送“对联 想说的内容”，或“对联 内容 数字”生成多条对联。

- [x] 点歌台
- 点歌/qq点歌/网易点歌/酷我点歌/酷狗点歌/咪咕点歌/b站点歌 + 关键词

- [x] 漂流瓶
- 发送“扔漂流瓶 内容”，还可发送：捡漂流瓶/举报漂流瓶/评论漂流瓶/查看漂流瓶

- [ ] 猜英雄
- 进度：
<progress value="22" max="100">
</progress>

## 部署

#### 配置go-cqhttp

下载<strong>[go-cqhttp](https://github.com/Mrs4s/go-cqhttp) </strong>，点击.bat运行，务必选择反向代理，将config.yml中的universal设置为: ws://127.0.0.1:8080/onebot/v11/ws

#### 获取代码
git clone https://github.com/mittr0c/ailin.git

#### 进入目录
cd ailin

#### 安装依赖
pip install poetry      # 安装 poetry
poetry install          # 安装依赖

## 配置

#### 配置.env

打开.env.dev和.env.prod文件进行配置，有注释

#### 配置configs

config.py文件包含数据库配置

config.yaml文件会在程序启动一次后生成，包含插件配置

#### 配置完毕，开始运行

poetry shell
python bot.py

部署或配置若有疑问，参见[NoneBot2文档](https://v2.nonebot.dev/)、[go-cqhttp帮助中心](https://docs.go-cqhttp.org/)

```
