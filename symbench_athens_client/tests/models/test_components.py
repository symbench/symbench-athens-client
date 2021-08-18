import json
import math

import pytest

from symbench_athens_client.models.components import (
    Autopilots,
    Batteries,
    CFPs,
    ESCs,
    Flanges,
    GPSes,
    Hubs,
    Instrument_Batteries,
    Motors,
    Orients,
    Propellers,
    Receivers,
    Sensors,
    Servos,
    Tubes,
    Wings,
)
from symbench_athens_client.utils import get_data_file_path


class TestComponents:
    @pytest.fixture(scope="session")
    def all_components(self):
        with open(get_data_file_path("all_components.json")) as json_file:
            return json.load(json_file)

    def test_batteries_count(self):
        assert len(Batteries) == 34

    def test_propellers_count(self):
        assert len(Propellers) == 416

    def test_servo_count(self):
        assert len(Servos) == 27

    def test_wings_count(self):
        assert len(Wings) == 136

    def test_motors_count(self):
        assert len(Motors) == 83

    def test_sensors_count(self):
        assert len(Sensors) == 4

    def test_gps_count(self):
        assert len(GPSes) == 2

    def test_autopilot_count(self):
        assert len(Autopilots) == 4

    def test_instrument_batteries_count(self):
        assert len(Instrument_Batteries) == 3

    def test_escs_count(self):
        assert len(ESCs) == 20

    def test_receivers_count(self):
        assert len(Receivers) == 1

    def test_orients_count(self):
        assert len(Orients) == 1

    def test_flanges_count(self):
        assert len(Flanges) == 1

    def test_tubes_count(self):
        assert len(Tubes) == 2

    def test_hubs_count(self):
        assert len(Hubs) == 5

    def test_cfps_count(self):
        assert len(CFPs) == 1

    def test_motor_properties(self):
        t_motor_at2827kv900 = Motors.t_motor_AT2826KV900
        assert t_motor_at2827kv900.control_channel == None
        assert t_motor_at2827kv900.max_current == 57.0
        assert t_motor_at2827kv900.poles == "12N14P"
        assert t_motor_at2827kv900.adapter_length == (30.0, 36.0)
        assert t_motor_at2827kv900.esc_bec_class == 3.0
        assert t_motor_at2827kv900.max_power == 820.0
        assert t_motor_at2827kv900.total_length == 69.5
        assert t_motor_at2827kv900.cost == 69.99
        assert t_motor_at2827kv900.shaft_diameter == 5.0
        assert t_motor_at2827kv900.max_no_cells == 4.0
        assert t_motor_at2827kv900.adapter_diameter == (6.0, 8.0)
        assert t_motor_at2827kv900.length == 49.0

    def test_battery_properties(self):
        battery_turingy_gphene_6000mah = Batteries.TurnigyGraphene6000mAh3S75C
        assert battery_turingy_gphene_6000mah.number_of_cells == "3S1P"
        assert battery_turingy_gphene_6000mah.cost == 75.16
        another_battery = Batteries["Turnigynano-tech3000mAh2040C"]
        assert math.isnan(another_battery.pack_resistance)

    def test_component_names(self, all_components):
        for component_name in Batteries.all:
            assert component_name in all_components

        for component_name in Motors.all:
            assert component_name in all_components

        for component_name in Wings.all:
            assert component_name in all_components

    def test_wing_properties(self):
        test_wing = Wings.right_NACA_2418
        assert test_wing.tube_offset is None
        assert test_wing.aileron_bias is None
        assert test_wing.servo_width is None
        assert test_wing.control_channel_ailerons is None
        assert test_wing.diameter is None
        assert test_wing.flap_bias is None

    def test_servo_properties(self):
        test_servo = Servos.Hitec_HS_625MG
        assert test_servo.idle_current == 9.1
        assert test_servo.servo_class == "Standard"
        assert test_servo.weight == 0.055200000000000006
        assert test_servo.deadband_width == 8.0

    def test_gps_properties(self):
        test_gps = GPSes.GPS_cuav_CUAVNEOV2
        assert test_gps.output_rate == 10.0
        assert test_gps.power_consumption == 25.0

    def test_esc_properties(self):
        test_esc = ESCs.t_motor_FLAME_70A
        assert test_esc.tube_od is None
        assert test_esc.cont_amps == 70.0
        assert test_esc.control_channel is None

    def test_repr(self):
        assert repr(Batteries["TurnigyGraphene1600mAh4S75C"])
