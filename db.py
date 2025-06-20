from sqlalchemy import Integer, String, Boolean, Float, Column, BigInteger, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from loguru import logger


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