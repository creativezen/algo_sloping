import asyncio
import hashlib
import hmac
import time
import aiohttp
import threading
import websocket
import ujson
from .error import WebsocketException


class Websocket:
    base_url: str
    ws: websocket.WebSocketApp | aiohttp.ClientWebSocketResponse
    recv_window = 5000
    reconnect_timeout = 30
    ping_interval = 180

    def __init__(self, category, asynced, streams, on_message, on_open, on_close, on_error, testnet, api_key=None,
                 secret_key=None):
        if not category and (not api_key or not secret_key):
            raise ValueError("Category not set")
        self.category = category
        self.__asynced = asynced
        if isinstance(streams, str):
            streams = [streams]
        self.streams = streams
        self.on_message = on_message
        self.on_open = on_open
        self.on_close = on_close
        self.on_error = on_error
        self.testnet = testnet
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = f'wss://stream-testnet.bybit.com/v5/' if testnet else f'wss://stream.bybit.com/v5/'
        self.base_url += f'private' if api_key and secret_key else f'public/{category}'
        self.__working = True
        self.__connected = False
        self.__ws = None
        if self.__asynced:
            self.__task = asyncio.create_task(self.__run_async())
            if self.api_key and self.secret_key:
                self.__ping_task = asyncio.create_task(self.__ping_service_async())
        else:
            self.__thread = threading.Thread(target=self.__run_sync, daemon=True)
            self.__thread.start()
            if self.api_key and self.secret_key:
                self.__ping_thread = threading.Thread(target=self.__ping_service_sync, daemon=True)
                self.__ping_thread.start()

    def close(self):
        self.__working = False
        if self.__asynced:
            try:
                self.__task.cancel()
            except:
                pass
            try:
                self.__ping_task.cancel()
            except:
                pass
            return asyncio.sleep(0)
        else:
            try:
                self.ws.close()
            except:
                pass

    def __run_sync(self):
        while self.__working:
            try:
                self.__connected = False
                self.ws = websocket.WebSocketApp(self.base_url, on_open=self.__on_open, on_message=self.__on_message,
                                                 on_error=self.__on_error, on_close=self.__on_close)
                thread = threading.Thread(target=self.ws.run_forever, daemon=True)
                thread.start()
                thread.join()
            except Exception as e:
                self.__on_error(self, e)
            finally:
                if not self.__connected:
                    time.sleep(self.reconnect_timeout)

    async def __run_async(self):
        while self.__working:
            try:
                self.__connected = False
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(self.base_url) as self.ws:
                        if self.api_key and self.secret_key:
                            await self.__auth()
                        elif self.streams:
                            await self.__subscribe(self.streams)
                        try:
                            if self.on_open:
                                await self.on_open(self)
                        except Exception as e:
                            await self.__on_error_async(e)
                        self.__connected = True
                        async for msg in self.ws:
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                if not self.__working:
                                    break
                                data = msg.data
                                try:
                                    data = ujson.loads(data)
                                except ujson.JSONDecodeError:
                                    pass
                                try:
                                    if data.get('success') is False:
                                        if self.__asynced:
                                            await self.__on_error_async(WebsocketException(data.get('ret_msg')))
                                        else:
                                            await self.__on_error_async(WebsocketException(data.get('ret_msg')))
                                    elif data.get('op') == 'auth' and data.get('success'):
                                        await self.__subscribe(self.streams)
                                    await self.on_message(self, data)
                                except Exception as e:
                                    await self.__on_error_async(e)
                            elif msg.type == aiohttp.WSMsgType.ERROR:
                                await self.__on_error_async(msg)
                                break
            except asyncio.CancelledError:
                break
            except Exception as e:
                await self.__on_error_async(e)
            finally:
                try:
                    if self.on_close:
                        await self.on_close(self)
                except Exception as e:
                    await self.__on_error_async(e)
                if not self.__connected:
                    await asyncio.sleep(self.reconnect_timeout)

    def __on_open(self, *_):
        try:
            self.__connected = True
            if self.api_key and self.secret_key:
                self.__auth()
            elif self.streams:
                self.__subscribe(self.streams)
            if self.on_open:
                return self.on_open(self)
        except Exception as e:
            self.__on_error(self, e)

    def __on_message(self, _, data):
        try:
            data = ujson.loads(data)
            if data.get('success') is False:
                self.__on_error(WebsocketException(data.get('ret_msg')))
            elif data.get('op') == 'auth' and data.get('success'):
                self.__subscribe(self.streams)
            if self.on_message:
                self.on_message(self, data)
        except Exception as e:
            self.__on_error(self, e)

    def __on_error(self, *e):
        if self.on_error:
            try:
                return self.on_error(self, e[-1])
            except:
                pass

    async def __on_error_async(self, e):
        if self.on_error:
            try:
                await self.on_error(self, e)
            except:
                pass

    def __on_close(self, *_):
        try:
            if self.on_close:
                return self.on_close(self)
        except Exception as e:
            self.__on_error(e)

    def send_json(self, msg):
        msg = ujson.dumps(msg)
        if self.__asynced:
            return self.ws.send_str(msg)
        else:
            self.ws.send_text(msg)

    def __subscribe(self, streams: list, unsubscribe=False):
        msg = {
            "op": "unsubscribe" if unsubscribe else "subscribe",
            "args": streams
        }
        return self.send_json(msg)

    def subscribe(self, streams: list):
        if not isinstance(streams, list):
            streams = [streams]
        self.streams.extend(streams)
        return self.__subscribe(streams)

    def unsubscribe(self, streams: list):
        if not isinstance(streams, list):
            streams = [streams]
        if self.streams:
            self.streams = [stream for stream in self.streams if stream not in streams]
        return self.__subscribe(streams, unsubscribe=True)

    def __auth(self):
        timestamp = int(time.time() * 1000 + self.recv_window)
        data = f"GET/realtime{timestamp}"
        signature = hmac.new(bytes(self.secret_key, "utf-8"), data.encode("utf-8"), hashlib.sha256).hexdigest()
        msg = {
            "op": "auth",
            "args": [self.api_key, timestamp, signature]
        }
        return self.send_json(msg)

    def __ping_service_sync(self):
        ping_msg = ujson.dumps({"op": "ping"})
        while True:
            try:
                if not self.__working:
                    break
                time.sleep(self.ping_interval)
                if self.__connected and self.__working:
                    self.ws.send_text(ping_msg)
            except Exception as e:
                self.__on_error(self.ws, e)

    async def __ping_service_async(self):
        ping_msg = ujson.dumps({"op": "ping"})
        while True:
            try:
                if not self.__working:
                    break
                await asyncio.sleep(self.ping_interval)
                if self.__connected and self.__working:
                    await self.ws.send_str(ping_msg)
            except asyncio.CancelledError:
                break
            except Exception as e:
                await self.__on_error(self.ws, e)
