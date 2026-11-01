# UML: Composite

На GitHub блоки Mermaid отображаются как диаграммы. Для просмотра без интернета
откройте [диаграмму классов](classes.svg), [последовательность вызовов](sequence.svg)
или [HTML-шпаргалку](cheatsheet.html).

[Исходники PlantUML](composite_uml.puml) пригодятся, если вы уже используете эту нотацию.
Для просмотра этих диаграмм дополнительные инструменты не требуются.

## Диаграмма классов

```mermaid
classDiagram
  direction LR
  Component <|-- Device
  Component <|-- DeviceGroup
  DeviceGroup o-- Component : children
  class Component {
    <<abstract>>
    turn_on()
    turn_off()
    describe()
  }
  class Device {
    is_on: bool
    turn_on()
    turn_off()
  }
  class DeviceGroup {
    add(child)
    remove(child)
    turn_on()
    turn_off()
  }
```

## Последовательность вызовов

```mermaid
sequenceDiagram
  autonumber
  participant C as Client
  participant H as house: DeviceGroup
  participant R as room: DeviceGroup
  participant L as lamp: Device
  participant T as tv: Device
  C->>H: turn_off()
  H->>R: turn_off()
  R->>L: turn_off()
  R->>T: turn_off()
```

SVG — готовые локальные изображения, Mermaid и PlantUML — редактируемые UML-исходники.
При изменении структуры кода обновите соответствующие диаграммы во всех трёх форматах.
При изменении кода обновите также примеры в HTML-шпаргалке.
