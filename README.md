# Структурные паттерны: умный дом

Каждая папка паттерна содержит теорию, код примера, демонстрацию, задание и его тесты.
Папки независимы: любую можно скопировать и изучать отдельно.

| Паттерн | Материалы |
|---|---|
| Adapter — Адаптер | [patterns/adapter](patterns/adapter/README.md) |
| Facade — Фасад | [patterns/facade](patterns/facade/README.md) |
| Composite — Компоновщик | [patterns/composite](patterns/composite/README.md) |
| Bridge — Мост, самостоятельно | [patterns/bridge](patterns/bridge/README.md) |

## Запуск в GitHub Codespaces

Нажмите **Code → Codespaces → Create codespace on main**.
Окружение использует Python 3.11 и устанавливает pytest из `requirements.txt`.
Откройте терминал и перейдите в папку нужного паттерна:

```bash
cd patterns/adapter
python3 __main__.py
pytest tests/test_example.py
pytest tests/test_task.py
```

В `facade`, `composite` и `bridge` команды такие же.
Для дополнительной практики выполните `pytest tests/test_extra.py`.
`pytest` внутри папки запускает все тесты этого паттерна.

Готовые примеры проходят сразу. Тесты заданий завершаются `FAILED`, пока студент
не реализует требования из `TASK.md`. Успех — все проверки `PASSED`, без пропусков.

В корне оставлены только навигация и общие настройки Codespaces, редактора и pytest.
Общего запускающего кода и общих заданий нет.
Для локальной работы нужны Python 3.10+ и pytest 9+; код примеров использует стандартную библиотеку.
