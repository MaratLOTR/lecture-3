"""Facade: один вызов настраивает подсистемы для просмотра фильма.

HomeFacade — Facade; Lighting, Curtains, Projector, SoundSystem — подсистемы.
Подсистемы не знают о фасаде и доступны клиенту напрямую.
"""


class Lighting:
    def __init__(self) -> None:
        self.brightness = 100

    def set_brightness(self, percent: int) -> None:
        if not 0 <= percent <= 100:
            raise ValueError("Яркость должна быть от 0 до 100")
        self.brightness = percent


class Curtains:
    def __init__(self) -> None:
        self.is_closed = False

    def close(self) -> None:
        self.is_closed = True

    def open(self) -> None:
        self.is_closed = False


class Projector:
    def __init__(self) -> None:
        self.is_on = False
        self.source: str | None = None

    def turn_on(self, source: str) -> None:
        self.source = source
        self.is_on = True

    def turn_off(self) -> None:
        self.is_on = False
        self.source = None


class SoundSystem:
    def __init__(self) -> None:
        self.is_on = False
        self.volume = 0

    def turn_on(self, volume: int) -> None:
        if not 0 <= volume <= 100:
            raise ValueError("Громкость должна быть от 0 до 100")
        self.volume = volume
        self.is_on = True

    def turn_off(self) -> None:
        self.is_on = False
        self.volume = 0


class HomeFacade:
    def __init__(
        self,
        lighting: Lighting,
        curtains: Curtains,
        projector: Projector,
        sound: SoundSystem,
    ) -> None:
        self.lighting = lighting
        self.curtains = curtains
        self.projector = projector
        self.sound = sound

    def start_movie(self) -> None:
        self.curtains.close()
        self.lighting.set_brightness(20)
        self.projector.turn_on("HDMI 1")
        self.sound.turn_on(35)

    def end_movie(self) -> None:
        self.projector.turn_off()
        self.sound.turn_off()
        self.lighting.set_brightness(100)
        self.curtains.open()

    # ЗАДАНИЕ: реализуйте HomeFacade.leave_home() — сценарий «Ушёл из дома».
    # Используйте публичные методы подсистем.
    # Условия и команды проверки: TASK.md; тесты: tests/test_task.py.
