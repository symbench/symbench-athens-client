import json
import os

import pytest

from symbench_athens_client.design_in_creo import SymbenchDesingInCREO
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
        return SymbenchDesingInCREO(
            parameters_map=parameters_map, assembly_path=os.environ["RAKE_DESIGN_PATH"]
        )

    def test_parameters_map(self, rake_in_creo):
        pass
