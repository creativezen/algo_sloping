import time
import aiohttp
import hmac
import hashlib

from pprint import pformat
from loguru import logger


class BybitClient:
    api_key: str
    secret_key: str
    testnet: bool
    api_url: str
    category: str
    recv_window: str
    
    headers: dict = {}
    
    def __init__(
        self,
        api_key,
        testnet,
        base_url,
        testnet_url,
        secret_key,
        category,
        recv_window
    ):
        self.api_key = api_key
        self.secret_key = secret_key
        self.testnet = testnet
        self.base_url = base_url
        self.testnet_url = testnet_url
        self.category = category
        self.recv_window = recv_window
    
    
    async def hash_signature(self, params, timestamp) -> str:
        """
        Создает подпись (signature) для аутентификации API-запроса
        Подпись генерируется по формуле: 
            SHA256(timestamp + api_key + recv_window + query_string)
        :params: Параметры запроса
        :timestamp: Текущее время в миллисекундах
        :return: Строка подписи в шестнадцатеричном формате
        """
        # Формируем строку запроса
        query_str = '&'.join([f"{key}={value}" for key, value in params.items()])
        
        # Объединяем все данные в одну строку для хэширования
        param_str = f"{timestamp}{self.api_key}{self.recv_window}{query_str}"
        
        # Генерируем SHA256-хэш и возвращаем его как hex-строку
        signature = hmac.new(
            bytes(self.secret_key, "utf-8"),
            param_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    
    async def set_headers(self, signature=None, timestamp=None) -> dict:
        """
        Устанавливает заголовки для авторизованного запроса к Bybit API
        Заголовки соответствуют требованиям Bybit:
        
        - X-BAPI-API-KEY: ваш публичный ключ
        - X-BAPI-SIGN: подпись запроса
        - X-BAPI-TIMESTAMP: временная метка
        - X-BAPI-RECV-WINDOW: окно времени жизни запроса (recvWindow)
        
        :signature: Подпись запроса
        :timestamp: Временная метка в мс
        :return: Словарь заголовков
        """
        if self.api_key:
            self.headers["X-BAPI-API-KEY"] = self.api_key
        if self.recv_window:
            self.headers["X-BAPI-RECV-WINDOW"] = self.recv_window
        if signature:
            self.headers["X-BAPI-SIGN"] = signature
        if timestamp:
            self.headers["X-BAPI-TIMESTAMP"] = timestamp

        return self.headers
    
    
    async def send_request(self, url, params):
        """
        Запрос к API с необходимыми параметрами и аутентификацией.

        1. Генерируется текущий timestamp в миллисекундах для подписи запроса.
        2. Формируются заголовки запроса (включая подпись) через метод `set_headers`.
        3. Выполняется GET-запрос к указанному URL с переданными параметрами.
        4. Проверяется статус ответа:
        - Если не 200 — выбрасывается исключение.
        - Если тело ответа содержит ошибку API (`retCode != 0`) — также выбрасывается исключение.
        5. В случае успеха — возвращается полезная нагрузка (`result` из JSON-ответа).

        Параметры:
        ----------
        url : str Полный URL-адрес API-метода
        params : dict Словарь параметров запроса

        Возвращает:
        ------------
        dict Данные из поля `result` JSON-ответа сервера.
        """
        # Получаем текущее время в миллисекундах для формирования подписи
        timestamp = str(int(time.time() * 1000))
        
        # Формируем заголовки запроса, включая аутентификацию и подпись
        headers = await self.set_headers(timestamp=timestamp)

        # Создаём асинхронную сессию с указанием заголовков
        async with aiohttp.ClientSession(headers=headers) as session:
            # Выполняем GET-запрос
            async with session.get(url=url, params=params, headers=headers) as response:
                # Проверяем успешность HTTP-ответа
                if response.status != 200:
                    logger.error(f"Ошибка сервера")
                    raise Exception(f"HTTP ошибка: {response.status}: {await response.text()}")

                # Парсим JSON-ответ
                data = await response.json()

                # Проверяем, нет ли ошибки на уровне API
                if data.get("retCode") != 0:
                    logger.error(f"Ошибка обработки API")
                    raise Exception(f"Ошибка в API: {data['retMsg']}")

                # Возвращаем результат, если всё прошло успешно
                return data['result']
    
        
    async def get_klines(self, symbol: str, interval: str, limit: int = 200):
        """
        Получает свечные данные (kline) для указанной пары
        :interval: Интервал свечей
        :limit: Количество запрашиваемых свечей
        :return: Список свечей (open_time, open, high, low, close, volume, turnover)
        """
        url = f"{self.base_url}/v5/market/kline"
        
        params = {
            "category": self.category,
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        
        response = await self.send_request(url=url, params=params)
        return response['list']
    
            
    async def get_instruments_info(self, symbol: str | None = None):
        """
        Получает информацию о торговой паре, такую как tickSize др.
        :return: Список информации по инструментам (для одной пары)
        """
        url = f"{self.base_url}/v5/market/instruments-info"
        
        params = {
            "category": self.category,
        }
        
        if symbol:
            params["symbol"] = symbol.upper()
        
        response = await self.send_request(url=url, params=params)
        return response['list']
            
        
    