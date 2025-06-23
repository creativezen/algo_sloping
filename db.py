from sqlalchemy import Integer, String, Boolean, Float, Column, BigInteger, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from loguru import logger
import os

Base = declarative_base()
Session: async_sessionmaker

class Config(Base):
    __tablename__ = "config"
    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[str] = mapped_column(String)

class SymbolsSettings(Base):
    __tablename__ = "symbols_settings"
    symbol: Mapped[str] = mapped_column(String, primary_key=True)
    status: Mapped[int] = mapped_column(Integer)
    interval: Mapped[str] = mapped_column(String)
    order_size: Mapped[float] = mapped_column(Float)
    leverage: Mapped[int] = mapped_column(Integer)
    length: Mapped[int] = mapped_column(Integer)
    atr_length: Mapped[int] = mapped_column(Integer)
    take: Mapped[float] = mapped_column(Float)
    stop: Mapped[float] = mapped_column(Float)

class Trades(Base):
    __tablename__ = "trades"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String)
    order_size: Mapped[float] = mapped_column(Float)
    side: Mapped[bool] = mapped_column(Boolean)
    status: Mapped[str] = mapped_column(String)
    open_time: Mapped[BigInteger] = mapped_column(BigInteger)
    close_time: Mapped[BigInteger] = mapped_column(BigInteger)
    entry_price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[float] = mapped_column(Float)
    take_price: Mapped[float] = mapped_column(Float)
    stop_price: Mapped[float] = mapped_column(Float)
    result: Mapped[float] = mapped_column(Float)
    msg_id: Mapped[int] = mapped_column(Integer)

class Orders(Base):
    __tablename__ = "orders"
    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trade_id: Mapped[int] = mapped_column(Integer)
    symbol: Mapped[str] = mapped_column(String)
    time: Mapped[BigInteger] = mapped_column(BigInteger)
    side: Mapped[bool] = mapped_column(Boolean)
    type: Mapped[str] = mapped_column(String)
    reduce: Mapped[bool] = mapped_column(Boolean)
    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[float] = mapped_column(Float)


class ConfigInfo:
    """
    Класс для хранения конфигурационных данных, загруженных из базы данных.
    Предоставляет удобный способ динамической инициализации атрибутов,
    а также автоматически преобразует значения к числовым типам (int/float),
    если это возможно.
    Все атрибуты инициализируются как None, если не переданы в `data`.
    """
    api_key: str
    api_secret: str
    trade_mode: int

    def __init__(self, data):
        """
        Инициализирует объект на основе словаря `data`.
        Попытка преобразования значений:
        - Сначала пытается привести значение к `int`.
        - Если не удалось — пытается привести к `float`.
        - Если всё неудачно — сохраняет исходное значение.
        """
        # Инициализируем все объявленные атрибуты как None
        for key in self.__class__.__annotations__:
            setattr(self, key, None)

        # Обрабатываем входные данные
        for key, value in data.items():
            if key not in self.__class__.__annotations__:
                logger.warning(f"Ключ '{key}' не определен в классе ConfigInfo. Пропускаю.")
                continue
            
            # Если значение равно None
            if value is None:
                # Если значение None, то просто присваиваем его атрибуту
                setattr(self, key, value)
                continue

            try:
                # Попытка преобразовать значение в int
                value = int(value)
            except ValueError as e:
                logger.warning(f"Не удалось преобразовать '{key}' в int: {e}. Пробую преобразовать в float.")
                try:
                    # Попытка преобразовать значение в float
                    value = float(value)
                except ValueError as e:
                    logger.error(f"Не удалось преобразовать '{key}' в float: {e}. Оставляю оригинальное значение.")
                    pass
            # Устанавливаем значение атрибута
            setattr(self, key, value)


async def connect(
    host: str,
    port: int,
    user: str,
    password: str,
    db: str
):
    """
    Асинхронно подключается к PostgreSQL и создаёт все таблицы, если они ещё не существуют.
    Также инициализирует фабрику сессий (`Session`) для работы с БД.
    Возвращает:
    ------------
    async_sessionmaker
        Фабрика асинхронных сессий для работы с БД.
    Исключения:
    ------------
    SQLAlchemyError
        Если произошла ошибка на уровне SQLAlchemy.
    Exception
        Для всех остальных непредвиденных ошибок.
    """
    global Session
    try:
        # Создание асинхронного движка
        engine = create_async_engine(f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}")
        # Создание таблиц
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        # Создание фабрики сессий
        Session = async_sessionmaker(engine, expire_on_commit=False)
        logger.success("Успешное подключение к бд и создание таблиц.")
        return Session
    except SQLAlchemyError as e:
        # Обработка ошибок SQLAlchemy
        logger.error(f"Ошибка SQLAlchemy при подключении к базе данных: {e}")
        raise  # Переброс исключения для вызывающего кода
    except Exception as e:
        # Обработка всех остальных ошибок
        logger.error(f"Непредвиденная ошибка при подключении к базе данных: {e}")
        raise  # Переброс исключения для вызывающего кода


async def load_config():
    """
    Инициализирует конфигурационные параметры в базе данных и загружает их обратно.
    1. Для каждого ключа из класса `ConfigInfo` проверяет, существует ли запись в таблице `Config`.
       Если записи нет — добавляет её со значением по умолчанию (пустая строка).
    2. После инициализации загружает все записи из таблицы `Config`.
    3. Преобразует их в экземпляр класса `ConfigInfo`.

    Возвращает:
    ------------
    ConfigInfo
        Объект с загруженной конфигурацией из базы данных.
    Исключения:
    ------------
    SQLAlchemyError
        Если произошла ошибка на уровне SQLAlchemy при работе с БД.
    Exception
        Для всех остальных непредвиденных ошибок.
    """
    # Инициализация конфигурации в базе данных
    for key in ConfigInfo.__annotations__.keys():
        try:
            async with Session() as session:
                # Проверяем, существует ли запись с таким ключом
                existing = (await session.execute(select(Config).where(Config.key == key))).scalar_one_or_none()
                if not existing:
                    # Добавляем запись только если её нет
                    session.add(Config(key=key, value=""))  # Значение по умолчанию — пустая строка
                    await session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении конфигурации '{key}' в базу данных: {e}")
            continue  # Продолжаем выполнение функции даже при ошибке
        except Exception as e:
            logger.error(f"Непредвиденная ошибка при добавлении конфигурации '{key}': {e}")
            continue  # Продолжаем выполнение функции даже при ошибке

    try:
        # Загрузка данных из базы
        async with Session() as session:
            result = (await session.execute(select(Config))).scalars().all()
            data = {row.key: row.value for row in result}
            return ConfigInfo(data)
    except SQLAlchemyError as e:
        # Логирование ошибки при чтении данных из базы
        logger.error(f"Ошибка при загрузке данных конфигурации из базы данных: {e}")
        raise  # Переброс исключения для вызывающего кода
    except Exception as e:
        # Логирование непредвиденных ошибок
        logger.error(f"Непредвиденная ошибка при загрузке данных конфигурации: {e}")
        raise  # Переброс исключения для вызывающего кода
    finally:
        logger.success("Конфигурация загружена из базы данных.")
