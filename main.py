import asyncio
import configparser
from loguru import logger

import db
from bybit.client import BybitClient
import sloping


# Получаем конфигурацию из файла config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Переменные для работы с БД
conf_db: db.ConfigInfo

# Для работы с Bybit API
client: BybitClient

async def main():
    global session
    global conf_db
    
    client = BybitClient(
        api_key=config['BYBIT']['API_KEY'],
        secret_key=config['BYBIT']['SECRET_KEY'],
        testnet=config['BYBIT']['TESTNET'],
        api_url=config['BYBIT']['BASE_URL'] if config['BYBIT']['TESTNET'] else config['BYBIT']['TESNET_URL'],
        category=config['BYBIT']['CATEGORY'],
        recv_window=config['BYBIT']['RECV_WINDOW'],
    )
    
    session = await db.connect(
        config['DB']['HOST'],
        int(config['DB']['PORT']),
        config['DB']['USER'],
        config['DB']['PASSWORD'],
        config['DB']['DB'],
    )
    
    conf_db = await db.load_config()
    logger.info(f"config_db: {conf_db.__dict__}")


if __name__ == "__main__":
    asyncio.run(main())