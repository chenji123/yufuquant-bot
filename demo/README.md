# 渔夫量化机器人示例

这是使用 [yufuquant-sdk](https://github.com/yufuquant/yufuquant-sdk) 开发的一个机器人示例，用于说明渔夫量化交易机器人的开发和使用方法。出于演示目的，这个机器人并未与真实的数字货币交易所接口交互，而是使用随机数 mock 了策略收益。

## 环境

Python 3.7+

## 启动机器人

1. 克隆或者下载本仓库的代码到本地或者服务器；
2. 进入 demo 目录下，安装依赖（推荐使用虚拟环境） `pip install -r requirements.txt`；
3. 复制 config.example.json 到同级目录，新复制的文件命名为 config.json；
4. 修改 config.json 中的配置项，各配置项说明见下方;
5. 运行 bot.py 脚本：`python -m bot.py`。

## 配置项说明

各配置项位于 config.json 文件内。

| 配置项            | 说明                                                         | 示例                                     |
| ----------------- | ------------------------------------------------------------ | ---------------------------------------- |
| rest_api_base_url | 渔夫量化后端 API 地址                                        | http://127.0.0.1:8000/api/v1             |
| ws_api_uri        | 渔夫量化后端 Weboskcet 地址                                  | ws://127.0.0.1:8000/ws/v1/streams/       |
| auth_token        | 身份认证令牌，详见：[认证令牌](https://yufuquant.github.io/yufuquant-user-manual/admin/auth_token/) | nd2f47h5h5ba04e23v00085geby6c12mam9ff9ec |
| robot_id          | 启动的机器人ID，详见：[查询机器人ID](https://yufuquant.github.io/yufuquant-user-manual/admin/robot/#%E6%9F%A5%E8%AF%A2%E6%9C%BA%E5%99%A8%E4%BA%BAid) | 1                                        |

