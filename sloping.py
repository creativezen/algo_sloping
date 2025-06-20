from collections import deque
import numpy as np
from dataclasses import dataclass
import plotly.graph_objects as go
import time

# датакласс для сигналов
@dataclass
class Signal:
    side: bool
    price: float
    line: tuple

# класс для поиска наклонок
class Sloping:
    length: int
    min_space: int
    ts: deque
    open: deque
    high: deque
    low: deque
    close: deque
    body_up: deque
    body_down: deque

    def __init__(self, length, min_space=5, max_len=500):
        # инициализируем переменные
        self.length = length
        self.min_space = min_space
        self.max_len = max_len
        # счетчики сигналов
        self._last_signal_resistance = min_space + 1
        self._last_signal_support = min_space + 1
        # создаем очереди
        for key, value in self.__annotations__.items():
            if issubclass(value, deque):
                setattr(self, key, deque([.0], maxlen=self.max_len))

    # функция для добавления свечи
    def add_kline(self, ts, open, high, low, close):
        ts = int(ts)
        # проверяем не дублируется ли свеча
        if not self.ts or ts > self.ts[-1]:
            # заполняем очереди
            self.ts.append(ts)
            self.open.append(float(open))
            self.high.append(float(high))
            self.low.append(float(low))
            self.close.append(float(close))
            # определяем верх и низ тела свечи
            self.body_up.append(max(float(open), float(close)))
            self.body_down.append(min(float(open), float(close)))
            # возвращаем True если добавили свечу
            return True
        return False

    # функция для получения сигнала
    def get_value(self, support=True, resistance=True):
        # если не хватает количества свеч, то пропускаем этот сигнал
        if len(self.ts) < self.length + 1:
            return None
        for is_resistance, side in enumerate([support, resistance]):
            # если нам не нужно вычислять поддержу или сопротивление, то пропускаем
            if not side:
                continue
            # берем окно для поиска наклонки (необходимую нам часть тела свечи)
            window = np.array(list(self.body_up if is_resistance else self.body_down)[-self.length:])
            # генерируем индексы свечей
            x = np.arange(len(window))
            # вычисляем точки для поиска наклонки
            slope, intercept = np.polyfit(x, window, 1)
            points = slope * x + intercept
            # ищем минимум или максимум в пределах окна, в зависимости от того, что мы ищем
            value = (window - points).argmax() if is_resistance else (window - points).argmin()
            # получаем наклонную линию
            line = self._get_line(window, slope, value, is_resistance)
            # if len(self.ts) == 170:
            #     print(value)
            #     print(line)
            #     print(slope, intercept)
            #     print(self.close[-1], window[-1], len(window))
            #     print(line[1] + self.length * line[0])
            # если произошел пробой сопротивления
            if is_resistance and self.close[-1] > line[1] + self.length * line[0]:
                # если сигнал был более min_space количества свечей назад
                if self._last_signal_resistance > self.min_space:
                    # обнуляем счетчик
                    print(f"Получен сигнал в лонг, цена закрытия {self.close[-1]}, цена с учетом наклона "
                          f"{line[1] + self.length * line[0]} ({line})")
                    self._last_signal_resistance = 0
                    # возвращаем сигнал
                    return Signal(True, self.close[-1], line)
                # обнуляем счетчик в любом случае
                self._last_signal_resistance = 0
            else:
                # если не было сигнала, то увеличиваем счетчик
                self._last_signal_resistance += 1
            # если произошел пробой поддержки
            if not is_resistance and self.close[-1] < line[1] + self.length * line[0]:
                # если сигнал был более min_space количества свечей назад
                if self._last_signal_support > self.min_space:
                    # обнуляем счетчик
                    self._last_signal_support = 0
                    # возвращаем сигнал
                    return Signal(False, self.close[-1], line)
                # обнуляем счетчик в любом случае
                self._last_signal_support = 0
            else:
                # если не было сигнала, то увеличиваем счетчик
                self._last_signal_support += 1

    # функция для поиска наклонной линии
    def _get_line(self, window, slope, value_index, is_resistance):
        # вычисляем шаг изменения наклона
        slope_step = (window.max() - window.min()) / len(window)
        # инициализируем начальные значения
        step = 1
        min_step = 0.0001
        best_slope = slope
        # вычисляем первоначальное значение тренда
        best_value = self._check_trend(window, slope, value_index, is_resistance)
        # флаг для вычисления производной
        get_der = True
        # переменная для хранения производной
        der = None
        # пока шаг не меньше min_step
        while step > min_step:
            # если нам нужно вычислять производную
            if get_der:
                # изменяем наклон на минимальный шаг
                slope_change = best_slope + slope_step * min_step
                # вычисляем значение еще раз
                test_value = self._check_trend(window, slope_change, value_index, is_resistance)
                # если значение меньше нуля, то меняем наклон
                if test_value < 0:
                    slope_change = best_slope - slope_step * min_step
                    # вычисляем значение еще раз
                    test_value = self._check_trend(window, slope_change, value_index, is_resistance)
                # запоминаем производную
                der = test_value - best_value
                get_der = False
            # в зависимости от знака производной меняем наклон
            if der > 0:
                test_slope = best_slope - slope_step * step
            else:
                test_slope = best_slope + slope_step * step
            # вычисляем значение
            test_value = self._check_trend(window, test_slope, value_index, is_resistance)
            # если значение меньше нуля или не улучшает лучшее значение, то уменьшаем шаг в 2 раза
            if test_value < 0 or test_value >= best_value:
                step *= 0.5
            else:
                # если значение улучшилось, то запоминаем наклон и значение
                best_slope = test_slope
                best_value = test_value
                get_der = True
        # возвращаем лучшее значение и пересечение с линей
        return best_slope, -best_slope * value_index + window[value_index]

    # функция для проверки тренда
    def _check_trend(self, window, slope, value_index, is_resistance):
        # вычисляем пересечение с линей
        intecept = -slope * value_index + window[value_index]
        # получаем все точки наклонки
        line_vals = slope * np.arange(len(window)) + intecept
        # if len(self.ts) == 400:
        #     _open = list(self.open)[-self.length:]
        #     high = list(self.high)[-self.length:]
        #     low = list(self.low)[-self.length:]
        #     close = list(self.close)[-self.length:]
        #     # строим график
        #     x = np.arange(len(window))
        #     fig = go.Figure(data=go.Candlestick(x=x, open=_open, high=high, low=low, close=close))
        #     fig.add_trace(go.Scatter(x=x, y=line_vals, mode='lines',
        #                              line=dict(color='blue', width=2)))
        #     fig.write_image(f"slops/{len(self.ts)}-{is_resistance}-{time.time_ns()}.png")
        # вычисляем разницу между точками наклонки и телом свечей
        diffs = line_vals - window
        # проверяем линию на корректность
        if (not is_resistance and diffs.max() > 0) or (is_resistance and diffs.min() < 0):
            # если линия некорректна, то возвращаем -1
            return -1
        # возвращаем сумму квадратов разниц, которая является мерой отклонения линии тренда
        return (diffs ** 2).sum()