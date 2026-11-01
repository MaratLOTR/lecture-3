"""Adapter: приложение использует °C, сторонний термостат — °F.

Реализуйте два метода ThermostatAdapter, не меняя ForeignThermostat.
Формулы: C = (F - 32) * 5 / 9; F = C * 9 / 5 + 32.
Допустимая температура: 10–30 °C. Недопустимое значение вызывает ValueError
и не изменяет состояние термостата. Не округляйте промежуточный результат.

Из папки паттерна: pytest tests/test_extra.py
"""

from abc import ABC, abstractmethod


class TemperatureControl(ABC):
    @abstractmethod
    def get_celsius(self) -> float:
        """Прочитать температуру в °C."""

    @abstractmethod
    def set_celsius(self, temperature: float) -> None:
        """Установить температуру в °C."""


class ForeignThermostat:
    """Готовый сторонний API; менять не нужно."""

    def __init__(self) -> None:
        self._fahrenheit = 68.0

    def read_fahrenheit(self) -> float:
        return self._fahrenheit

    def write_fahrenheit(self, temperature: float) -> None:
        if not 50 <= temperature <= 86:
            raise ValueError("Температура должна быть от 50 до 86 °F")
        self._fahrenheit = temperature


class ThermostatAdapter(TemperatureControl):
    def __init__(self, thermostat: ForeignThermostat) -> None:
        self.thermostat = thermostat

    def get_celsius(self) -> float:
        # TODO: прочитайте температуру через сторонний API и переведите в °C.
        raise NotImplementedError("Реализуйте чтение температуры через адаптер")

    def set_celsius(self, temperature: float) -> None:
        # TODO: проверьте диапазон и передайте значение в °F стороннему API.
        raise NotImplementedError("Реализуйте установку температуры через адаптер")
