"""Composite: расчёт текущей мощности устройства, комнаты или дома.

Реализуйте power_usage() в двух классах. Выключенный PowerDevice потребляет 0,
включённый — rated_watts. PowerGroup суммирует мощность непосредственных детей,
вызывая их power_usage(); вложенные группы сами обрабатывают своих потомков.
В этом задании дерево содержит только PowerDevice и PowerGroup.
Включение, выключение и защита дерева уже реализованы в базовых классах.

Из папки паттерна: pytest tests/test_extra.py
"""

from .tree import Device, DeviceGroup


class PowerDevice(Device):
    def __init__(self, name: str, rated_watts: int) -> None:
        super().__init__(name)
        if rated_watts < 0:
            raise ValueError("Мощность не может быть отрицательной")
        self.rated_watts = rated_watts

    def power_usage(self) -> int:
        # TODO: верните мощность с учётом состояния устройства.
        raise NotImplementedError("Реализуйте расчёт мощности устройства")


class PowerGroup(DeviceGroup):
    def power_usage(self) -> int:
        # TODO: используйте общий метод детей; для пустой группы верните 0.
        raise NotImplementedError("Реализуйте рекурсивный расчёт мощности группы")
