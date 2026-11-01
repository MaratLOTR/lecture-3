# Структурные паттерны на примере умного дома

Учебный проект на Python по презентации «Лекция 3»: **Adapter, Facade, Composite**.
**Bridge** — дополнительный материал для самостоятельного изучения, как указано в плане лекции.
Все устройства имитируются в памяти. Нужен Python 3.10+ и pytest 9+ для тестов.
Сами примеры используют только стандартную библиотеку Python.

## Запуск в GitHub Codespaces

1. Загрузите содержимое `smart_home_patterns` в корень своего репозитория GitHub.
   В корне должны лежать `main.py`, `patterns/`, `.devcontainer/` и `.vscode/`.
   При загрузке через файловый менеджер проверьте, что скрытые папки тоже добавлены.
2. В репозитории нажмите **Code → Codespaces → Create codespace on main**
   (или на выбранной ветке) и дождитесь открытия редактора.
3. Откройте **Terminal → New Terminal** и выполните:

```bash
python3 main.py
python3 -m patterns.adapter
```

Проверки готового примера и задания Adapter запускаются отдельно:

```bash
pytest patterns/adapter/tests/test_example.py
pytest patterns/adapter/tests/test_task.py
```

Для остальных разделов замените `adapter` на `facade`, `composite` или `bridge`.
Команды запуска внутри отдельной папки паттерна также работают в терминале Codespaces.

[.devcontainer/devcontainer.json](.devcontainer/devcontainer.json) задаёт готовое
окружение с Python 3.11 и установку pytest из [requirements.txt](requirements.txt)
при создании Codespaces. Собственный `Dockerfile` не нужен.
Если Codespaces уже был создан до добавления конфигурации, примените её командой
**Codespaces: Rebuild Container** в палитре команд редактора.

[.vscode/settings.json](.vscode/settings.json) настраивает `pytest` для панели
**Testing** при наличии расширения Python. Здесь тесты сгруппированы по папкам
паттернов; в список входят примеры, основные и дополнительные задания.
До выполнения заданий часть проверок будет красной. Запуск через терминал работает
независимо от панели Testing.

Для локального запуска сначала подготовьте отдельное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

В Windows активируйте окружение командой `.venv\Scripts\Activate.ps1` в PowerShell.
В Codespaces этот шаг не нужен: pytest устанавливается при создании окружения.
Версия pytest 9+ нужна для поддержки `subTest` в существующих проверках `TestCase`.
Их условия сохранены; запуск и отчёты выполняет pytest.

Окружение задаётся для репозитория целиком: копировать `.devcontainer` в папку
каждого паттерна внутри этого репозитория не нужно.

Справка: [создание Codespaces](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository),
[настройка окружения](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers).

## Папка одного паттерна

Откройте нужную папку: внутри находятся теория, общий код по теме, пример из лекции,
демонстрация, задание и тесты. Её можно скопировать и передать студенту отдельно.

| Раздел | Пример | Задание |
|---|---|---|
| [Adapter](patterns/adapter/README.md) | `LampObjectAdapter` и `LampClassAdapter`: композиция и наследование | [Два адаптера вентилятора](patterns/adapter/TASK.md), слайд 19 |
| [Facade](patterns/facade/README.md) | `HomeFacade.start_movie()`, четыре подсистемы | [Сценарий «Ушёл из дома»](patterns/facade/TASK.md), слайд 29 |
| [Composite](patterns/composite/README.md) | `Component`, `Device`, `DeviceGroup` | [Дерево дома](patterns/composite/TASK.md), слайд 43 |
| [Bridge — самостоятельно](patterns/bridge/README.md) | Независимое развитие пультов и устройств | [Радио и пульт для презентации](patterns/bridge/TASK.md) |

Номера слайдов — фактический порядок в приложенном файле. В презентации код местами
сокращён до `...`; здесь методы дополнены рабочими реализациями. В Composite сохранены
вывод дерева, удаление элементов и защита от циклов, опущенные на слайдах.
У клиента Adapter используется функция `set_all_power()` с `Iterable[Switchable]`;
это тот же алгоритм обхода, что и на слайдах. Старое имя `LegacyLampAdapter`
сохранено для совместимости с уже написанными примерами.

```text
patterns/<паттерн>/
  README.md                    теория, роли, пример и команды запуска
  devices.py / home.py /       общий код темы и работающий пример
  tree.py / remotes.py         (один из этих файлов на паттерн)
  __main__.py                  демонстрация
  TASK.md                     задание из лекции, условия и проверка
  tests/
    test_example.py            тесты готового примера
    test_task.py               тесты задания
    test_extra.py              тесты дополнительной практики
  <дополнительное задание>.py   заготовка с TODO
  docs/                        UML и HTML-шпаргалка
```

## Запуск из папки паттерна

Например, откройте терминал в `patterns/adapter`:

```bash
python3 __main__.py
pytest tests/test_example.py
pytest tests/test_task.py
```

Эти же команды действуют в `facade`, `composite` и `bridge`.
В Windows вместо `python3` можно использовать `py -3`.

Готовые примеры проходят сразу. Задания намеренно оставлены студенту:
найдите комментарий `ЗАДАНИЕ` в основном файле и реализуйте контракт из `TASK.md`.
Проверки задания **падают до его выполнения**, без `skipped`. Успех означает,
что все тесты завершились `PASSED`. Тесты менять не нужно.
Демонстрация автоматически подхватит добавленные классы, метод или функцию.

Дополнительные задания находятся в той же папке: термостат °C/°F, ночной режим,
мощность дерева устройств и пульт с ограничением громкости. Они расширяют практику
и не заменяют задания из лекции. Контракт записан в начале каждой заготовки.

```bash
pytest tests/test_extra.py
```

До реализации TODO эти отдельные проверки падают с `NotImplementedError`.

## Запуск из корня проекта

```bash
python3 main.py
python3 main.py --bridge
```

Проверить все готовые примеры и генератор HTML, без студенческих заданий:

```bash
pytest patterns/*/tests/test_example.py tests/test_cheatsheets.py
```

Проверить один паттерн целиком, включая его основное и дополнительное задания:

```bash
pytest patterns/adapter/tests
pytest patterns/facade/tests
pytest patterns/composite/tests
pytest patterns/bridge/tests
```

Все проверки проекта:

```bash
pytest
```

[pytest.ini](pytest.ini) собирает тесты из папок паттернов и проверки HTML.
До выполнения основных и дополнительных заданий часть тестов завершается `FAILED`.
`PASSED` означает, что проверка прошла. Папки `tests/` и `exercises/` в корне
содержат совместимые импорты; они исключены из повторного автоматического сбора,
чтобы одни проверки не выполнялись дважды. Редактируйте код и тесты внутри
`patterns/<паттерн>/`. Дополнительная практика описана в [exercises/README.md](exercises/README.md).

## UML и HTML-шпаргалки

| Паттерн | UML | Теория, код, задания и тесты в HTML |
|---|---|---|
| Adapter | [Диаграммы](patterns/adapter/docs/diagrams.md) | [Открыть HTML](patterns/adapter/docs/cheatsheet.html) |
| Facade | [Диаграммы](patterns/facade/docs/diagrams.md) | [Открыть HTML](patterns/facade/docs/cheatsheet.html) |
| Composite | [Диаграммы](patterns/composite/docs/diagrams.md) | [Открыть HTML](patterns/composite/docs/cheatsheet.html) |
| Bridge | [Диаграммы](patterns/bridge/docs/diagrams.md) | [Открыть HTML](patterns/bridge/docs/cheatsheet.html) |

HTML открывается без интернета; код и SVG встроены в страницу. Для переходов к другим
разделам нужна папка проекта целиком. Рядом лежат редактируемые Mermaid и PlantUML.
После изменения README, TASK.md, кода, тестов или SVG пересоберите HTML:

```bash
python3 tools/build_cheatsheets.py
```
