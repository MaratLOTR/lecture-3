"""Adapter: клиент управляет новой и старой лампами через один интерфейс.

Switchable — Target; LegacyLamp — Adaptee;
LampObjectAdapter, LampClassAdapter — Adapter; set_all_power — Client.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable


class Switchable(ABC):
    @abstractmethod
    def set_power(self, enabled: bool) -> None:
        """Установить питание устройства."""


class ModernLight(Switchable):
    def __init__(self) -> None:
        self.is_on = False

    def set_power(self, enabled: bool) -> None:
        self.is_on = enabled


class LegacyLamp:
    """Имитирует готовую стороннюю библиотеку; её интерфейс не меняем."""

    def __init__(self) -> None:
        self.powered = False

    def switch_on(self) -> None:
        self.powered = True

    def switch_off(self) -> None:
        self.powered = False


class LampObjectAdapter(Switchable):
    def __init__(self, lamp: LegacyLamp) -> None:
        self.lamp = lamp

    def set_power(self, enabled: bool) -> None:
        if enabled:
            self.lamp.switch_on()
        else:
            self.lamp.switch_off()


class LampClassAdapter(Switchable, LegacyLamp):
    def __init__(self) -> None:
        LegacyLamp.__init__(self)

    def set_power(self, enabled: bool) -> None:
        if enabled:
            self.switch_on()
        else:
            self.switch_off()


# Сохраняем прежнее имя для уже написанных примеров.
LegacyLampAdapter = LampObjectAdapter


def set_all_power(devices: Iterable[Switchable], enabled: bool) -> None:
    """Клиенту не нужно знать конкретные классы и старые методы."""
    for device in devices:
        device.set_power(enabled)


class ForeignFan:
    """Ещё один сторонний API, который предстоит адаптировать."""

    def __init__(self) -> None:
        self.mode = "STOP"

    def set_mode(self, mode: str) -> None:
        if mode not in ("RUN", "STOP"):
            raise ValueError("Допустимые режимы: RUN и STOP")
        self.mode = mode


# ЗАДАНИЕ (слайд 19): добавьте FanAdapter(Switchable), хранящий self.fan,
# и FanClassAdapter(Switchable, ForeignFan), наследующий готовый API.
# Оба переводят set_power(True) в set_mode("RUN"), False — в set_mode("STOP").
# Не меняйте ForeignFan и клиентскую функцию set_all_power.
# Условия и команды проверки: TASK.md; тесты: tests/test_task.py.
