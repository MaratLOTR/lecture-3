"""Composite: дом → этаж → комната → устройство.

Component — Component; Device — Leaf; DeviceGroup — Composite.
Устройства и группы имеют общие команды; только группы хранят детей.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Component(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self._parent: DeviceGroup | None = None

    @abstractmethod
    def turn_on(self) -> None:
        """Включить компонент."""

    @abstractmethod
    def turn_off(self) -> None:
        """Выключить компонент."""

    @abstractmethod
    def describe(self, indent: int = 0) -> list[str]:
        """Вернуть строки для вывода дерева."""


class Device(Component):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.is_on = False

    def turn_on(self) -> None:
        self.is_on = True

    def turn_off(self) -> None:
        self.is_on = False

    def describe(self, indent: int = 0) -> list[str]:
        state = "включено" if self.is_on else "выключено"
        return [f"{'  ' * indent}{self.name}: {state}"]


class DeviceGroup(Component):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._children: list[Component] = []

    @property
    def children(self) -> tuple[Component, ...]:
        return tuple(self._children)

    def add(self, child: Component) -> None:
        if not isinstance(child, Component):
            raise TypeError("В группу можно добавить только Component")
        # Циклы привели бы к бесконечной рекурсии при выполнении команд.
        ancestor: Component | None = self
        while ancestor is not None:
            if ancestor is child:
                raise ValueError("Нельзя добавить группу в саму себя или своего потомка")
            ancestor = ancestor._parent
        if child._parent is not None:
            raise ValueError("Компонент уже в группе; сначала удалите его из неё")
        self._children.append(child)
        child._parent = self

    def remove(self, child: Component) -> None:
        self._children.remove(child)
        child._parent = None

    def turn_on(self) -> None:
        for child in self._children:
            child.turn_on()

    def turn_off(self) -> None:
        for child in self._children:
            child.turn_off()

    def describe(self, indent: int = 0) -> list[str]:
        lines = [f"{'  ' * indent}{self.name}/"]
        for child in self._children:
            lines.extend(child.describe(indent + 1))
        return lines


# ЗАДАНИЕ: реализуйте build_demo_house(), создающую дерево дома через add().
# Не меняйте готовые классы.
# Условия и команды проверки: TASK.md; тесты: tests/test_task.py.
