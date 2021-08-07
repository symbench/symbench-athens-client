import pandas as pd
import pytest

from symbench_athens_client.models.components import Batteries, Battery
from symbench_athens_client.utils import get_data_file_path


class TestComponents:
    @pytest.fixture(scope="session")
    def battery_dataframe(self):
        battery_excel = get_data_file_path("Battery_Corpus.xlsx")
        return pd.read_excel(battery_excel)

    def test_batteries_count(self):
        assert len(Batteries.all) == 34

    def test_battery_fields(self, battery_dataframe):
        aliases = set(field.alias for field in Battery.__fields__.values())
        assert set(battery_dataframe.columns) == aliases

    def test_batteries_attributes(self, battery_dataframe):
        battery_turnigy_nanotech_1450 = Batteries["Turnigy nano-tech 1450mAh 20~40C"]
        assert battery_turnigy_nanotech_1450.manufacturer == "Turnigy"
        assert battery_turnigy_nanotech_1450.cost == 11.49
        assert battery_turnigy_nanotech_1450.length == 85.00
        assert battery_turnigy_nanotech_1450.width == 34.00
        assert battery_turnigy_nanotech_1450.num_cells == "2S1P"
        assert battery_turnigy_nanotech_1450.performance_file == ""
