if __package__:
    from . import devices
else:
    import devices


def demo() -> None:
    print("=== Adapter: разные интерфейсы, одна команда ===")
    light = devices.ModernLight()
    lamp = devices.LegacyLamp()
    object_adapter = devices.LampObjectAdapter(lamp)
    class_adapter = devices.LampClassAdapter()
    switches = [light, object_adapter, class_adapter]
    fan = devices.ForeignFan()
    fan_adapter = getattr(devices, "FanAdapter", None)
    if fan_adapter is not None:
        switches.append(fan_adapter(fan))
    fan_class_adapter_type = getattr(devices, "FanClassAdapter", None)
    fan_class_adapter = None
    if fan_class_adapter_type is not None:
        fan_class_adapter = fan_class_adapter_type()
        switches.append(fan_class_adapter)
    for enabled in (True, False):
        devices.set_all_power(switches, enabled)
        print(
            f"Питание {enabled}: новая лампа={light.is_on}, "
            f"адаптер объекта={lamp.powered}, адаптер класса={class_adapter.powered}"
        )
        if fan_adapter is not None:
            print(f"  Вентилятор: {fan.mode}")
        if fan_class_adapter is not None:
            print(f"  Вентилятор через наследование: {fan_class_adapter.mode}")


if __name__ == "__main__":
    demo()
