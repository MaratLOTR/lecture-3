import unittest
from unittest.mock import patch

from ..adapter_thermostat import ForeignThermostat, ThermostatAdapter


class ThermostatTests(unittest.TestCase):
    def test_reads_the_current_temperature_of_original_device(self):
        thermostat = ForeignThermostat()
        adapter = ThermostatAdapter(thermostat)
        self.assertAlmostEqual(adapter.get_celsius(), 20)
        thermostat.write_fahrenheit(86)
        self.assertAlmostEqual(adapter.get_celsius(), 30)

    def test_writes_fractional_temperature_through_foreign_api(self):
        thermostat = ForeignThermostat()
        adapter = ThermostatAdapter(thermostat)
        with patch.object(thermostat, "write_fahrenheit", wraps=thermostat.write_fahrenheit) as write:
            adapter.set_celsius(22.5)
            write.assert_called_once()
            self.assertAlmostEqual(write.call_args.args[0], 72.5)
        self.assertAlmostEqual(thermostat.read_fahrenheit(), 72.5)
        self.assertAlmostEqual(adapter.get_celsius(), 22.5)

    def test_boundaries_and_rejected_commands(self):
        thermostat = ForeignThermostat()
        adapter = ThermostatAdapter(thermostat)
        for celsius, fahrenheit in ((10, 50), (30, 86)):
            adapter.set_celsius(celsius)
            self.assertAlmostEqual(thermostat.read_fahrenheit(), fahrenheit)
        for invalid in (9, 31, float("nan")):
            with self.assertRaises(ValueError):
                adapter.set_celsius(invalid)
            self.assertAlmostEqual(thermostat.read_fahrenheit(), 86)
