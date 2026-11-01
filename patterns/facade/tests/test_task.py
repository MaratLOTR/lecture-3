import unittest
from unittest.mock import Mock

from ..home import Curtains, HomeFacade, Lighting, Projector, SoundSystem
from .test_example import make_home


class LeaveHomeTaskTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            callable(getattr(HomeFacade, "leave_home", None)),
            "ЗАДАНИЕ: добавьте HomeFacade.leave_home() в home.py (см. TASK.md)",
        )

    def test_leaving_home_from_initial_and_movie_states(self):
        for watching_movie in (False, True):
            with self.subTest(watching_movie=watching_movie):
                home = make_home()
                if watching_movie:
                    home.start_movie()
                for _ in range(2):
                    home.leave_home()
                    self.assertEqual(home.lighting.brightness, 0)
                    self.assertTrue(home.curtains.is_closed)
                    self.assertFalse(home.projector.is_on)
                    self.assertIsNone(home.projector.source)
                    self.assertFalse(home.sound.is_on)
                    self.assertEqual(home.sound.volume, 0)

    def test_leave_home_uses_public_subsystem_methods(self):
        light = Mock(spec=Lighting)
        curtains = Mock(spec=Curtains)
        projector = Mock(spec=Projector)
        sound = Mock(spec=SoundSystem)
        home = HomeFacade(light, curtains, projector, sound)
        home.leave_home()
        light.set_brightness.assert_called_once_with(0)
        curtains.close.assert_called_once_with()
        projector.turn_off.assert_called_once_with()
        sound.turn_off.assert_called_once_with()
