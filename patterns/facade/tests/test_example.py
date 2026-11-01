import unittest
from unittest.mock import Mock

from ..home import Curtains, HomeFacade, Lighting, Projector, SoundSystem


def make_home():
    return HomeFacade(Lighting(), Curtains(), Projector(), SoundSystem())


class FacadeTests(unittest.TestCase):
    def test_start_movie_configures_all_subsystems(self):
        home = make_home()
        home.start_movie()
        self.assertEqual(home.lighting.brightness, 20)
        self.assertTrue(home.curtains.is_closed)
        self.assertTrue(home.projector.is_on)
        self.assertEqual(home.projector.source, "HDMI 1")
        self.assertTrue(home.sound.is_on)
        self.assertEqual(home.sound.volume, 35)

    def test_end_movie_resets_all_subsystems(self):
        home = make_home()
        home.start_movie()
        home.end_movie()
        self.assertEqual(home.lighting.brightness, 100)
        self.assertFalse(home.curtains.is_closed)
        self.assertFalse(home.projector.is_on)
        self.assertIsNone(home.projector.source)
        self.assertFalse(home.sound.is_on)
        self.assertEqual(home.sound.volume, 0)

    def test_subsystems_remain_available_without_facade(self):
        home = make_home()
        home.lighting.set_brightness(70)
        self.assertEqual(home.lighting.brightness, 70)
        self.assertFalse(home.projector.is_on)

    def test_invalid_levels_do_not_change_subsystems(self):
        light = Lighting()
        sound = SoundSystem()
        for value in (-1, 101):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    light.set_brightness(value)
                with self.assertRaises(ValueError):
                    sound.turn_on(value)
        self.assertEqual(light.brightness, 100)
        self.assertEqual(sound.volume, 0)
        self.assertFalse(sound.is_on)

