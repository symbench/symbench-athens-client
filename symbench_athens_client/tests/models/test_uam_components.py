import json
import math

import pytest

from symbench_athens_client.models.uam_components import Batteries, Motors, Propellers
from symbench_athens_client.utils import get_data_file_path


class TestComponents:
    @pytest.fixture(scope="session")
    def all_components(self):
        with open(get_data_file_path("all_uam_components.json")) as json_file:
            return json.load(json_file)

    def test_batteries_count(self):
        assert len(Batteries) == 27

    def test_propellers_count(self):
        assert len(Propellers) == 940

    def test_wings_count(self):
        pass

    def test_motors_count(self):
        assert len(Motors) == 102

    def test_sensors_count(self):
        pass

    def test_gps_count(self):
        pass

    def test_autopilot_count(self):
        pass

    def test_instrument_batteries_count(self):
        pass

    def test_escs_count(self):
        pass

    def test_receivers_count(self):
        pass

    def test_orients_count(self):
        pass

    def test_flanges_count(self):
        pass

    def test_tubes_count(self):
        pass

    def test_hubs_count(self):
        pass

    def test_cfps_count(self):
        pass

    def test_motor_properties(self):
        E811 = Motors.E811
        assert E811.control_channel == 1
        assert E811.max_current == 226.0
        assert E811.poles is None
        assert E811.adapter_length is None
        assert E811.esc_bec_class is None
        assert E811.max_power == 49200.0
        assert E811.total_length == 200.0
        assert E811.cost == 0.0
        assert E811.shaft_diameter == 50.8
        assert E811.max_no_cells == 108
        assert E811.adapter_diameter is None
        assert E811.length == 187.0
        assert E811.corpus == "uam"

    def test_battery_properties(self):
        Tattu22AhLi = Batteries.Tattu22AhLi
        assert Tattu22AhLi.battery_type == "Wing"
        assert Tattu22AhLi.voltage == 51.8
        assert Tattu22AhLi.module_mass == 8.74
        assert Tattu22AhLi.module_volume == 5991804.0
        assert Tattu22AhLi.peak_discharge_rate == 50.0
        assert Tattu22AhLi.cont_discharge_rate == 25.0
        assert Tattu22AhLi.mount_side == 1
        assert Tattu22AhLi.span == 10000.0
        assert Tattu22AhLi.taper_offset == 0
        assert Tattu22AhLi.thickness == 200.0
        assert Tattu22AhLi.chord_1 == 1000.0
        assert Tattu22AhLi.volume_percent == 100.0
        assert Tattu22AhLi.voltage_request == 800.0
        assert Tattu22AhLi.chord_2 == 1000.0

        assert Tattu22AhLi.model == "Tattu22AhLi"

    def test_component_names(self, all_components):
        for component_name in Propellers.all:
            assert component_name in all_components

        for component_name in Motors.all:
            assert component_name in all_components

        for component_name in Batteries.all:
            assert component_name in all_components

    def test_wing_properties(self):
        pass

    def test_repr(self):
        assert repr(Propellers["55x12_4_1600_51_700"])
