import unittest

from .. import remotes


class BridgeTaskTests(unittest.TestCase):
    def require(self, name):
        cls = getattr(remotes, name, None)
        self.assertIsNotNone(
            cls, f"САМОСТОЯТЕЛЬНО: добавьте {name} в remotes.py (см. TASK.md)"
        )
        return cls

    def test_radio_works_with_existing_remotes(self):
        radio_type = self.require("Radio")
        self.assertTrue(issubclass(radio_type, remotes.MediaDevice))
        for remote_type in (remotes.Remote, remotes.AdvancedRemote):
            radio = radio_type()
            self.assertFalse(radio.is_on)
            self.assertEqual(radio.volume, 30)
            remote = remote_type(radio)
            remote.toggle_power()
            self.assertTrue(radio.is_on)
            remote.set_volume(37)
            self.assertEqual(radio.volume, 37)
            remote.toggle_power()
            self.assertFalse(radio.is_on)
            if isinstance(remote, remotes.AdvancedRemote):
                remote.mute()
                self.assertEqual(radio.volume, 0)

    def test_radio_validates_volume(self):
        radio = self.require("Radio")()
        for volume in (0, 100):
            radio.set_volume(volume)
            self.assertEqual(radio.volume, volume)
        for volume in (-1, 101):
            with self.assertRaises(ValueError):
                radio.set_volume(volume)
            self.assertEqual(radio.volume, 100)

    def test_presentation_remote_works_with_existing_devices(self):
        remote_type = self.require("PresentationRemote")
        self.assertTrue(issubclass(remote_type, remotes.Remote))
        for device_type in (remotes.TV, remotes.Projector):
            device = device_type()
            remote = remote_type(device)
            remote.set_volume(70)
            remote.start_presentation()
            remote.start_presentation()
            self.assertTrue(device.is_on)
            self.assertEqual(device.volume, 0)
            remote.toggle_power()
            self.assertFalse(device.is_on)

    def test_new_remote_and_new_device_work_together(self):
        radio = self.require("Radio")()
        remote = self.require("PresentationRemote")(radio)
        remote.start_presentation()
        self.assertTrue(radio.is_on)
        self.assertEqual(radio.volume, 0)
