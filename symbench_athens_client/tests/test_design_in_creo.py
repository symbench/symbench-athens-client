import json
import os

import pytest

from symbench_athens_client.design_in_creo import SymbenchDesignInCREO
from symbench_athens_client.tests.utils import get_test_file_path


@pytest.mark.slow
@pytest.mark.skipif(os.environ.get("CI"), reason="Skip in CI.")
class TestCreoDesignSweeper:
    @pytest.fixture(scope="session")
    def parameters_map(self):
        with open(get_test_file_path("rake_parameters_map.json")) as param_map_file:
            return json.load(param_map_file)

    @pytest.fixture(scope="session")
    def rake_in_creo(self, parameters_map):
        return SymbenchDesignInCREO(
            parameters_map=parameters_map, assembly_path=os.environ["RAKE_DESIGN_PATH"]
        )

    def test_apply_parameters(self, rake_in_creo):
        parameters = {"Param_10": 2800.0, "Param_15": 1000.0}

        assert rake_in_creo.apply_params(parameters)
