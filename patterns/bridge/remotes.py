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


# САМОСТОЯТЕЛЬНОЕ ЗАДАНИЕ:
# 1. Добавьте Radio(MediaDevice): начальная громкость 30, питание выключено.
#    Громкость хранится точно в процентах; за пределами 0–100 — ValueError.
# 2. Добавьте PresentationRemote(Remote) с start_presentation():
#    включить переданное устройство и установить громкость 0.
# 3. Проверьте новый пульт со всеми устройствами, а Radio — со всеми пультами.
#    Существующие классы пультов и устройств изменять не нужно.
# Условия и команды проверки: TASK.md; тесты: tests/test_task.py.
