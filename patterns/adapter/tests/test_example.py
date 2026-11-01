import unittest
from unittest.mock import patch

from .. import devices


class AdapterTests(unittest.TestCase):
    def test_same_client_controls_modern_and_legacy_lights(self):
        light = devices.ModernLight()
        lamp = devices.LegacyLamp()
        adapter = devices.LampObjectAdapter(lamp)
        self.assertIs(adapter.lamp, lamp)
        for enabled in (True, False, False, True):
            devices.set_all_power([light, adapter], enabled)
            self.assertEqual(light.is_on, enabled)
            self.assertEqual(lamp.powered, enabled)

    def test_adapter_delegates_to_legacy_api(self):
        lamp = devices.LegacyLamp()
        adapter = devices.LampObjectAdapter(lamp)
        with patch.object(lamp, "switch_on", wraps=lamp.switch_on) as on:
            adapter.set_power(True)
            on.assert_called_once_with()
        with patch.object(lamp, "switch_off", wraps=lamp.switch_off) as off:
            adapter.set_power(False)
            off.assert_called_once_with()

    def test_foreign_fan_rejects_unknown_mode(self):
        fan = devices.ForeignFan()
        with self.assertRaises(ValueError):
            fan.set_mode("FAST")
        self.assertEqual(fan.mode, "STOP")

    def test_class_adapter_implements_both_interfaces(self):
        adapter = devices.LampClassAdapter()
        self.assertIsInstance(adapter, devices.Switchable)
        self.assertIsInstance(adapter, devices.LegacyLamp)
        self.assertFalse(adapter.powered)
        adapter.switch_on()
        self.assertTrue(adapter.powered)
        adapter.switch_off()
        self.assertFalse(adapter.powered)
        light = devices.ModernLight()
        lamp = devices.LegacyLamp()
        for enabled in (True, True, False, False, True):
            devices.set_all_power([light, devices.LampObjectAdapter(lamp), adapter], enabled)
            self.assertEqual((light.is_on, lamp.powered, adapter.powered), (enabled,) * 3)

    def test_class_adapter_uses_inherited_api(self):
        adapter = devices.LampClassAdapter()
        for enabled, method in ((True, "switch_on"), (False, "switch_off")):
            with self.subTest(enabled=enabled):
                with patch.object(adapter, method, wraps=getattr(adapter, method)) as call:
                    adapter.set_power(enabled)
                    call.assert_called_once_with()

