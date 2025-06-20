import asyncio
import configparser
from loguru import logger

import db
import sloping

conf_db: db.ConfigInfo

async def main():
    global session
    global conf_db
    
    session = await db.connect(
        config['DB']['host'],
        int(config['DB']['port']),
        config['DB']['user'],
        config['DB']['password'],
        config['DB']['db'],
    )
    
    conf_db = await db.load_config()
    logger.info(f"config_db: {conf_db.__dict__}")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    asyncio.run(main())