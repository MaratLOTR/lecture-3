import unittest

from .. import tree
from ..tree import Device, DeviceGroup


class CompositeTests(unittest.TestCase):
    def test_nested_group_commands_reach_all_leaves(self):
        house = DeviceGroup("Дом")
        room = DeviceGroup("Комната")
        lamp = Device("Лампа")
        tv = Device("Телевизор")
        hall_light = Device("Прихожая")
        room.add(lamp)
        room.add(tv)
        house.add(room)
        house.add(hall_light)
        house.turn_on()
        self.assertTrue(all(d.is_on for d in (lamp, tv, hall_light)))
        room.turn_off()
        self.assertFalse(lamp.is_on)
        self.assertFalse(tv.is_on)
        self.assertTrue(hall_light.is_on)
        house.turn_off()
        self.assertFalse(hall_light.is_on)

    def test_leaf_and_empty_group_support_common_operations(self):
        for component in (Device("Лампа"), DeviceGroup("Пустая комната")):
            component.turn_on()
            self.assertTrue(component.describe())
            component.turn_off()
        self.assertFalse(component.children)

    def test_removed_device_can_move_and_no_longer_receives_old_commands(self):
        old = DeviceGroup("Старая комната")
        new = DeviceGroup("Новая комната")
        lamp = Device("Лампа")
        old.add(lamp)
        old.remove(lamp)
        old.turn_on()
        self.assertFalse(lamp.is_on)
        new.add(lamp)
        new.turn_on()
        self.assertTrue(lamp.is_on)

    def test_tree_rejects_self_and_ancestor_cycles(self):
        root = DeviceGroup("Дом")
        room = DeviceGroup("Комната")
        root.add(room)
        with self.assertRaises(ValueError):
            root.add(root)
        with self.assertRaises(ValueError):
            room.add(root)
        self.assertEqual(root.children, (room,))
        self.assertEqual(room.children, ())

    def test_component_cannot_have_two_parents_or_be_added_twice(self):
        first = DeviceGroup("Первая")
        second = DeviceGroup("Вторая")
        lamp = Device("Лампа")
        first.add(lamp)
        with self.assertRaises(ValueError):
            first.add(lamp)
        with self.assertRaises(ValueError):
            second.add(lamp)
        self.assertEqual(first.children, (lamp,))
        self.assertEqual(second.children, ())

    def test_invalid_add_and_remove_preserve_group(self):
        group = DeviceGroup("Комната")
        lamp = Device("Лампа")
        group.add(lamp)
        with self.assertRaises(TypeError):
            group.add("не устройство")
        with self.assertRaises(ValueError):
            group.remove(Device("Чужая лампа"))
        self.assertEqual(group.children, (lamp,))

