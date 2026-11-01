"""Bridge — самостоятельно: пульт с ограничением громкости.

Реализуйте LimitedRemote.set_volume(): допустимы команды 0–100,
но устройству передаётся не больше limit. Некорректная команда вызывает
ValueError и не изменяет громкость. Пульт не проверяет конкретный тип устройства.
TV и Projector из готового примера менять нельзя.

Из папки паттерна: pytest tests/test_extra.py
"""

from .remotes import MediaDevice, Remote


class LimitedRemote(Remote):
    def __init__(self, device: MediaDevice, limit: int = 40) -> None:
        super().__init__(device)
        if not 0 <= limit <= 100:
            raise ValueError("Ограничение должно быть от 0 до 100")
        self.limit = limit

    def set_volume(self, percent: int) -> None:
        # TODO: проверьте команду, ограничьте значение и делегируйте устройству.
        raise NotImplementedError("Реализуйте ограничение громкости на стороне пультов")
