import os
import shutil
import sys
from pathlib import Path

import pytest

from symbench_athens_client.creoson import CreosonMassPropertiesDriver
from symbench_athens_client.models.components import Batteries


@pytest.mark.skipif(
    os.environ.get("GITHUB_ACTIONS") or sys.platform.startswith("linux"),
    reason="No Creo in github actions/linux",
)
class TestCreosonMassPropertiesDriver:
    @pytest.fixture(autouse=True, scope="session")
    def creoson_driver(self):
        creo_start_filename = "nitro_proe_remote.bat"
        shutil.copy(os.environ["CREO_PARAMETRIC_START_FILE"], creo_start_filename)
        driver = CreosonMassPropertiesDriver(
            nitro_proe_remote_loc=str(Path(creo_start_filename).resolve()),
            use_desktop=True,
        )
        yield driver
        # driver.kill_creo()

    def test_driver_exists(self, creoson_driver):
        assert creoson_driver

    def test_get_set_params(self, creoson_driver):
        for battery_name in Batteries.all:
            battery = Batteries[battery_name]
            creoson_driver.set_parameters(battery)
            params = creoson_driver.get_parameters(battery)
            battery_dict = battery.dict(by_alias=True)
            for param in params:
                if param["name"] in battery_dict:
                    value = param["value"]
                    type_ = param["type"]

                    if type_ == "DOUBLE":
                        value = float(value)
                    elif type_ == "INTEGER":
                        value = int(value)
                    elif type_ == "BOOL":
                        value = bool(value)
                    print(
                        value, type_, type(battery_dict[param["name"]]), param["name"]
                    )
                    assert value == battery_dict[param["name"]]
