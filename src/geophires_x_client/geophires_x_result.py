import re
from pathlib import Path
from types import MappingProxyType

from geophires_x_client.common import log


class GeophiresXResult:
    _RESULT_FIELDS_BY_CATEGORY = MappingProxyType(
        {
            'SUMMARY OF RESULTS': [
                # TODO uses colon delimiter inconsistently
                #'End-Use Option',
                'Average Net Electricity Production',
                'Electricity breakeven price',
                'Average Direct-Use Heat Production',
                'Direct-Use heat breakeven price',
                'Number of production wells',
                'Number of injection wells',
                'Flowrate per production well',
                'Well depth',
                'Geothermal gradient',
            ],
            'ECONOMIC PARAMETERS': [
                'Interest Rate',
                'Accrued financing during construction',
                'Project lifetime',
                'Capacity factor',
            ],  # %  # %
            'ENGINEERING PARAMETERS': [
                'Well depth',
                'Water loss rate',  # %
                'Pump efficiency',  # %
                'Injection temperature',
                'Average production well temperature drop',
                'Flowrate per production well',
                'Injection well casing ID',
                'Produciton well casing ID',  # TODO correct typo upstream
                'Number of times redrilling',
                'Power plant type',
            ],
            'RESOURCE CHARACTERISTICS': ['Maximum reservoir temperature', 'Number of segments', 'Geothermal gradient'],
            'RESERVOIR PARAMETERS': [
                # TODO moved to power generation profile, parse from there
                #  'Annual Thermal Drawdown (%/year)',
                'Bottom-hole temperature',
                'Well seperation: fracture diameter',  # TODO correct typo upstream
                'Fracture area',
                'Reservoir volume',
                'Reservoir hydrostatic pressure',
                'Plant outlet pressure',
                'Production wellhead pressure',
                'Productivity Index',
                'Injectivity Index',
                'Reservoir density',
                'Reservoir thermal conductivity',
                'Reservoir heat capacity',
            ],
            'RESERVOIR SIMULATION RESULTS': [
                'Maximum Production Temperature',
                'Average Production Temperature',
                'Minimum Production Temperature',
                'Initial Production Temperature',
                'Average Reservoir Heat Extraction',
                'Average Production Well Temperature Drop',
                'Average Injection Well Pump Pressure Drop',
                'Average Production Well Pump Pressure Drop',
            ],
            'CAPITAL COSTS (M$)': [
                'Drilling and completion costs',
                'Drilling and completion costs per well',
                'Stimulation costs',
                'Surface power plant costs',
                'Field gathering system costs',
                'Total surface equipment costs',
                'Exploration costs',
                'Total capital costs',
            ],
            'OPERATING AND MAINTENANCE COSTS (M$/yr)': [
                'Wellfield maintenance costs',
                'Power plant maintenance costs',
                'Water costs',
                'Average annual pumping costs',
                'Total operating and maintenance costs',
            ],
            # 'POWER GENERATION RESULTS': [
            #     'Initial direct-use heat production (MWth)',
            #     'Average direct-use heat production (MWth)',
            #     'Average annual heat production (GWh/yr)',
            #     'Average injection well pump pressure drop (kPa)',
            #     'Average production well pump pressure drop (kPa)'
            # ]
            'SURFACE EQUIPMENT SIMULATION RESULTS': [
                'Maximum Net Heat Production',
                'Average Net Heat Production',
                'Minimum Net Heat Production',
                'Initial Net Heat Production',
                'Average Annual Heat Production',
                'Average Pumping Power',
            ],
        }
    )

    _METADATA_FIELDS = (
        #'End-Use Option',
        'Economic Model',
        'Reservoir Model',
    )

    def __init__(self, output_file_path):
        self.output_file_path = output_file_path

        f = Path.open(Path(self.output_file_path), 'r')
        self._lines = list(f.readlines())
        f.close()

        # TODO generic-er result value map
        # TODO Power generation profile
        # TODO "HEAT AND/OR ELECTRICITY EXTRACTION AND GENERATION PROFILE"

        self.result = {}
        for category_fields in GeophiresXResult._RESULT_FIELDS_BY_CATEGORY.items():
            category = category_fields[0]
            fields = category_fields[1]

            self.result[category] = {}
            for field in fields:
                self.result[category][field] = self._get_result_field(field)

        self.result['metadata'] = {'output_file_path': str(self.output_file_path)}
        for metadata_field in GeophiresXResult._METADATA_FIELDS:
            self.result['metadata'][metadata_field] = self._get_metadata_field(metadata_field)

    @property
    def direct_use_heat_breakeven_price_USD_per_MMBTU(self):
        return self.result['SUMMARY OF RESULTS']['Direct-Use heat breakeven price']['value']

    def _get_result_field(self, field):
        # TODO make this less fragile with proper regex
        matching_lines = set(filter(lambda line: f'  {field}:  ' in line, self._lines))

        if len(matching_lines) == 0:
            log.warning(f'Field not found: {field}')
            return None

        if len(matching_lines) > 1:
            log.warning(f'Found multiple ({len(matching_lines)}) entries for field: {field}\n\t{matching_lines}')

        matching_line = matching_lines.pop()
        val_and_unit_str = re.sub(r'\s\s+', '', matching_line.replace(f'{field}:', '').replace('\n', ''))
        val_and_unit_tuple = val_and_unit_str.split(' ')
        str_val = val_and_unit_tuple[0]

        unit = None
        if len(val_and_unit_tuple) == 2:
            unit = val_and_unit_tuple[1]
        elif field.startswith('Number'):
            unit = 'count'

        def number(number_str):
            try:
                if '.' in number_str:
                    return float(number_str)
                else:
                    return int(number_str)
            except TypeError:
                log.error(f'Unable to parse field "{field}" as number: {number_str}')
                return None

        return {'value': number(str_val), 'unit': unit}

    def _get_metadata_field(self, metadata_field):
        metadata_marker = f'{metadata_field} = '
        matching_lines = set(filter(lambda line: metadata_marker in line, self._lines))

        if len(matching_lines) == 0:
            log.warn(f'Metadata Field not found: {metadata_field}')
            return None

        if len(matching_lines) > 1:
            log.warn(f'Found multiple ({len(matching_lines)}) entries for metadata field: {metadata_field}\n\t{matching_lines}')

        return matching_lines.pop().split(metadata_marker)[1].replace('\n', '')
