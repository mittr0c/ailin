<p align="center" >
  <a href="https://github.com/CMHopeSunshine/LittlePaimon/tree/nonebot2"><img src="http://q.qlogo.cn/headimg_dl?dst_uin=1279605045&spec=640&img_type=jpg" width="256" height="256" alt="LittlePaimon"></a>
</p>
<h1 align="center">艾琳 | Irene</h1>
<h3 align="center">QQ聊天机器人 | 王者荣耀查询</h3>
<h4 align="center">基于<a href="https://github.com/nonebot/nonebot2" target="_blank">NoneBot2</a>和<a href="https://github.com/Mrs4s/go-cqhttp" target="_blank">go-cqhttp</a></h4>

<p align="center">
<img src="https://img.shields.io/github/license/mittr0c/ailin" alt="license">
    <img src="https://img.shields.io/badge/python-3.8+-blue" alt="python">
    <img src="https://img.shields.io/badge/nonebot-2.0.0-green">
    <img src="https://img.shields.io/badge/go--cqhttp-1.0.0-yellow">
    <img src="https://img.shields.io/badge/版本号-1.2.1-red" alt="version">
    <a href="https://jq.qq.com/?_wv=1027&k=CXHuHAmp"><img src="https://img.shields.io/badge/加入-测试群-pink"alt="QQ guild"></a>
</p>

## 丨简介

艾琳，群聊天互动机器人，实现查战力、查出装、查皮肤、光遇每日任务等功能，并设置了金币查询机制，用户花金币进行查询，通过签到、群里淘金、小游戏等方式获取金币。所有用户数据储存在本地文件夹。

持续更新中。如有问题或建议/意见，可以发送issues或加入<strong>[艾琳bot测试群](https://jq.qq.com/?_wv=1027&k=ExnAAm1V) </strong>

## 丨功能

#### | 艾琳bot `菜单` `功能` `帮助` `目录`
- [ ] 常规类
- - [x] <strong>签到</strong>  `签到` `打卡` `冒泡`
- - [x] <strong>金币查询</strong> `金币` `金币 qq号` `排名` 
- [ ] 人工智能
- - [x] <strong>AI对联</strong> `对联` `对联 xxx 5`
- - [x] <strong>AI写歌词</strong> `写歌词` `歌词 xxx`
- [ ] 查询类
- - [x] <strong>查战力</strong> `查战力 英雄名`
- - [x] <strong>查出装</strong> `查出装 英雄名`
- - [x] <strong>查皮肤</strong> `查皮肤 英雄名`
- - [x] <strong>光遇</strong> `光遇今日攻略`
- - [x] <strong>天气</strong> `天气 城市名`
- - [x] <strong>查百科</strong> `百科 xxx`
- [ ] 娱乐类
- - [x] <strong>获得金币</strong> `淘金` `抽奖`
- - [x] <strong>Jieba</strong> `jieba xxx` `拆词 xxx`
- - [x] <strong>点歌台</strong> `点歌台` `点歌 xxx`
- - [x] <strong>漂流瓶</strong> `扔漂流瓶 xxx` `捡漂流瓶`
- - [x] <strong>猜英雄</strong> `猜英雄` `猜英雄 英雄名`
- - [x] <strong>一言</strong> `一言` `随机一言`
- [ ] 更多
- - [x] <strong>关于</strong> `关于` `开发人员`

## 丨部署

#### 配置go-cqhttp

下载<strong>[go-cqhttp](https://github.com/Mrs4s/go-cqhttp) </strong>，点击.bat运行，务必选择反向代理，将config.yml中的universal设置为: ws://127.0.0.1:13579/onebot/v11/ws

#### 获取代码

git clone https://github.com/mittr0c/ailin.git

#### 进入目录

cd ailin

#### 安装依赖

pip install poetry

poetry install

## 丨配置

#### 配置.env

打开.env.dev和.env.prod文件进行配置，有注释

#### 配置configs

config.py文件包含数据库配置

config.yaml文件会在程序启动一次后生成，包含插件配置

#### 配置完毕，开始运行

poetry shell

python bot.py

部署或配置若有疑问，参见[NoneBot2文档](https://v2.nonebot.dev/)、[go-cqhttp帮助中心](https://docs.go-cqhttp.org/)

## 丨更新日志

### v1.2.1

新功能：AI写歌词，利用RNN循环神经网络训练的语言模型

weights目录下有一个我训练好的模型，我的embed size是128，hidden size是1024，batch size是32，训练了一轮，用的显卡是英伟达RTX3080，训练用时10个小时左右。

你也可以准备好歌词放入data目录，运行 <strong>训练.py</strong> ，根据提示自己训练一个模型

#### v1.1.3

新功能：金币排名、荣誉称号

优化了部分代码

#### v1.1.0

对存档地址进行了优化；相应地，对各插件的代码进行了优化

#### v1.0.7 Beta

新功能：jieba

#### v1.0.6

新功能：光遇今日攻略

#### v1.0.4

修复bug
