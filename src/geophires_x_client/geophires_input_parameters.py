import tempfile
from enum import Enum
from pathlib import Path


class EndUseOption(Enum):
    ELECTRICITY = 1
    DIRECT_USE_HEAT = 2
    COGEN_TOPPING_CYCLE = 3
    COGEN_BOTTOMING_CYCLE = 4
    COGEN_SPLIT_OF_MASS_FLOW_RATE = 5


class PowerPlantType(Enum):
    SUBCRITICAL_ORC = 1
    SUPERCRITICAL_ORC = 2
    SINGLE_FLASH = 3
    DOUBLE_FLASH = 4


class GeophiresInputParameters:
    def __init__(self, params):
        # TODO probably better if stable hash of params
        # self._id = str(uuid1())

        self.params = dict(params)

        # TODO validate params

        self._id = hash(frozenset(self.params.items()))

    def as_file_path(self):
        tmp_file_path = Path(tempfile.gettempdir(), f'geophires-input-params_{self._id}.txt')
        f = Path.open(tmp_file_path, 'w')

        f.writelines([','.join([str(p) for p in param_item]) + '\n' for param_item in self.params.items()])
        f.close()
        return tmp_file_path

    def get_output_file_path(self):
        return Path(tempfile.gettempdir(), f'geophires-result_{self._id}.out')

    def __hash__(self):
        return self._id
