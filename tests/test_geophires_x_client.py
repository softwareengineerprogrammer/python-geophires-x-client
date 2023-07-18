import os.path
import unittest

from geophires_x_client.cli import main
from geophires_x_client.geophires_input_parameters import EndUseOption
from geophires_x_client.geophires_input_parameters import GeophiresInputParameters
from geophires_x_client.geophires_x_client import GeophiresXClient
from geophires_x_client.geophires_x_result import GeophiresXResult


class GeophiresXClientTestCase(unittest.TestCase):
    def test_main(self):
        assert main([]) == 0

    def test_geophires_x(self):
        client = GeophiresXClient()
        result = client.get_geophires_result(
            GeophiresInputParameters(
                {
                    'Print Output to Console': 0,
                    'End-Use Option': EndUseOption.DIRECT_USE_HEAT.value,
                    'Reservoir Model': 1,
                    'Time steps per year': 1,
                    'Reservoir Depth': 3,
                    'Gradient 1': 50,
                    'Maximum Temperature': 250,
                }
            )
        )

        assert result is not None

        result_same_input = client.get_geophires_result(
            GeophiresInputParameters(
                {
                    'Print Output to Console': 0,
                    'End-Use Option': EndUseOption.DIRECT_USE_HEAT.value,
                    'Reservoir Model': 1,
                    'Time steps per year': 1,
                    'Reservoir Depth': 3,
                    'Gradient 1': 50,
                    'Maximum Temperature': 250,
                }
            )
        )

        assert result == result_same_input

        # TODO assert that result was retrieved from cache instead of recomputed (somehow)

    def test_geophires_x_result(self):
        result = GeophiresXResult(os.path.abspath('geophires-result_example-1.out'))
        assert result is not None
        expected_price = 5.85
        assert result.direct_use_heat_breakeven_price_USD_per_MMBTU == expected_price
        assert result.result['SUMMARY OF RESULTS']['Direct-Use heat breakeven price']['value'] == expected_price
        assert result.result['SUMMARY OF RESULTS']['Direct-Use heat breakeven price']['unit'] == 'USD/MMBTU'

    def test_input_hashing(self):
        input1 = GeophiresInputParameters(
            {'End-Use Option': EndUseOption.DIRECT_USE_HEAT.value, 'Gradient 1': 50, 'Maximum Temperature': 250}
        )

        input2 = GeophiresInputParameters(
            {'Maximum Temperature': 250, 'End-Use Option': EndUseOption.DIRECT_USE_HEAT.value, 'Gradient 1': 50}
        )

        assert hash(input1) == hash(input2)

        input3 = GeophiresInputParameters(
            {'Maximum Temperature': 420, 'End-Use Option': EndUseOption.DIRECT_USE_HEAT.value, 'Gradient 1': 69}
        )

        assert hash(input1) != hash(input3)
