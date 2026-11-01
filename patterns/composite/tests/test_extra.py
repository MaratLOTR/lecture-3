import unittest

from ..composite_power_usage import PowerDevice, PowerGroup


class PowerUsageTests(unittest.TestCase):
    def test_leaf_power_depends_on_state(self):
        lamp = PowerDevice("Лампа", 12)
        self.assertEqual(lamp.power_usage(), 0)
        lamp.turn_on()
        self.assertEqual(lamp.power_usage(), 12)
        lamp.turn_off()
        self.assertEqual(lamp.power_usage(), 0)

    def test_nested_groups_aggregate_only_enabled_devices(self):
        house, room = PowerGroup("Дом"), PowerGroup("Комната")
        lamp, tv, hall = PowerDevice("Лампа", 12), PowerDevice("ТВ", 80), PowerDevice("Прихожая", 5)
        room.add(lamp)
        room.add(tv)
        house.add(room)
        house.add(hall)
        self.assertEqual(house.power_usage(), 0)
        house.turn_on()
        self.assertEqual(house.power_usage(), 97)
        tv.turn_off()
        self.assertEqual(room.power_usage(), 12)
        self.assertEqual(house.power_usage(), 17)
        room.turn_off()
        self.assertEqual(house.power_usage(), 5)

    def test_empty_group_and_removed_device(self):
        room = PowerGroup("Комната")
        self.assertEqual(room.power_usage(), 0)
        lamp = PowerDevice("Лампа", 12)
        lamp.turn_on()
        room.add(lamp)
        self.assertEqual(room.power_usage(), 12)
        room.remove(lamp)
        self.assertEqual(room.power_usage(), 0)
