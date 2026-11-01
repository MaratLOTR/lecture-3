if __package__:
    from . import tree
else:
    import tree


def demo() -> None:
    print("=== Composite: одна команда для устройства, комнаты или дома ===")
    house = tree.DeviceGroup("Дом")
    room = tree.DeviceGroup("Гостиная")
    room.add(tree.Device("Лампа"))
    room.add(tree.Device("Телевизор"))
    house.add(room)
    house.add(tree.Device("Свет в прихожей"))
    house.turn_on()
    print("После house.turn_on():")
    print("\n".join(house.describe()))
    room.turn_off()
    print("После room.turn_off():")
    print("\n".join(house.describe()))
    build_house = getattr(tree, "build_demo_house", None)
    if build_house is not None:
        print("Дерево из задания:")
        print("\n".join(build_house().describe()))


if __name__ == "__main__":
    demo()
