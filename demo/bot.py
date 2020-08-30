import asyncio
import json
import logging
import random

from yufuquantsdk.clients import RESTAPIClient, WebsocketAPIClient

logger = logging.getLogger(__file__)

CONFIG_FILENAME = "config.json"


class ConfigException(Exception):
    pass


def load_config():
    try:
        with open(CONFIG_FILENAME, mode="rt", encoding="utf-8") as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        raise ConfigException(f"Config file {CONFIG_FILENAME} does not exist.")


async def main():
    config = load_config()
    rest_api_base_url = config["rest_api_base_url"]
    ws_api_uri = config["ws_api_uri"]
    auth_token = config["auth_token"]
    robot_id = config["robot_id"]

    total_balance = 0.5

    rest_api_client = RESTAPIClient(base_url=rest_api_base_url, auth_token=auth_token)
    ws_api_client = WebsocketAPIClient(uri=ws_api_uri)

    # 发送认证消息，认证后才能广播机器人日志消息
    await ws_api_client.auth(auth_token=auth_token)

    # 订阅机器人日志话题
    topics = ["robot#1.log"]
    await ws_api_client.sub(topics)

    while True:
        # 获取最新的机器人配置信息
        robot_cfg = await rest_api_client.get_robot_config(robot_id)
        # 更新策略参数
        strategy_parameters = robot_cfg["strategy_parameters"]
        trade_interval = strategy_parameters.get("trade_interval", 5)  # 单轮交易的时间间隔
        direction = strategy_parameters.get(
            "direction", "both"
        )  # 交易方向。long：只做多；short：只做空；both：多空都做

        # 这个示例机器人仅用于演示如何使用 yufuquant SDK 和 yufuquant 后台交互，不涉及和数字货币交易所的实际交互。
        decision = random.randint(-1, 1)  # 随机生成 -1、0、1。-1 做空；0 休息；1 做多。
        price = round(random.randint(3000, 20000), 2)  # 生成一个随机价格
        amount = round(random.random(), 4)  # 随机生成 0~1 的数，作为比特币虚拟交易的数量。

        if decision == -1:
            if direction == "long":
                msg = f"指标做空，用户禁止开空。"
            else:
                msg = f"做空BTC，做空价: {price}，做空数量：{amount}。"
        elif decision == 0:
            msg = f"没有指标方向，休息..."
        elif decision == 1:
            if direction == "short":
                msg = f"指标做多，用户禁止开多。"
            else:
                msg = f"做多BTC，做多价: {price}，做多数量：{amount}。"
        else:
            msg = "指标混乱！！！"

        logger.info(msg)
        await ws_api_client.robot_log(text=msg)

        profit = round(
            random.random() * random.randint(-1, 1), 4
        )  # 随机产生 -1~1 之间数字，作为虚拟交易的收益
        msg = f"本轮交易收益 {profit} BTC。"
        logger.info(msg)
        await ws_api_client.robot_log(text=msg)

        # 回传资产
        total_balance += profit
        await rest_api_client.patch_robot_asset_record(
            robot_id=robot_id,
            data={"total_balance": total_balance},
        )
        await asyncio.sleep(trade_interval)


if __name__ == "__main__":
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    asyncio.run(main())
