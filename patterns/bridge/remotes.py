"""Bridge: виды пультов и виды устройств развиваются независимо.

Remote — Abstraction; AdvancedRemote — RefinedAbstraction;
MediaDevice — Implementor; TV, Projector — ConcreteImplementor.
"""

from abc import ABC, abstractmethod


class MediaDevice(ABC):
    def __init__(self) -> None:
        self.is_on = False

    @abstractmethod
    def set_power(self, enabled: bool) -> None:
        """Установить питание."""

    @property
    @abstractmethod
    def volume(self) -> int:
        """Текущая громкость в процентах."""

    @abstractmethod
    def set_volume(self, percent: int) -> None:
        """Установить громкость 0–100; устройство может округлять её вниз."""


class TV(MediaDevice):
    def __init__(self) -> None:
        super().__init__()
        self._volume = 30

    def set_power(self, enabled: bool) -> None:
        self.is_on = enabled

    @property
    def volume(self) -> int:
        return self._volume

    def set_volume(self, percent: int) -> None:
        if not 0 <= percent <= 100:
            raise ValueError("Громкость должна быть от 0 до 100")
        self._volume = percent


class Projector(MediaDevice):
    def __init__(self) -> None:
        super().__init__()
        self._volume_steps = 3

    def set_power(self, enabled: bool) -> None:
        self.is_on = enabled

    @property
    def volume(self) -> int:
        return self._volume_steps * 10

    def set_volume(self, percent: int) -> None:
        if not 0 <= percent <= 100:
            raise ValueError("Громкость должна быть от 0 до 100")
        self._volume_steps = percent // 10


class Remote:
    def __init__(self, device: MediaDevice) -> None:
        self.device = device

    def toggle_power(self) -> None:
        self.device.set_power(not self.device.is_on)

    def set_volume(self, percent: int) -> None:
        self.device.set_volume(percent)


class AdvancedRemote(Remote):
    def mute(self) -> None:
        self.device.set_volume(0)


# САМОСТОЯТЕЛЬНОЕ ЗАДАНИЕ: реализуйте Radio с интерфейсом MediaDevice
# и PresentationRemote с методом start_presentation().
# Не меняйте существующие пульты и устройства.
# Условия и команды проверки: TASK.md; тесты: tests/test_task.py.
