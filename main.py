import asyncio
import configparser
from pprint import pformat
from loguru import logger

import db
from bybit.client import BybitClient
import sloping


# Получаем конфигурацию из файла config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Конфигурация для работы с БД
conf_db: db.ConfigInfo

# Объект для работы с Bybit API
client: BybitClient

# Переменная для хранения словаря всех доступных символов
all_symbols: dict = {}


async def load_symbols():
    global all_symbols
    
    while True:
        try:
            all_symbols = await client.get_instruments_info()
            logger.debug(pformat(all_symbols))
        except Exception as e:
            logger.error(f"Ошибка загрузки символов: {e}")
            pass
        finally:
            await asyncio.sleep(3600)


async def connect_ws():
    if not conf_db.trade_mode:
        return
    logger.info("Подключение к WebSocket...")       


async def main():
    global session
    global conf_db
    global client
    
    # Устанавливаем соединение с БД
    session = await db.connect(
        config['DB']['HOST'],
        int(config['DB']['PORT']),
        config['DB']['USER'],
        config['DB']['PASSWORD'],
        config['DB']['DB'],
    )
    
    # Загружаем конфигурацию из БД
    conf_db = await db.load_config()
    
    # Создаем экземпляр класса BybitClient
    client = BybitClient(
        api_key=config['BYBIT']['API_KEY'],
        secret_key=config['BYBIT']['SECRET_KEY'],
        testnet=config.getboolean('BOT', 'TESTNET'),
        base_url=config['BYBIT']['BASE_URL'],
        testnet_url=config['BYBIT']['TESTNET_URL'],
        category=config['BYBIT']['CATEGORY'],
        recv_window=config['BYBIT']['RECV_WINDOW'],
    )
    
    asyncio.create_task(load_symbols())
    logger.debug(pformat(all_symbols))


if __name__ == "__main__":
    asyncio.run(main())