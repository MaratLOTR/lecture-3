# UML: Bridge

На GitHub блоки Mermaid отображаются как диаграммы. Для просмотра без интернета
откройте [диаграмму классов](classes.svg), [последовательность вызовов](sequence.svg)
или [HTML-шпаргалку](cheatsheet.html).

[Исходники PlantUML](bridge_uml.puml) пригодятся, если вы уже используете эту нотацию.
Для просмотра этих диаграмм дополнительные инструменты не требуются.

## Диаграмма классов

```mermaid
classDiagram
  direction LR
  Remote --> MediaDevice : device
  Remote <|-- AdvancedRemote
  MediaDevice <|-- TV
  MediaDevice <|-- Projector
  class Remote {
    device: MediaDevice
    toggle_power()
    set_volume(percent)
  }
  class MediaDevice {
    <<abstract>>
    set_power(enabled)
    set_volume(percent)
    volume: int
  }
  class AdvancedRemote {
    mute()
  }
  class TV
  class Projector
```

## Последовательность вызовов

```mermaid
sequenceDiagram
  autonumber
  participant C as Client
  participant R as remote: AdvancedRemote
  participant D as device: TV
  C->>R: mute()
  R->>D: set_volume(0)
```

SVG — готовые локальные изображения, Mermaid и PlantUML — редактируемые UML-исходники.
При изменении структуры кода обновите соответствующие диаграммы во всех трёх форматах.
При изменении кода обновите также примеры в HTML-шпаргалке.
