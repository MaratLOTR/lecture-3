import unittest
from unittest.mock import call, patch

from .. import devices


class FanAdapterTaskTests(unittest.TestCase):
    def require(self, name):
        cls = getattr(devices, name, None)
        self.assertIsNotNone(cls, f"ЗАДАНИЕ: добавьте {name} в devices.py (см. TASK.md)")
        self.assertTrue(issubclass(cls, devices.Switchable))
        return cls

    def test_object_adapter_wraps_original_fan(self):
        fan = devices.ForeignFan()
        adapter = self.require("FanAdapter")(fan)
        self.assertIs(adapter.fan, fan)
        for enabled, mode in ((True, "RUN"), (True, "RUN"), (False, "STOP"), (False, "STOP")):
            adapter.set_power(enabled)
            self.assertEqual(fan.mode, mode)

    def test_object_adapter_calls_foreign_api(self):
        fan = devices.ForeignFan()
        adapter = self.require("FanAdapter")(fan)
        with patch.object(fan, "set_mode", wraps=fan.set_mode) as set_mode:
            adapter.set_power(True)
            adapter.set_power(False)
            self.assertEqual(set_mode.call_args_list, [call("RUN"), call("STOP")])

    def test_class_adapter_inherits_foreign_fan_and_initializes_state(self):
        cls = self.require("FanClassAdapter")
        self.assertTrue(issubclass(cls, devices.ForeignFan))
        adapter = cls()
        self.assertEqual(adapter.mode, "STOP")
        adapter.set_mode("RUN")
        self.assertEqual(adapter.mode, "RUN")
        adapter.set_power(False)
        self.assertEqual(adapter.mode, "STOP")

    def test_class_adapter_calls_inherited_api(self):
        adapter = self.require("FanClassAdapter")()
        with patch.object(adapter, "set_mode", wraps=adapter.set_mode) as set_mode:
            adapter.set_power(True)
            adapter.set_power(False)
            self.assertEqual(set_mode.call_args_list, [call("RUN"), call("STOP")])

    def test_one_client_controls_both_adapters_and_lights(self):
        fan = devices.ForeignFan()
        fan_adapter = self.require("FanAdapter")(fan)
        class_adapter = self.require("FanClassAdapter")()
        light = devices.ModernLight()
        lamp = devices.LegacyLamp()
        class_lamp = devices.LampClassAdapter()
        switches = [light, devices.LampObjectAdapter(lamp), class_lamp, fan_adapter, class_adapter]
        for enabled, mode in ((True, "RUN"), (False, "STOP"), (False, "STOP"), (True, "RUN")):
            devices.set_all_power(switches, enabled)
            self.assertEqual((fan.mode, class_adapter.mode), (mode, mode))
            self.assertEqual((light.is_on, lamp.powered, class_lamp.powered), (enabled,) * 3)
