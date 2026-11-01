# UML: Adapter

На GitHub блоки Mermaid отображаются как диаграммы. Для просмотра без интернета
откройте [диаграмму классов](classes.svg), [последовательность вызовов](sequence.svg)
или [HTML-шпаргалку](cheatsheet.html).

[Исходники PlantUML](adapter_uml.puml) пригодятся, если вы уже используете эту нотацию.
Для просмотра этих диаграмм дополнительные инструменты не требуются.

## Диаграмма классов

```mermaid
classDiagram
  direction LR
  Switchable <|-- ModernLight
  Switchable <|-- LampObjectAdapter
  Switchable <|-- LampClassAdapter
  LegacyLamp <|-- LampClassAdapter
  LampObjectAdapter --> LegacyLamp : lamp
  Client --> Switchable
  class Switchable {
    <<abstract>>
    set_power(enabled)
  }
  class Client {
    set_all_power()
  }
  class ModernLight {
    set_power(enabled)
  }
  class LampObjectAdapter {
    lamp: LegacyLamp
    set_power(enabled)
  }
  class LampClassAdapter {
    set_power(enabled)
  }
  class LegacyLamp {
    switch_on()
    switch_off()
  }
```

SVG последовательности показывает адаптер объекта; Mermaid ниже сопоставляет оба варианта.

## Последовательность вызовов

```mermaid
sequenceDiagram
  autonumber
  participant C as Client
  participant A as LampObjectAdapter
  participant L as LegacyLamp
  C->>A: set_power(True)
  A->>L: switch_on()
  C->>A: set_power(False)
  A->>L: switch_off()
  participant K as LampClassAdapter
  C->>K: set_power(True)
  K->>K: switch_on()
  C->>K: set_power(False)
  K->>K: switch_off()
```

SVG — готовые локальные изображения, Mermaid и PlantUML — редактируемые UML-исходники.
При изменении структуры кода обновите соответствующие диаграммы во всех трёх форматах,
затем пересоберите HTML командой `python3 tools/build_cheatsheets.py` из корня проекта.
