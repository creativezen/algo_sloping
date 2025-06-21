import hashlib
import hmac
import time
import aiohttp
import requests
import ujson
import inspect
from .error import ClientException, ServerException
from .endpoints import Endpoints
from .websockets import Websocket


class Client(Endpoints):
    base_url: str
    recv_window = 5000
    __session: aiohttp.ClientSession or requests.Session

    def __init__(self, api_key=None, secret_key=None, testnet=False, category=None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.testnet = testnet
        self.base_url = "https://api-testnet.bybit.com" if testnet else "https://api.bybit.com"
        self.category = category
        self.__headers = {
            "Content-Type": "application/json;charset=utf-8"
        }
        if api_key and secret_key:
            self.__headers["X-BAPI-API-KEY"] = api_key
            self.__headers["X-BAPI-RECV-WINDOW"] = str(self.recv_window)
        frame = inspect.currentframe().f_back
        self.__asynced = inspect.iscoroutinefunction(frame.f_globals.get(frame.f_code.co_name))
        if self.__asynced:
            self.__session = aiohttp.ClientSession(headers=self.__headers)
        else:
            self.__session = requests.Session()
            self.__session.headers.update(self.__headers)

    def close(self):
        return self.__session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def __get_signature(self, post_method, data, timestamp):
        param_str = timestamp + self.api_key + str(self.recv_window)
        param_str += ujson.dumps(data) if post_method else "&".join([f"{k}={v}" for k, v in data.items()])
        return hmac.new(bytes(self.secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256).hexdigest()

    def __prepare_data(self, post_method, sign, data):
        new_data = {}
        for key, value in data.items():
            if value is not None:
                if isinstance(value, list):
                    new_data[key] = ujson.dumps(value)
                else:
                    new_data[key] = str(value)
            elif key == "category" and self.category:
                new_data[key] = str(self.category)
        headers = self.__headers.copy()
        if sign:
            timestamp = str(int(time.time() * 1000))
            headers["X-BAPI-SIGN"] = self.__get_signature(post_method, new_data, timestamp)
            headers["X-BAPI-TIMESTAMP"] = timestamp
        self.__session.headers.update(headers)
        return new_data

    def request(self, post_method, url, sign, **data):
        data = self.__prepare_data(post_method, sign, data)
        data = {"data": ujson.dumps(data)} if post_method else {"params": data}
        if self.__asynced:
            return self.__request_async(post_method, url, data)
        else:
            return self.__request_sync(post_method, url, data)

    def __request_sync(self, post_method, url, data):
        with (self.__session.post if post_method else self.__session.get)(self.base_url + url, **data) as res:
            return self.__response(res.status_code, res.headers, res.text)

    async def __request_async(self, post_method, url, data):
        async with (self.__session.post if post_method else self.__session.get)(self.base_url + url, **data) as res:
            return self.__response(res.status, dict(res.headers), await res.text())

    @staticmethod
    def __response(code, headers, text):
        if 400 <= code < 500:
            raise ClientException(code, text, headers)
        if code >= 500:
            raise ServerException(code, text)
        try:
            data = ujson.loads(text)
            if ret_code := data.get("retCode"):
                raise ClientException(code, text, headers, ret_code, data.get("retMsg"))
            return data.get("result")
        except ujson.JSONDecodeError:
            return text

    async def __ws_async(self, category, streams, on_message, on_open, on_close, on_error, api_key=None,
                         secret_key=None):
        return Websocket(category, True, streams, on_message, on_open, on_close, on_error, self.testnet,
                         api_key, secret_key)

    def websocket(self, streams=None, on_message=None, on_open=None, on_close=None, on_error=None, category=None):
        if self.__asynced:
            return self.__ws_async(category if category else self.category, streams, on_message, on_open, on_close,
                                   on_error)
        else:
            return Websocket(category if category else self.category, False, streams, on_message, on_open,
                             on_close, on_error, self.testnet)

    def websocket_userdata(self, streams=None, on_message=None, on_open=None, on_close=None, on_error=None,
                           category=None):
        if self.__asynced:
            return self.__ws_async(category if category else self.category, streams, on_message, on_open, on_close,
                                   on_error, self.api_key, self.secret_key)
        else:
            return Websocket(category if category else self.category, False, streams, on_message, on_open,
                             on_close, on_error, self.testnet, self.api_key, self.secret_key)
