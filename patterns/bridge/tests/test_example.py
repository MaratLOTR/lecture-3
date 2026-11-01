import unittest

from .. import remotes


class BridgeTests(unittest.TestCase):
    def test_all_remote_and_device_combinations(self):
        for remote_type in (remotes.Remote, remotes.AdvancedRemote):
            for device_type in (remotes.TV, remotes.Projector):
                with self.subTest(remote=remote_type.__name__, device=device_type.__name__):
                    device = device_type()
                    remote = remote_type(device)
                    self.assertIs(remote.device, device)
                    self.assertFalse(device.is_on)
                    remote.toggle_power()
                    self.assertTrue(device.is_on)
                    remote.set_volume(37)
                    self.assertEqual(device.volume, 37 if device_type is remotes.TV else 30)
                    remote.toggle_power()
                    self.assertFalse(device.is_on)

    def test_mute_works_with_every_implementation(self):
        for device_type in (remotes.TV, remotes.Projector):
            device = device_type()
            remote = remotes.AdvancedRemote(device)
            remote.toggle_power()
            remote.set_volume(80)
            remote.mute()
            self.assertEqual(device.volume, 0)
            self.assertTrue(device.is_on)

    def test_devices_check_volume_bounds(self):
        for device_type in (remotes.TV, remotes.Projector):
            device = device_type()
            for volume in (0, 100):
                device.set_volume(volume)
                self.assertEqual(device.volume, volume)
            for volume in (-1, 101):
                with self.assertRaises(ValueError):
                    device.set_volume(volume)
                self.assertEqual(device.volume, 100)

