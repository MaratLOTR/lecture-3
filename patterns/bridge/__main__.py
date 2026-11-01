if __package__:
    from . import remotes
else:
    import remotes


def demo() -> None:
    print("=== Bridge (самостоятельно): виды пультов × виды устройств ===")
    device_types = [remotes.TV, remotes.Projector]
    remote_types = [remotes.Remote, remotes.AdvancedRemote]
    radio = getattr(remotes, "Radio", None)
    presentation_remote = getattr(remotes, "PresentationRemote", None)
    if radio is not None:
        device_types.append(radio)
    if presentation_remote is not None:
        remote_types.append(presentation_remote)
    for device_type in device_types:
        for remote_type in remote_types:
            device = device_type()
            remote = remote_type(device)
            remote.toggle_power()
            remote.set_volume(37)
            print(f"{remote_type.__name__} + {device_type.__name__}: питание={device.is_on}, звук={device.volume}%")
            if isinstance(remote, remotes.AdvancedRemote):
                remote.mute()
                print(f"  mute(): звук={device.volume}%")
            if presentation_remote is not None and isinstance(remote, presentation_remote):
                remote.start_presentation()
                print(f"  start_presentation(): питание={device.is_on}, звук={device.volume}%")


if __name__ == "__main__":
    demo()
