import csv
import itertools
import json

import pytest

from symbench_athens_client.models.uam_components import (
    Batteries,
    BatteryControllers,
    Beam_Caps,
    Beams,
    Cylinder_Flips,
    Cylinders,
    Flanges,
    Fuselages,
    Hubs,
    Motors,
    NACA_Port_Connectors,
    Orients,
    Passengers,
    Propellers,
    Tubes,
    Wings,
)
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
        assert len(Wings) == 1

    def test_motors_count(self):
        assert len(Motors) == 102

    def test_beam_caps_count(self):
        assert len(Beam_Caps) == 1

    def test_naca_port_connectors_count(self):
        assert len(NACA_Port_Connectors) == 1

    def test_battery_controllers_count(self):
        assert len(BatteryControllers) == 1

    def test_cylinders_batteries_count(self):
        assert len(Cylinders) == 1

    def test_fuselages_count(self):
        assert len(Fuselages) == 1

    def test_orients_count(self):
        assert len(Orients) == 1

    def test_passengers_count(self):
        assert len(Passengers) == 1

    def test_beams_count(self):
        assert len(Beams) == 1

    def test_cylinder_flips_count(self):
        assert len(Cylinder_Flips) == 1

    def test_missing_components(self):
        missing_txt = get_data_file_path("missing_uam_components.txt")
        with open(missing_txt) as txt_file:
            missing_lines = list(txt_file.readlines())
            all_missing = missing_lines[-1].strip()
            assert set(itertools.chain(Hubs.all, Flanges.all, Tubes.all)) == set(
                all_missing.split(",")
            )

    def test_flanges_count(self):
        assert len(Flanges) == 2

    def test_tubes_count(self):
        assert len(Tubes) == 2

    def test_hubs_count(self):
        assert len(Hubs) == 5

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
        for component_name in itertools.chain(
            Batteries.all,
            Motors.all,
            Propellers.all,
            Wings.all,
            Beam_Caps.all,
            NACA_Port_Connectors.all,
            BatteryControllers.all,
            Cylinders.all,
            Fuselages.all,
            Passengers.all,
            Orients.all,
            Beams.all,
            Cylinder_Flips.all,
            Flanges.all,
            Hubs.all,
            Tubes.all,
        ):
            assert component_name in all_components

    def test_wing_properties(self):
        wing = Wings.naca_wing
        assert wing.taper_offset == 0
        assert wing.aileron_bias == 0.5
        assert wing.chord_1 == 1000
        assert wing.span == 10000
        assert wing.flap_bias == 0.5
        assert wing.naca_profile == "0012"
        assert wing.load == 1.28106e011
        assert wing.thickness == 12.0
        assert wing.chord_2 == 1000.0

    def test_beam_cap_properties(self):
        beam_cap = Beam_Caps.Beam_Cap
        assert beam_cap.thickness == 40.0
        assert beam_cap.chord == 500.0

    def test_naca_connector_properties(self):
        naca_connector = NACA_Port_Connectors.naca_connector
        assert naca_connector.bottom_connection_disp == 0
        assert naca_connector.port_thickness == 100.0
        assert naca_connector.chord == 4000
        assert naca_connector.thickness == 12.0

    def test_battery_controller_properties(self):
        battery_controller = BatteryControllers.BatteryController
        assert battery_controller.input_voltage == 1.0
        assert battery_controller.output_voltage == 1.0

    def test_cylinder_properties(self):
        cylinder = Cylinders.PORTED_CYL
        assert cylinder.wall_thickness == 3.0
        assert cylinder.classification == "Cylinder"
        assert (
            cylinder.top_conn_display
            == cylinder.left_conn_display
            == cylinder.right_conn_display
            == cylinder.bottom_conn_display
            == 0.0
        )
        assert cylinder.port_thickness == 100.0
        assert cylinder.diameter == 200.0
        assert cylinder.front_angle == 0
        assert cylinder.length == 5000.0

    def test_fuselage_properties(self):
        fuse_sphere_cyl_cone = Fuselages.FUSE_SPHERE_CYL_CONE
        assert fuse_sphere_cyl_cone.wall_thickness == 3.0
        assert fuse_sphere_cyl_cone.classification == "Fuselage"
        assert fuse_sphere_cyl_cone.seat_1_lr == -200.0
        assert fuse_sphere_cyl_cone.floor_height == 150.0
        assert fuse_sphere_cyl_cone.port_thickness == 100.0
        assert fuse_sphere_cyl_cone.middle_length == 750.0
        assert fuse_sphere_cyl_cone.bottom_port_disp == 0.0
        assert fuse_sphere_cyl_cone.length == 2000.0
        assert fuse_sphere_cyl_cone.seat_2_fb == 1000.0
        assert fuse_sphere_cyl_cone.seat_1_fb == 1000.0
        assert fuse_sphere_cyl_cone.seat_2_lr == 200.0
        assert fuse_sphere_cyl_cone.tail_diameter == 200.0
        assert fuse_sphere_cyl_cone.sphere_diameter == 1520.0
        assert fuse_sphere_cyl_cone.right_port_disp == 0.0
        assert fuse_sphere_cyl_cone.top_port_disp == 0.0
        assert fuse_sphere_cyl_cone.left_port_disp == 0.0

    def test_passengers_properties(self):
        passenger = Passengers.Passenger
        assert passenger.weight == 90.0
        assert passenger.classification == "Passenger"

    def test_beams_properties(self):
        beam = Beams.Beam
        assert beam.top_conn_disp == 0.0
        assert beam.chord == 500.0
        assert beam.thickness == 40.0
        assert beam.span == 1000.0
        assert beam.bottom_conn_disp == 0.0
        assert beam.classification == "Beam"

    def test_cylinder_flips_properties(self):
        cyl_flip = Cylinder_Flips.Cyl_Flip
        assert cyl_flip.wall_thickness == 3.0
        assert cyl_flip.length == 5.0
        assert cyl_flip.diameter == 200.0

    def test_flange_properties(self):
        flange = Flanges["0281_para_flange"]
        assert flange.od == 7.3152
        assert flange.num_horizontal_conn == 2
        assert flange.angle_horizontal_connection == 90.0
        assert flange.box == 30.48
        assert flange.offset == 0.0
        assert flange.classification == "Flange"

    def test_tube_properties(self):
        tube = Tubes["0281OD_para_tube"]
        assert tube.length == 200.0
        assert tube.od == 7.1374
        assert tube.id == 4.699

    def test_hub_properties(self):
        hub = Hubs["0394od_para_hub_4"]
        assert hub.num_of_horizontal_connections == 4
        assert hub.angle_of_horizontal_connections == 90.0

    def test_battery_swap_aliases(self):
        battery = Batteries[0]
        battery_dict = battery.dict(by_alias=True)
        for key, value in battery.__swap_aliases__.items():
            assert key in battery_dict
            assert value not in battery_dict

    def test_motor_swap_aliases(self):
        motor = Motors[0]
        motor_dict = motor.dict(by_alias=True)
        for key, value in motor.__swap_aliases__.items():
            assert key not in motor_dict
            assert value in motor_dict

    def test_repr(self):
        assert repr(Propellers["55x12_4_1600_51_700"])

    def test_to_csv(self):
        Batteries.to_csv("batteries.csv")
        with open("batteries.csv") as batt_csv:
            reader = csv.DictReader(batt_csv)
            assert "VOLTAGE" not in reader.fieldnames
            assert "BASE_VOLTAGE" in reader.fieldnames

        Motors.to_csv("motors.csv")
        with open("motors.csv") as batt_csv:
            reader = csv.DictReader(batt_csv)
            assert "IO_IDLE_CURRENT_10V" in reader.fieldnames
            assert "IO_IDLE_CURRENT@10V" not in reader.fieldnames
