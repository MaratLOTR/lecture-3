if __package__:
    from .home import Curtains, HomeFacade, Lighting, Projector, SoundSystem
else:
    from home import Curtains, HomeFacade, Lighting, Projector, SoundSystem


def demo() -> None:
    print("=== Facade: один вызов вместо настройки четырёх подсистем ===")
    lighting, curtains = Lighting(), Curtains()
    home = HomeFacade(lighting, curtains, Projector(), SoundSystem())
    home.start_movie()
    print(
        f"Кино: свет={home.lighting.brightness}%, шторы закрыты={home.curtains.is_closed}, "
        f"проектор={home.projector.source}, звук={home.sound.volume}%"
    )
    lighting.set_brightness(70)
    print(f"Прямой вызов подсистемы: свет={lighting.brightness}%")
    home.end_movie()
    print(f"Фильм окончен: свет={home.lighting.brightness}%, проектор={home.projector.is_on}")
    leave_home = getattr(home, "leave_home", None)
    if leave_home is not None:
        leave_home()
        print(f"Ушли из дома: свет={home.lighting.brightness}%, шторы закрыты={home.curtains.is_closed}")


if __name__ == "__main__":
    demo()
