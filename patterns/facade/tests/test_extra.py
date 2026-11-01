import unittest
from unittest.mock import Mock

from ..facade_night_mode import NightModeFacade
from ..home import Curtains, Lighting, Projector, SoundSystem


class NightModeTests(unittest.TestCase):
    def test_night_mode_from_different_states_and_repeated_call(self):
        for watching_movie in (False, True):
            with self.subTest(watching_movie=watching_movie):
                light, curtains = Lighting(), Curtains()
                projector, sound = Projector(), SoundSystem()
                if watching_movie:
                    light.set_brightness(80)
                    projector.turn_on("HDMI 2")
                    sound.turn_on(70)
                facade = NightModeFacade(light, curtains, projector, sound)
                for _ in range(2):
                    facade.start()
                    self.assertEqual(light.brightness, 10)
                    self.assertTrue(curtains.is_closed)
                    self.assertFalse(projector.is_on)
                    self.assertIsNone(projector.source)
                    self.assertFalse(sound.is_on)
                    self.assertEqual(sound.volume, 0)

    def test_calls_subsystem_methods(self):
        light, curtains = Mock(spec=Lighting), Mock(spec=Curtains)
        projector, sound = Mock(spec=Projector), Mock(spec=SoundSystem)
        NightModeFacade(light, curtains, projector, sound).start()
        light.set_brightness.assert_called_once_with(10)
        curtains.close.assert_called_once_with()
        projector.turn_off.assert_called_once_with()
        sound.turn_off.assert_called_once_with()
