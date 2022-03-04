import itertools
import json
import math

import pytest

from symbench_athens_client.models.uav_components import (
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
        with open(get_data_file_path("all_uav_components.json")) as json_file:
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
        assert t_motor_at2827kv900.control_channel == 1
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
        assert test_wing.tube_offset == 50
        assert test_wing.aileron_bias == 0.5
        assert test_wing.servo_width == 32.8
        assert test_wing.control_channel_ailerons == 7
        assert test_wing.diameter == 10.16
        assert test_wing.flap_bias == 0.5
        assert test_wing.control_channel_flaps == 6
        assert test_wing.chord == 304.8

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
        assert test_esc.tube_od == 10.0076
        assert test_esc.cont_amps == 70.0
        assert test_esc.control_channel == 1

    def test_repr(self):
        assert repr(Batteries["TurnigyGraphene1600mAh4S75C"])

    def test_battery_swap_aliases(self):
        battery = Batteries[0]
        battery_dict = battery.dict(by_alias=True)
        for key, value in battery.__swap_aliases__.items():
            assert key not in battery_dict
            assert value in battery_dict

    def test_motor_swap_aliases(self):
        motor = Motors[0]
        motor_dict = motor.dict(by_alias=True)
        for key, value in motor.__swap_aliases__.items():
            assert key in motor_dict
            assert value not in motor_dict

    def test_prt_files(self):
        assert Batteries[0].prt_file == "para_battery.prt"
        assert Propellers[0].prt_file == "para_prop.prt"
        assert Receivers[0].prt_file == "para_receiver.prt"
        assert Sensors[0].prt_file == "para_sensor.prt"
        assert Motors[0].prt_file == "para_motor.prt"
        assert GPSes[0].prt_file == "para_gps.prt"
        assert ESCs[0].prt_file == "para_esc.prt"
        assert "para_wing_" in Wings[0].prt_file
        assert Instrument_Batteries[0].prt_file is None
        assert Autopilots[0].prt_file is None

        assert Orients[0].prt_file is None
        assert Flanges[0].prt_file is None
        assert Tubes[0].prt_file is None
        assert Hubs[0].prt_file is None
        assert CFPs[0].prt_file is None

    def test_proptype(self):
        assert not any(prop.prop_type for prop in Propellers)

    def test_corpus(self):
        assert set(
            batt.corpus
            for batt in itertools.chain(
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
        ) == {"uav"}
