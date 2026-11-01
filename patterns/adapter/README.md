# Adapter — Адаптер

## Проблема

Приложение управляет приборами через `set_power(enabled)`. `ModernLight` уже
поддерживает этот интерфейс. Готовая `LegacyLamp` предоставляет только
`switch_on()` и `switch_off()`. Если передать её клиенту напрямую, получим
`AttributeError`: у старой лампы нет `set_power()`.

Adapter преобразует готовый интерфейс в тот, которого ожидает клиент.
Старую библиотеку и общий алгоритм управления менять не требуется.

## Два варианта из лекции

| Различие | Адаптер объекта | Адаптер класса |
|---|---|---|
| Класс | `LampObjectAdapter(Switchable)` | `LampClassAdapter(Switchable, LegacyLamp)` |
| Связь с лампой | Хранит `self.lamp` | Наследует `LegacyLamp` |
| Состояние | В переданном экземпляре | В самом адаптере, поле `powered` |
| Включение | `self.lamp.switch_on()` | `self.switch_on()` |
| Готовый экземпляр | Можно обернуть | Создаёт собственное состояние |

Адаптер класса явно вызывает `LegacyLamp.__init__(self)`. Он предоставляет
и унаследованные `switch_on()` / `switch_off()`, и новый `set_power()`.
Адаптер объекта делегирует команды одному и тому же переданному объекту.

| Роль | Класс или функция |
|---|---|
| Target — ожидаемый контракт | `Switchable.set_power(enabled)` |
| Adaptee — готовый несовместимый API | `LegacyLamp` |
| Adapter — перевод интерфейсов | `LampObjectAdapter`, `LampClassAdapter` |
| Client — общий алгоритм | `set_all_power()` |
| Изначально совместимое устройство | `ModernLight` |

```python
lamp = LegacyLamp()
object_adapter = LampObjectAdapter(lamp)
class_adapter = LampClassAdapter()
devices = [ModernLight(), object_adapter, class_adapter]
set_all_power(devices, True)
assert lamp.powered is True
assert class_adapter.powered is True
set_all_power(devices, False)
```

## Код и запуск

- [devices.py](devices.py) — контракт, устройства, оба адаптера и общий клиент.
- [__main__.py](__main__.py) — включение и выключение всех вариантов одним клиентом.
- [TASK.md](TASK.md) — задание: два адаптера вентилятора (`fan` — вентилятор).
- [tests/test_example.py](tests/test_example.py) — проверки готового примера.
- [tests/test_task.py](tests/test_task.py) — проверки задания.

Все материалы находятся в этой папке; её можно передать студенту отдельно.
Нужен Python 3.10+ и pytest 9+. В Codespaces pytest устанавливается автоматически. Из этой папки:

```bash
python3 __main__.py
pytest tests/test_example.py
pytest tests/test_task.py
```

Готовый пример проходит сразу. Проверки задания дают `FAILED`, пока требуемые классы
не реализованы. Успех — все проверки `PASSED`, без пропусков.

## Применимость и ограничения

Adapter нужен при подключении стороннего или устаревшего API. Он позволяет
повторно использовать код и изолировать особенности этого API от клиента.
Цена — дополнительные классы и делегирование; изменение API потребует проверки
адаптера. Для простого случая отдельный класс может оказаться избыточным.
Адаптация должна сохранять смысл операций, даже если различаются единицы измерения.

**Вопрос:** какой вариант позволяет подключить уже созданный экземпляр лампы и почему?

## Дополнительные материалы

- [UML: классы и последовательность вызовов](docs/diagrams.md).
- [HTML-шпаргалка с теорией, кодом, заданиями и тестами](docs/cheatsheet.html).
