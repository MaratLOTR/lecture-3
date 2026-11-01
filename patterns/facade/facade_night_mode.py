"""Facade: подготовка дома ко сну одним вызовом.

Реализуйте NightModeFacade.start(): яркость 10%, шторы закрыты,
проектор и звук выключены. Используйте публичные методы подсистем.
Сценарий должен работать из любого их состояния и при повторном вызове.

Из папки паттерна: pytest tests/test_extra.py
"""

from .home import Curtains, Lighting, Projector, SoundSystem


class NightModeFacade:
    def __init__(
        self, lighting: Lighting, curtains: Curtains,
        projector: Projector, sound: SoundSystem,
    ) -> None:
        self.lighting = lighting
        self.curtains = curtains
        self.projector = projector
        self.sound = sound

    def start(self) -> None:
        # TODO: настройте четыре подсистемы, не присваивая их полям значения напрямую.
        raise NotImplementedError("Реализуйте ночной сценарий фасада")
