import numpy as np
import pandas as pd
import pytest

from symbench_athens_client.models.components import (
    Batteries,
    Battery,
    Motor,
    Motors,
    Propeller,
    Propellers,
)
from symbench_athens_client.utils import get_data_file_path


class TestComponents:
    @pytest.fixture(scope="session")
    def batteries_dataframe(self):
        battery_excel = get_data_file_path("Battery_Corpus.xlsx")
        return pd.read_excel(battery_excel)

    @pytest.fixture(scope="session")
    def propellers_dataframe(self):
        propellers_excel = get_data_file_path("Propeller_Corpus_Rev3.xlsx")
        return pd.read_excel(propellers_excel)

    @pytest.fixture(scope="session")
    def motors_dataframe(self):
        motors_excel = get_data_file_path("Motor_Corpus.xlsx")
        return pd.read_excel(motors_excel)

    def test_batteries_count(self):
        assert len(Batteries) == 34

    def test_battery_fields(self, batteries_dataframe):
        aliases = set(field.alias for field in Battery.__fields__.values())
        assert set(batteries_dataframe.columns) == aliases

    def test_batteries_attributes(self, batteries_dataframe):
        battery_turnigy_nanotech_1450 = Batteries["Turnigy nano-tech 1450mAh 20~40C"]
        assert battery_turnigy_nanotech_1450.manufacturer == "Turnigy"
        assert battery_turnigy_nanotech_1450.cost == 11.49
        assert battery_turnigy_nanotech_1450.length == 85.00
        assert battery_turnigy_nanotech_1450.width == 34.00
        assert battery_turnigy_nanotech_1450.num_cells == "2S1P"
        assert battery_turnigy_nanotech_1450.performance_file == ""

    def test_propellers_count(self, propellers_dataframe):
        assert len(Propellers) == 417

    def test_propellers_attributes(self, propellers_dataframe):
        propeller_14x4s = Propellers["10.5x6"]
        assert propeller_14x4s.name == "10.5x6"
        assert propeller_14x4s.manufacturer == "APC Propellers"
        assert propeller_14x4s.diameter_in == 10.5
        assert propeller_14x4s.performance_file == "PER3_105x6.dat"
        assert np.isclose(propeller_14x4s.pitch_mm, 152.4)

    def test_motors_count(self, motors_dataframe):
        assert len(motors_dataframe) == len(Motors)

    def test_motor_fields(self, motors_dataframe):
        aliases = set(field.alias for field in Motor.__fields__.values())
        assert set(motors_dataframe.columns) == aliases

    def test_motor_attributes(self, motors_dataframe):
        motor_as2308_kv2600 = Motors.as2308_kv2600
        assert motor_as2308_kv2600
        assert motor_as2308_kv2600.adapter_length == (24.0, 28.0)
        assert motor_as2308_kv2600.adapter_diameter == (5.0, 6.0)
        assert motor_as2308_kv2600.poles == "12N14P"
