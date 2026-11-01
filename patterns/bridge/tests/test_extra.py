import unittest

from ..bridge_limited_remote import LimitedRemote
from ..remotes import Projector, TV


class LimitedRemoteTests(unittest.TestCase):
    def test_new_remote_works_with_both_device_implementations(self):
        for device_type, expected in ((TV, 55), (Projector, 50)):
            device = device_type()
            remote = LimitedRemote(device, limit=55)
            remote.toggle_power()
            self.assertTrue(device.is_on)
            remote.set_volume(90)
            self.assertEqual(device.volume, expected)
            remote.set_volume(20)
            self.assertEqual(device.volume, 20)
            remote.toggle_power()
            self.assertFalse(device.is_on)

    def test_limit_can_be_zero_or_one_hundred(self):
        for limit in (0, 100):
            device = TV()
            LimitedRemote(device, limit).set_volume(100)
            self.assertEqual(device.volume, limit)

    def test_invalid_command_does_not_change_device(self):
        device = TV()
        remote = LimitedRemote(device)
        for invalid in (-1, 101, float("nan")):
            with self.assertRaises(ValueError):
                remote.set_volume(invalid)
            self.assertEqual(device.volume, 30)
