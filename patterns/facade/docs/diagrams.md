# UML: Facade

На GitHub блоки Mermaid отображаются как диаграммы. Для просмотра без интернета
откройте [диаграмму классов](classes.svg), [последовательность вызовов](sequence.svg)
или [HTML-шпаргалку](cheatsheet.html).

[Исходники PlantUML](facade_uml.puml) пригодятся, если вы уже используете эту нотацию.
Для просмотра этих диаграмм дополнительные инструменты не требуются.

## Диаграмма классов

```mermaid
classDiagram
  direction LR
  Client --> HomeFacade
  HomeFacade --> Curtains
  HomeFacade --> Lighting
  HomeFacade --> Projector
  HomeFacade --> SoundSystem
  class Client {
    home.start_movie()
  }
  class HomeFacade {
    start_movie()
    end_movie()
  }
  class Curtains {
    close()
    open()
  }
  class Lighting {
    set_brightness(percent)
  }
  class Projector {
    turn_on(source)
    turn_off()
  }
  class SoundSystem {
    turn_on(volume)
    turn_off()
  }
```

## Последовательность вызовов

```mermaid
sequenceDiagram
  autonumber
  participant C as Client
  participant H as home: HomeFacade
  participant S as curtains: Curtains
  participant L as light: Lighting
  participant P as projector: Projector
  participant A as sound: SoundSystem
  C->>H: start_movie()
  H->>S: close()
  H->>L: set_brightness(20)
  H->>P: turn_on("HDMI 1")
  H->>A: turn_on(35)
```

SVG — готовые локальные изображения, Mermaid и PlantUML — редактируемые UML-исходники.
При изменении структуры кода обновите соответствующие диаграммы во всех трёх форматах.
При изменении кода обновите также примеры в HTML-шпаргалке.
