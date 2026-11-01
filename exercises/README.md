# Дополнительные задания

Заготовки и их тесты находятся внутри папки соответствующего паттерна.
Эти задания расширяют практику; основные задания из лекции описаны в `TASK.md` рядом с примером.

| Паттерн | Заготовка | Тесты |
|---|---|---|
| Adapter | [Термостат °C/°F](../patterns/adapter/adapter_thermostat.py) | [test_extra.py](../patterns/adapter/tests/test_extra.py) |
| Facade | [Ночной режим](../patterns/facade/facade_night_mode.py) | [test_extra.py](../patterns/facade/tests/test_extra.py) |
| Composite | [Мощность дерева](../patterns/composite/composite_power_usage.py) | [test_extra.py](../patterns/composite/tests/test_extra.py) |
| Bridge — самостоятельно | [Ограничение громкости](../patterns/bridge/bridge_limited_remote.py) | [test_extra.py](../patterns/bridge/tests/test_extra.py) |

Допишите методы с TODO, убрав `NotImplementedError`. Полный контракт — в начале заготовки.
Из папки выбранного паттерна:

```bash
pytest tests/test_extra.py
```

Из корня проекта можно проверить одно или все дополнительные задания:

```bash
pytest patterns/adapter/tests/test_extra.py
pytest patterns/facade/tests/test_extra.py
pytest patterns/composite/tests/test_extra.py
pytest patterns/bridge/tests/test_extra.py
pytest patterns/*/tests/test_extra.py
```

До выполнения TODO тесты падают; задание выполнено, когда все его проверки завершаются `PASSED`.
В этой папке оставлены совместимые импорты: вносите решения в файлы внутри `patterns/`.
