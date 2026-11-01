# Задание: адаптеры вентилятора

**Fan** по-английски — **вентилятор**. Готовый класс `ForeignFan` управляет им
через `set_mode("RUN")` — включить и `set_mode("STOP")` — выключить.
Клиент `set_all_power()` ожидает метод `set_power(True/False)`.

В [devices.py](devices.py) добавьте два класса:

1. `FanAdapter(Switchable)` принимает `ForeignFan` в конструкторе и хранит его
   в `self.fan`. Метод `set_power()` вызывает `self.fan.set_mode()`.
2. `FanClassAdapter(Switchable, ForeignFan)` наследует вентилятор.
   Конструктор без аргументов инициализирует его в режиме `"STOP"`.
   Метод `set_power()` вызывает унаследованный `self.set_mode()`.

Оба адаптера переводят `True` в `"RUN"`, а `False` — в `"STOP"`.
Не меняйте готовые классы, `set_all_power()` и тесты. Поле `mode` напрямую не изменяйте.
Оба адаптера должны работать через `set_all_power()` вместе с лампами.

Из этой папки запустите проверку — все тесты должны пройти:

```bash
pytest tests/test_task.py
```
