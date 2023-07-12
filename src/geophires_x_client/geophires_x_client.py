import json
import os
import sys
from pathlib import Path

import GEOPHIRESv3 as geophires

from geophires_x_client.common import log
from geophires_x_client.geophires_input_parameters import EndUseOption
from geophires_x_client.geophires_input_parameters import GeophiresInputParameters
from geophires_x_client.geophires_x_result import GeophiresXResult


class GeophiresXClient:
    def __init__(self, enable_caching=True):
        self._enable_caching = enable_caching
        self._cache = {}

    def get_geophires_result(self, input_params: GeophiresInputParameters) -> GeophiresXResult:
        cache_key = hash(input_params)
        if self._enable_caching and cache_key in self._cache:
            return self._cache[cache_key]

        stash_cwd = Path.cwd()
        stash_sys_argv = sys.argv

        sys.argv = ['', input_params.as_file_path(), input_params.get_output_file_path()]
        geophires.GEOPHIRESv3.main()

        # Undo the ~unconventional~ things Geophires does.
        sys.argv = stash_sys_argv
        os.chdir(stash_cwd)

        log.info(f'GEOPHIRES-X output file: {input_params.get_output_file_path()}')

        result = GeophiresXResult(input_params.get_output_file_path())
        if self._enable_caching:
            self._cache[cache_key] = result

        return result


if __name__ == '__main__':
    client = GeophiresXClient()
    params = GeophiresInputParameters(
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

    result = client.get_geophires_result(params)
    log.info(f'Breakeven price: ${result.direct_use_heat_breakeven_price_USD_per_MMBTU}/MMBTU')
    log.info(json.dumps(result.result, indent=2))
