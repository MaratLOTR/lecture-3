import unittest
from unittest.mock import patch

from .. import tree
from ..tree import Device, DeviceGroup


class BuildHouseTaskTests(unittest.TestCase):
    def setUp(self):
        build_house = getattr(tree, "build_demo_house", None)
        self.assertTrue(
            callable(build_house),
            "ЗАДАНИЕ: добавьте build_demo_house() в tree.py (см. TASK.md)",
        )
        self.build_house = build_house
        self.house = build_house()

    def test_structure_matches_assignment(self):
        self.assertIsInstance(self.house, DeviceGroup)
        self.assertEqual(self.house.name, "Дом")
        self.assertEqual(len(self.house.children), 1)
        floor = self.house.children[0]
        self.assertIsInstance(floor, DeviceGroup)
        self.assertEqual(floor.name, "Первый этаж")
        self.assertEqual([c.name for c in floor.children], ["Гостиная", "Кухня"])
        living, kitchen = floor.children
        for room in (living, kitchen):
            self.assertIsInstance(room, DeviceGroup)
        self.assertEqual([d.name for d in living.children], ["Лампа", "Телевизор"])
        self.assertEqual([d.name for d in kitchen.children], ["Чайник"])
        for device in (*living.children, *kitchen.children):
            self.assertIsInstance(device, Device)
            self.assertFalse(device.is_on)

    def test_house_and_room_commands(self):
        living, kitchen = self.house.children[0].children
        self.house.turn_on()
        for device in (*living.children, *kitchen.children):
            self.assertTrue(device.is_on)
        living.turn_off()
        self.assertTrue(all(not d.is_on for d in living.children))
        self.assertTrue(all(d.is_on for d in kitchen.children))
        self.house.turn_off()
        self.assertTrue(all(not d.is_on for d in (*living.children, *kitchen.children)))

    def test_each_call_creates_independent_devices(self):
        self.house.turn_on()
        other = self.build_house()
        self.assertIsNot(other, self.house)

        def nodes(house):
            floor = house.children[0]
            living, kitchen = floor.children
            return (house, floor, living, kitchen, *living.children, *kitchen.children)

        self.assertTrue(set(map(id, nodes(self.house))).isdisjoint(map(id, nodes(other))))
        living, kitchen = other.children[0].children
        for device in (*living.children, *kitchen.children):
            self.assertFalse(device.is_on)

    def test_builder_uses_add_for_every_edge(self):
        edges = []
        original_add = DeviceGroup.add

        def record_add(group, child):
            edges.append((group, child))
            original_add(group, child)

        with patch.object(DeviceGroup, "add", record_add):
            house = self.build_house()

        def collect_edges(group):
            result = []
            for child in group.children:
                result.append((group, child))
                if isinstance(child, DeviceGroup):
                    result.extend(collect_edges(child))
            return result

        self.assertCountEqual(edges, collect_edges(house))
