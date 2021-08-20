from typing import ClassVar, Dict, List, Tuple, Union

from pydantic import BaseModel, Field, validator

from symbench_athens_client.models.components import (
    ESC,
    Batteries,
    Battery,
    CarbonFiberPlate,
    CFPs,
    ESCs,
    Flange,
    Flanges,
    Hub,
    Hubs,
    Motor,
    Motors,
    Orient,
    Orients,
    Propeller,
    Propellers,
    Servo,
    Servos,
    Tube,
    Tubes,
    Wing,
    Wings,
)
from symbench_athens_client.utils import dict_to_design_vars


class SeedDesign(BaseModel):

    __design_vars__: ClassVar[str] = {
        "q_position",
        "q_velocity",
        "q_angular_velocity",
        "q_angles",
        "r",
    }

    name: str = Field(
        "", alias="name", description="Name of the seed design in the graph database"
    )

    swap_list: Dict[str, List[str]] = Field(
        {}, description="list of swap components for this design", alias="swap_list"
    )

    q_position: Union[float, Tuple[float, float]] = Field(
        default=1.0, alias="Q_Position", description="The Q-Position"
    )

    q_velocity: Union[float, Tuple[float, float]] = Field(
        default=1.0, description="The Q-Velocity", alias="Q_Velocity"
    )

    q_angular_velocity: Union[float, Tuple[float, float]] = Field(
        default=1.0, description="The Q-Angular Velocity", alias="Q_Angular_Velocity"
    )

    q_angles: Union[float, Tuple[float, float]] = Field(
        1.0, description="The Q-Angles", alias="Q_Angles"
    )

    r: Union[float, Tuple[float, float]] = Field(
        1.0, description="The R-Parameter", alias="R"
    )

    def to_jenkins_parameters(self):
        design_vars = self.dict(by_alias=True, include=self.__design_vars__)
        return {"DesignVars": dict_to_design_vars(design_vars, repeat_values=True)}

    def parameters(self):
        return self.dict(by_alias=True, include=self.__design_vars__)

    def components(self, by_alias=True):
        all_components = self.dict(
            by_alias=by_alias, exclude={"name", "swap_list"}.union(self.__design_vars__)
        )
        names = {}

        for component in all_components:
            names[component] = (
                all_components[component]["Name"]
                if by_alias
                else all_components[component]["name"]
            )

        return names

    def reset_name(self):
        self.name = self.__class__.__name__

    def clear_swap(self, component_instance_name=None):
        if component_instance_name is None:
            self.swap_list = {}
        else:
            del self.swap_list[component_instance_name]

    def needs_swap(self):
        return len(self.swap_list) > 0

    def iter_components(self, by_alias=True):
        for field_key, v in self.__dict__.items():
            if field_key not in self.__design_vars__ and field_key != "name":
                name = field_key
                if by_alias:
                    name = self.__fields__[field_key].alias
                yield name, v

    def __setattr__(self, key, value):
        if key not in self.__design_vars__ and (key != "name" and key != "swap_list"):
            if getattr(self, key) != value:
                field_info_for_key = self.__fields__[key]
                if not self.swap_list.get(field_info_for_key.alias):
                    self.swap_list[field_info_for_key.alias] = [getattr(self, key).name]
                self.swap_list[field_info_for_key.alias].append(value.name)

        super().__setattr__(key, value)

    @validator("name", pre=True, always=True)
    def validate_name(cls, name):
        if name is None or name == "":
            name = cls.__name__
        return name

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True


class QuadCopter(SeedDesign):
    """The quadcopter seed design"""

    __design_vars__ = {
        "arm_length",
        "support_length",
        "batt_mount_x_offset",
        "batt_mount_z_offset",
        "q_position",
        "q_velocity",
        "q_angular_velocity",
        "q_angles",
        "r",
    }

    def __init__(
        self,
        arm_length=220.0,
        support_length=95.0,
        batt_mount_x_offset=0.0,
        batt_mount_z_offset=0.0,
    ):
        super(QuadCopter, self).__init__(
            arm_length=arm_length,
            support_length=support_length,
            batt_mount_x_offset=batt_mount_x_offset,
            batt_mount_z_offset=batt_mount_z_offset,
        )

    arm_length: Union[float, Tuple[float, float]] = Field(
        220.0,
        description="Length of Arm_0, Arm_1, Arm_2, Arm_3 in mm",
        alias="Length_0",
    )

    support_length: Union[float, Tuple[float, float]] = Field(
        95.0,
        description="Length of support_0, Support_1, Support_2, Support_3 in mm",
        alias="Length_1",
    )

    batt_mount_x_offset: Union[float, Tuple[float, float]] = Field(
        0.0,
        description="X-Offset of the battery mounting position from center of the plate in mm",
        alias="Length_8",
    )

    batt_mount_z_offset: Union[float, Tuple[float, float]] = Field(
        0.0,
        description="Z-Offset of the battery mounting position from center of the plate in mm",
        alias="Length_9",
    )

    battery_0: Battery = Field(
        Batteries["TurnigyGraphene1000mAh2S75C"],
        description="Battery_0",
        alias="Battery_0",
    )

    esc_0: ESC = Field(ESCs.ESC_debugging, description="ESC 0", alias="ESC_0")

    esc_1: ESC = Field(ESCs.ESC_debugging, description="ESC 1", alias="ESC_1")

    esc_2: ESC = Field(ESCs.ESC_debugging, description="ESC 2", alias="ESC_2")

    esc_3: ESC = Field(ESCs.ESC_debugging, description="ESC 3", alias="ESC_3")

    motor_0: Motor = Field(
        Motors.t_motor_AT2312KV1400, description="Motor 0", alias="Motor_0"
    )

    motor_1: Motor = Field(
        Motors.t_motor_AT2312KV1400, description="Motor 0", alias="Motor_1"
    )

    motor_2: Motor = Field(
        Motors.t_motor_AT2312KV1400, description="Motor 0", alias="Motor_2"
    )

    motor_3: Motor = Field(
        Motors.t_motor_AT2312KV1400, description="Motor 0", alias="Motor_3"
    )

    propeller_0: Propeller = Field(
        Propellers.apc_propellers_6x4EP, description="Propeller 0", alias="Prop_0"
    )

    propeller_1: Propeller = Field(
        Propellers.apc_propellers_6x4E, description="Propeller 1", alias="Prop_1"
    )

    propeller_2: Propeller = Field(
        Propellers.apc_propellers_6x4EP, description="Propeller 2", alias="Prop_2"
    )

    propeller_3: Propeller = Field(
        Propellers.apc_propellers_6x4E, description="Propeller 2", alias="Prop_3"
    )

    flange_0: Flange = Field(
        Flanges["0394_para_flange"], description="Flange 0", alias="Flange_0"
    )

    flange_1: Flange = Field(
        Flanges["0394_para_flange"], description="Flange 1", alias="Flange_1"
    )

    flange_2: Flange = Field(
        Flanges["0394_para_flange"], description="Flange 2", alias="Flange_2"
    )

    flange_3: Flange = Field(
        Flanges["0394_para_flange"], description="Flange 3", alias="Flange_3"
    )

    support_0: Tube = Field(
        Tubes["0394OD_para_tube"], description="Support 0", alias="Support_0"
    )

    support_1: Tube = Field(
        Tubes["0394OD_para_tube"], description="Support 1", alias="Support_1"
    )

    support_2: Tube = Field(
        Tubes["0394OD_para_tube"], description="Support 2", alias="Support_2"
    )

    support_3: Tube = Field(
        Tubes["0394OD_para_tube"], description="Support 3", alias="Support_3"
    )

    arm_0: Tube = Field(Tubes["0394OD_para_tube"], description="Arm 0", alias="Arm_0")

    arm_1: Tube = Field(Tubes["0394OD_para_tube"], description="Arm 1", alias="Arm_1")

    arm_2: Tube = Field(Tubes["0394OD_para_tube"], description="Arm 2", alias="Arm_2")

    arm_3: Tube = Field(Tubes["0394OD_para_tube"], description="Arm 3", alias="Arm_3")

    orient: Orient = Field(Orients["Orient"], description="Orient", alias="Orient")

    para_cf_plate: CarbonFiberPlate = Field(
        CFPs["para_cf_fplate"], description="Carbon fiber plate", alias="para_cf_fplate"
    )

    hub_4_way: Hub = Field(Hubs["0394od_para_hub_4"], alias="Hub_4Way")

    @validator(*__design_vars__, pre=True, always=True)
    def validate_design_vars_tuple(cls, value):
        if isinstance(value, Tuple):
            assert (
                value[0] <= value[1]
            ), "The first element should be less than the second one; while using ranges"
        return value

    def to_fd_input(
        self,
        test_bench_path,
        propellers_data_path=None,
        filename=None,
        analysis_type=3,
        flight_path=1,
        requested_vertical_speed=10.0,
        requested_lateral_speed=1,
    ):
        """Get SWRi's flight dynamics model's input files for this design

        Parameters
        ----------
        test_bench_path: str, pathlib.Path
            The location of the testbench data to use by uav_analysis.testbench_data.TestBenchData
        propellers_data_path: str, pathlib.Path
            The base directory for propellers data
        filename: str, pathlib.Path
            The Path of the input file, should have an .inp extension
        analysis_type: int, default=3
            The analysis type for this input file (3=flight path analysis, 2=Trim Steady, 1=Initial Conditions)
        flight_path: int, default=1
            The flight path for analysis_type of 3, (1=fly straight line, 2=Unused, 3= fly circle, 4 = rise and hover, 5 = racing oval
        requested_vertical_speed: float, default=10.0
            The requested vertical speed for the FD software
        requested_lateral_speed: int, default=1
            The requested lateral speed for the FD software

        Returns
        -------
        dict or None
            if filename is None, this method will return a dictionary containing all the parameters
            otherwise the file will be saved as filename
        """
        masses = self._get_mass_properties(test_bench_path)
        propeller_1 = self.propeller_0.to_fd_inp(propellers_data_path)
        propeller_1["for"] = 0
        propeller_1.update(self.motor_0.to_fd_inp())
        propeller_1.update(masses["propeller_0"])

        propeller_2 = self.propeller_1.to_fd_inp(propellers_data_path)
        propeller_2.update(self.motor_1.to_fd_inp())
        propeller_2.update(masses["propeller_1"])
        propeller_2["for"] = 1

        propeller_3 = self.propeller_2.to_fd_inp(propellers_data_path)
        propeller_3.update(self.motor_2.to_fd_inp())
        propeller_3.update(masses["propeller_2"])
        propeller_3["for"] = 2

        propeller_4 = self.propeller_3.to_fd_inp(propellers_data_path)
        propeller_4.update(self.motor_3.to_fd_inp())
        propeller_4.update(masses["propeller_3"])
        propeller_4["for"] = 3

        self._assign_normals(propeller_1)
        self._assign_normals(propeller_2)
        self._assign_normals(propeller_3)
        self._assign_normals(propeller_4)
        self._assign_controls_and_battery(
            propeller_1, propeller_2, propeller_3, propeller_4
        )

        aircraft_data = {
            "cname": f"'UAV_{self.name}' ! M name of the aircraft",
            "ctype": f"'SymCPS UAV Design'  ! Type of the Aircraft",
            "num_wings": "0  ! M number of wings in aircraft",
            "uc_initial": [
                "0.4d0, 0.5d0, 0.6d0, 0.7d0 ! inputs for controls",
                "0.5d0, 0.5d0, 0.5d0, 0.5d0",
            ],
            "time": "0.d0        ! initial time (default = 0.)",
            "dt": "1.d-03        ! s  fixed time step",
            "dt_output": "1.0d0  ! s  time between output lines",
            "time_end": "1000.d0       ! s  end time ",
            "Unwind": "0.d0      !  North wind speed in world frame",
            "Vewind": "0.d0      !  East wind speed in  world frame",
            "Wdwind": "0.d0      ! Down wind speed in world frame",
            "debug": "0          ! verbose printouts from fderiv",
            "num_propellers": 4,
            "num_batteries": 1,
            "i_analysis_type": analysis_type,
            "x_initial": "0.d0, 0.d0, 0.d0, 0.d0, 0.d0, 0.d0, 1.d0, 0.d0, 0.d0, 0.d0, 0.d0, 0.d0, 0.d0",
        }

        aircraft_data.update(masses["aircraft"])

        fd_params = {
            "aircraft": aircraft_data,
            "propellers": [propeller_1, propeller_2, propeller_3, propeller_4],
            "battery": self.battery_0.to_fd_inp(),
            "controls": {
                "i_flight_path": flight_path,
                "requested_lateral_speed": int(requested_lateral_speed),
                "requested_vertical_speed": requested_vertical_speed,
                "iaileron": 5,
                "iflap": 6,
                "Q_position": self.q_position,
                "Q_velocity": self.q_velocity,
                "Q_angular_velocity": self.q_angular_velocity,
                "Q_angles": self.q_angles,
                "R": self.r,
            },
        }

        if filename is not None:
            with open(filename, "w") as fd_inp:
                fd_inp.write(self._to_fd_inp(fd_params))
        else:
            return fd_params

    def _get_mass_properties(self, testbench_path):
        """Get estimated mass properties for the quadcopter(works only for single parameters for now)"""
        from symbench_athens_client.utils import get_mass_estimates_for_quadcopter

        for var in self.__design_vars__:
            if isinstance(getattr(self, var), Tuple):
                raise ValueError(
                    "Cannot estimate mass properties for a range. "
                    "Please set discrete values for the design variables."
                )

        property_estimates = get_mass_estimates_for_quadcopter(testbench_path, self)
        property_estimates["x_fuse"] = property_estimates["x_cm"]
        property_estimates["y_fuse"] = property_estimates["y_cm"]
        property_estimates["z_fuse"] = property_estimates["z_cm"]
        return {
            "propeller_0": {
                "x": property_estimates.pop("Prop_0_x"),
                "y": property_estimates.pop("Prop_0_y"),
                "z": property_estimates.pop("Prop_0_z"),
            },
            "propeller_1": {
                "x": property_estimates.pop("Prop_1_x"),
                "y": property_estimates.pop("Prop_1_y"),
                "z": property_estimates.pop("Prop_1_z"),
            },
            "propeller_2": {
                "x": property_estimates.pop("Prop_2_x"),
                "y": property_estimates.pop("Prop_2_y"),
                "z": property_estimates.pop("Prop_2_z"),
            },
            "propeller_3": {
                "x": property_estimates.pop("Prop_3_x"),
                "y": property_estimates.pop("Prop_3_y"),
                "z": property_estimates.pop("Prop_3_z"),
            },
            "aircraft": property_estimates,
        }

    @staticmethod
    def _assign_normals(propeller_dict):
        propeller_dict.update({"nx": 0.0, "ny": 0.0, "nz": -1.0})

    @staticmethod
    def _assign_controls_and_battery(*propeller_dicts):
        for i, inp_dict in enumerate(propeller_dicts):
            inp_dict["icontrol"] = i + 1
            inp_dict["ibattery"] = 1

    @staticmethod
    def _to_fd_inp(input_dict):
        """Write the flight dynamics input file (Clean refactorable implementation)"""
        inp_lines = ["&aircraft_data"]
        duplicate_entries = []
        for key, value in input_dict["aircraft"].items():
            if isinstance(value, list):
                for j in range(1, len(value)):
                    duplicate_entries.append(f"   aircraft%{key}     = {value[j]}")
                inp_lines.append(f"   aircraft%{key}     = {value[0]}")
            else:
                inp_lines.append(f"   aircraft%{key}     = {value}")

        for entry in duplicate_entries:
            inp_lines.append(entry)

        inp_lines.append("\n")

        for propeller_dict in input_dict["propellers"]:
            for_components = propeller_dict.pop("for")
            comment_line = f"!   Propeller({for_components+1}) uses components named Prop_{for_components}, Motor_{for_components}, ESC_{for_components}"
            inp_lines.append(comment_line)
            for key, value in propeller_dict.items():
                inp_lines.append(
                    f"   propeller({for_components+1})%{key}   = {str(value)}"
                )

            inp_lines.append("\n")

        inp_lines.append("!\t Battery(1) is component named: Battery_0")
        for key, value in input_dict["battery"].items():
            inp_lines.append(f"   battery(1)%{key}    = {value}")

        inp_lines.append("\n")

        inp_lines.append("!\t Controls")
        for key, value in input_dict["controls"].items():
            inp_lines.append(f"   control%{key} = {value}")
        inp_lines.append("/\n\n")
        return "\n".join(inp_lines)

    def validate_propellers_directions(self):
        assert (
            self.propeller_0.direction + self.propeller_1.direction == 0
        ), "Propeller 0 and 1 should have opposite directions"
        assert (
            self.propeller_2.direction + self.propeller_3.direction == 0
        ), "Propeller 2 and 3 should have opposite directions"


class QuadSpiderCopter(SeedDesign):
    """The QuadSpiderCopter seed design."""

    __design_vars__ = {
        "arm_length",
        "support_length",
        "arm_a_length",
        "arm_b_length",
        "batt_mount_x_offset",
        "batt_mount_z_offset",
        "bend_angle",
        "q_position",
        "q_velocity",
        "q_angular_velocity",
        "q_angles",
        "r",
    }

    def __init__(
        self,
        arm_length=220.0,
        support_length=155.0,
        arm_a_length=80.0,
        arm_b_length=80.0,
        batt_mount_x_offset=0.0,
        batt_mount_z_offset=0.0,
        bend_angle=120.0,
    ):
        super(QuadSpiderCopter, self).__init__(
            arm_length=arm_length,
            support_length=support_length,
            arm_a_length=arm_a_length,
            arm_b_length=arm_b_length,
            batt_mount_x_offset=batt_mount_x_offset,
            batt_mount_z_offset=batt_mount_z_offset,
            bend_angle=bend_angle,
        )

    arm_length: Union[float, Tuple[float, float]] = Field(
        220.0,
        description="Length of Arm_0, Arm_1, Arm_2, Arm_3 in mm",
        alias="Length_0",
    )

    support_length: Union[float, Tuple[float, float]] = Field(
        155.0,
        description="Length for Support_0, Support_1, Support_2, Support_3 in mm",
        alias="Length_1",
    )

    arm_a_length: Union[float, Tuple[float, float]] = Field(
        80.0,
        description="Length for Arm_0a, Arm_1a, Arm_2a, Arm_3a in mm",
        alias="Length_2",
    )

    arm_b_length: Union[float, Tuple[float, float]] = Field(
        80.0, description="Length of segment Arm_*b in mm", alias="Length_3"
    )

    batt_mount_x_offset: Union[float, Tuple[float, float]] = Field(
        0.0,
        description="X-Offset of the battery mounting position from center of the plate in mm",
        alias="Length_8",
    )

    batt_mount_z_offset: Union[float, Tuple[float, float]] = Field(
        0.0,
        description="Z-Offset of the battery mounting position from center of the plate in mm",
        alias="Length_9",
    )

    bend_angle: Union[float, Tuple[float, float]] = Field(
        120.0,
        description="ANGHORZCONN for Bend_0a, Bend_0b, Bend_1a, Bend_1b, Bend_2a, Bend_2b, Bend_3a, Bend_3b",
        alias="Param_0",
    )

    battery_0: Battery = Field(
        Batteries["TurnigyGraphene1000mAh2S75C"],
        description="Battery_0",
        alias="Battery_0",
    )

    esc_0: ESC = Field(ESCs.ESC_debugging, description="ESC 0", alias="ESC_0")

    esc_1: ESC = Field(ESCs.ESC_debugging, description="ESC 1", alias="ESC_1")

    esc_2: ESC = Field(ESCs.ESC_debugging, description="ESC 2", alias="ESC_2")

    esc_3: ESC = Field(ESCs.ESC_debugging, description="ESC 3", alias="ESC_3")

    motor_0: Motor = Field(
        Motors.kde_direct_KDE2306XF2550, description="Motor 0", alias="Motor_0"
    )

    motor_1: Motor = Field(
        Motors.kde_direct_KDE2306XF2550, description="Motor 0", alias="Motor_1"
    )

    motor_2: Motor = Field(
        Motors.kde_direct_KDE2306XF2550, description="Motor 0", alias="Motor_2"
    )

    motor_3: Motor = Field(
        Motors.kde_direct_KDE2306XF2550, description="Motor 0", alias="Motor_3"
    )

    propeller_0: Propeller = Field(
        Propellers.apc_propellers_10x7E, description="Propeller 0", alias="Prop_0"
    )

    propeller_1: Propeller = Field(
        Propellers.apc_propellers_10x7EP, description="Propeller 1", alias="Prop_1"
    )

    propeller_2: Propeller = Field(
        Propellers.apc_propellers_10x7EP, description="Propeller 2", alias="Prop_2"
    )

    propeller_3: Propeller = Field(
        Propellers.apc_propellers_10x7E, description="Propeller 2", alias="Prop_3"
    )

    flange_0: Flange = Field(
        Flanges["0394_para_flange"], description="Flange 0", alias="Flange_0"
    )

    flange_1: Flange = Field(
        Flanges["0394_para_flange"], description="Flange 1", alias="Flange_1"
    )

    flange_2: Flange = Field(
        Flanges["0394_para_flange"], description="Flange 2", alias="Flange_2"
    )

    flange_3: Flange = Field(
        Flanges["0394_para_flange"], description="Flange 3", alias="Flange_3"
    )

    support_0: Tube = Field(
        Tubes["0394OD_para_tube"], description="Support 0", alias="Support_0"
    )

    support_1: Tube = Field(
        Tubes["0394OD_para_tube"], description="Support 1", alias="Support_1"
    )

    support_2: Tube = Field(
        Tubes["0394OD_para_tube"], description="Support 2", alias="Support_2"
    )

    support_3: Tube = Field(
        Tubes["0394OD_para_tube"], description="Support 3", alias="Support_3"
    )

    arm_0: Tube = Field(Tubes["0394OD_para_tube"], description="Arm 0", alias="Arm_0")

    arm_1: Tube = Field(Tubes["0394OD_para_tube"], description="Arm 1", alias="Arm_1")

    arm_2: Tube = Field(Tubes["0394OD_para_tube"], description="Arm 2", alias="Arm_2")

    arm_3: Tube = Field(Tubes["0394OD_para_tube"], description="Arm 3", alias="Arm_3")

    arm_0a: Tube = Field(
        Tubes["0394OD_para_tube"], description="Arm 0-A", alias="Arm_0a"
    )

    arm_0b: Tube = Field(
        Tubes["0394OD_para_tube"], description="Arm 0-B", alias="Arm_0b"
    )

    arm_1a: Tube = Field(
        Tubes["0394OD_para_tube"], description="Arm 1-A", alias="Arm_1a"
    )

    arm_1b: Tube = Field(
        Tubes["0394OD_para_tube"], description="Arm 1-B", alias="Arm_1b"
    )

    arm_2a: Tube = Field(
        Tubes["0394OD_para_tube"], description="Arm 2-A", alias="Arm_2a"
    )

    arm_2b: Tube = Field(
        Tubes["0394OD_para_tube"], description="Arm 2-B", alias="Arm_2b"
    )

    arm_3a: Tube = Field(
        Tubes["0394OD_para_tube"], description="Arm 3-A", alias="Arm_3a"
    )

    arm_3b: Tube = Field(
        Tubes["0394OD_para_tube"], description="Arm 3-B", alias="Arm_3b"
    )

    orient: Orient = Field(Orients["Orient"], description="Orient", alias="Orient")

    para_cf_plate: CarbonFiberPlate = Field(
        CFPs["para_cf_fplate"], description="Carbon fiber plate", alias="para_cf_fplate"
    )

    hub_4_way: Hub = Field(
        Hubs["0394od_para_hub_4"], description="Hub 4 way", alias="Hub_4Way"
    )

    bend_0a: Hub = Field(
        Hubs["0394od_para_hub_2"], description="Bend 0-A", alias="Bend_0a"
    )

    bend_0b: Hub = Field(
        Hubs["0394od_para_hub_2"], description="Bend 0-B", alias="Bend_0b"
    )

    bend_1a: Hub = Field(
        Hubs["0394od_para_hub_2"], description="Bend 1-A", alias="Bend_1a"
    )

    bend_1b: Hub = Field(
        Hubs["0394od_para_hub_2"], description="Bend 1-B", alias="Bend_0a"
    )

    bend_2a: Hub = Field(
        Hubs["0394od_para_hub_2"], description="Bend 2-A", alias="Bend_2a"
    )

    bend_2b: Hub = Field(
        Hubs["0394od_para_hub_2"], description="Bend 2-B", alias="Bend_2b"
    )

    bend_3a: Hub = Field(
        Hubs["0394od_para_hub_2"], description="Bend 3-A", alias="Bend_3a"
    )

    bend_3b: Hub = Field(
        Hubs["0394od_para_hub_2"], description="Bend 3-B", alias="Bend_3b"
    )

    def validate_propellers_directions(self):
        assert (
            self.propeller_0.direction + self.propeller_1.direction == 0
        ), "Propeller 0 and 1 should have opposite directions"
        assert (
            self.propeller_2.direction + self.propeller_3.direction == 0
        ), "Propeller 2 and 3 should have opposite directions"

    @validator(*__design_vars__, pre=True, always=True)
    def validate_design_vars_tuple(cls, value):
        if isinstance(value, Tuple):
            assert (
                value[0] <= value[1]
            ), "The first element should be less than the second one; while using ranges"
        return value


class HCopter(SeedDesign):
    """The H-Copter Seed Design"""

    __design_vars__ = {
        "arm_length",
        "support_length",
        "batt_mount_x_offset",
        "batt_mount_z_offset",
        "q_position",
        "q_velocity",
        "q_angular_velocity",
        "q_angles",
        "r",
    }

    def __init__(
        self,
        arm_length=500.0,
        support_length=95.0,
        batt_mount_x_offset=0.0,
        batt_mount_z_offset=0.0,
    ):
        super(HCopter, self).__init__(
            arm_length=arm_length,
            support_length=support_length,
            batt_mount_x_offset=batt_mount_x_offset,
            batt_mount_z_offset=batt_mount_z_offset,
        )

    arm_length: Union[float, Tuple[float, float]] = Field(
        500.0,
        description="Length of Arm_0, Arm_1, Arm_2, Arm_3 in mm (default 500)",
        alias="Length_0",
    )

    support_length: Union[float, Tuple[float, float]] = Field(
        95.0,
        description="Length of Support_0, Support_1, Support_2, Support_3 in mm (default 95)",
        alias="Length_1",
    )

    batt_mount_x_offset: Union[float, Tuple[float, float]] = Field(
        0.0,
        description="X Offset of battery mounting position from center of plate in mm (default 0)",
        alias="Length_8",
    )

    batt_mount_z_offset: Union[float, Tuple[float, float]] = Field(
        0.0,
        description="Z Offset of battery mounting position from center of plate in mm (default 0)",
        alias="Length_9",
    )

    battery_0: Battery = Field(
        Batteries["TurnigyGraphene1000mAh2S75C"],
        description="Battery",
        alias="Battery_0",
    )

    esc_0: ESC = Field(ESCs.ESC_debugging, description="ESC 0", alias="ESC_0")

    esc_1: ESC = Field(ESCs.ESC_debugging, description="ESC 1", alias="ESC_1")

    esc_2: ESC = Field(ESCs.ESC_debugging, description="ESC 2", alias="ESC_2")

    esc_3: ESC = Field(ESCs.ESC_debugging, description="ESC 3", alias="ESC_3")

    motor_0: Motor = Field(
        Motors.kde_direct_KDE2306XF2550, description="Motor 0", alias="Motor_0"
    )

    motor_1: Motor = Field(
        Motors.kde_direct_KDE2306XF2550, description="Motor 0", alias="Motor_1"
    )

    motor_2: Motor = Field(
        Motors.kde_direct_KDE2306XF2550, description="Motor 0", alias="Motor_2"
    )

    motor_3: Motor = Field(
        Motors.kde_direct_KDE2306XF2550, description="Motor 0", alias="Motor_3"
    )

    propeller_0: Propeller = Field(
        Propellers.apc_propellers_4_75x4_75E, description="Propeller 0", alias="Prop_0"
    )

    propeller_1: Propeller = Field(
        Propellers.apc_propellers_4_75x4_75EP, description="Propeller 1", alias="Prop_1"
    )

    propeller_2: Propeller = Field(
        Propellers.apc_propellers_4_75x4_75EP, description="Propeller 2", alias="Prop_2"
    )

    propeller_3: Propeller = Field(
        Propellers.apc_propellers_4_75x4_75E, description="Propeller 2", alias="Prop_3"
    )

    flange_0: Flange = Field(
        Flanges["0394_para_flange"], description="Flange 0", alias="Flange_0"
    )

    flange_1: Flange = Field(
        Flanges["0394_para_flange"], description="Flange 1", alias="Flange_1"
    )

    flange_2: Flange = Field(
        Flanges["0394_para_flange"], description="Flange 2", alias="Flange_2"
    )

    flange_3: Flange = Field(
        Flanges["0394_para_flange"], description="Flange 3", alias="Flange_3"
    )

    support_0: Tube = Field(
        Tubes["0394OD_para_tube"], description="Support 0", alias="Support_0"
    )

    support_1: Tube = Field(
        Tubes["0394OD_para_tube"], description="Support 1", alias="Support_1"
    )

    support_2: Tube = Field(
        Tubes["0394OD_para_tube"], description="Support 2", alias="Support_2"
    )

    support_3: Tube = Field(
        Tubes["0394OD_para_tube"], description="Support 3", alias="Support_3"
    )

    arm_right_center: Tube = Field(
        Tubes["0394OD_para_tube"], description="Right Center Arm", alias="Arm_RightCtr"
    )

    arm_left_center: Tube = Field(
        Tubes["0394OD_para_tube"], description="Left Center Arm", alias="Arm_LeftCtr"
    )

    orient: Orient = Field(Orients["Orient"], description="Orient", alias="Orient")

    para_cf_plate: CarbonFiberPlate = Field(
        CFPs["para_cf_fplate"], description="Carbon fiber plate", alias="para_cf_fplate"
    )

    right_hub_4_way: Hub = Field(
        Hubs["0394od_para_hub_4"], description="The Right Hub", alias="RightHub_4Way"
    )

    left_hub_4_way: Hub = Field(
        Hubs["0394od_para_hub_4"], description="The Left Hub", alias="LeftHub_4Way"
    )

    center_hub_4_way: Hub = Field(
        Hubs["0394od_para_hub_4"], description="The Center Hub", alias="CtrHub_4Way"
    )

    @validator(*__design_vars__, pre=True, always=True)
    def validate_design_vars_tuple(cls, value):
        if isinstance(value, Tuple):
            assert (
                value[0] <= value[1]
            ), "The first element should be less than the second one; while using ranges"
        return value

    def validate_propellers_directions(self):
        assert (
            self.propeller_0.direction + self.propeller_1.direction == 0
        ), "Propeller 0 and 1 should have opposite directions"
        assert (
            self.propeller_2.direction + self.propeller_3.direction == 0
        ), "Propeller 2 and 3 should have opposite directions"


class HPlane(SeedDesign):
    """The H-Plane Seed Design"""

    __design_vars__ = {
        "tube_length",
        "batt_mount_x_offset",
        "batt_mount_z_offset",
        "q_position",
        "q_velocity",
        "q_angular_velocity",
        "q_angles",
        "r",
    }

    def __init__(
        self, tube_length=320.0, batt_mount_x_offset=0.0, batt_mount_z_offset=0.0
    ):
        super(HPlane, self).__init__(
            tube_length=tube_length,
            batt_mount_x_offset=batt_mount_x_offset,
            batt_mount_z_offset=batt_mount_z_offset,
        )

    tube_length: Union[float, Tuple[float, float]] = Field(
        320.0,
        description="Length for Body_Tube_Front_L, Body_Tube_Front_R, "
        "Body_Tube_Rear_L, Body_Tube_Rear_R in mm (default 320) "
        "Length in x. Do not put props under wings",
        alias="Length_1",
    )

    batt_mount_x_offset: Union[float, Tuple[float, float]] = Field(
        0.0,
        description="X Offset of battery mounting position from center of plate in mm (default 0)",
        alias="Length_8",
    )

    batt_mount_z_offset: Union[float, Tuple[float, float]] = Field(
        0.0,
        description="Z Offset of battery mounting position from center of plate in mm (default 0)",
        alias="Length_9",
    )

    orient: Orient = Field(Orients["Orient"], description="Orient", alias="Orient")

    para_cf_plate: CarbonFiberPlate = Field(
        CFPs["para_cf_fplate"], description="Parametric CF Plate", alias="Plate_0"
    )

    servo_l: Servo = Field(
        Servos["Hitec_D485HW"], description="Left Servo", alias="Servo_L"
    )

    servo_r: Servo = Field(
        Servos["Hitec_D485HW"], description="Right Servo", alias="Servo_R"
    )

    left_wing: Wing = Field(
        Wings["left_NACA_0006"], description="Left Wing", alias="Left_Wing"
    )

    right_wing: Wing = Field(
        Wings["left_NACA_0006"], description="Left Wing", alias="Left_Wing"
    )

    central_hub: Hub = Field(
        Hubs["0394od_para_hub_4"], description="The Central Hub", alias="Central_Hub"
    )

    rear_hub_l: Hub = Field(
        Hubs["0394od_para_hub_3"], description="The left rear hub", alias="Rear_Hub_L"
    )

    rear_hub_r: Hub = Field(
        Hubs["0394od_para_hub_3"], description="The right rear hub", alias="Rear_Hub_R"
    )

    front_hub_l: Hub = Field(
        Hubs["0394od_para_hub_3"], description="The left front hub", alias="Front_Hub_L"
    )

    front_hub_r: Hub = Field(
        Hubs["0394od_para_hub_3"],
        description="The right front hub",
        alias="Front_Hub_R",
    )

    wing_body_hub_l: Hub = Field(
        Hubs["0394od_para_hub_3"],
        description="The left wing-body hub",
        alias="Wing_Body_Hub_L",
    )

    wing_body_hub_r: Hub = Field(
        Hubs["0394od_para_hub_3"],
        description="The right wing-body hub",
        alias="Wing_Body_Hub_R",
    )

    vertical_l: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The left vertical leg tube",
        alias="Vertical_L",
    )

    vertical_r: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The right vertical leg tube",
        alias="Vertical_R",
    )

    leg_rear_l: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The left rear leg tube",
        alias="Leg_Rear_L",
    )

    leg_rear_r: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The right rear leg tube",
        alias="Leg_Rear_R",
    )

    leg_front_l: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The left front leg tube",
        alias="Leg_Front_L",
    )

    leg_front_r: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The right front leg tube",
        alias="Leg_Front_R",
    )

    body_tube_rear_l: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The rear body tube(left)",
        alias="Body_Tube_Rear_L",
    )

    body_tube_rear_r: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The rear body tube(right)",
        alias="Body_Tube_Rear_R",
    )

    body_tube_front_l: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The front body tube(left)",
        alias="Body_Tube_Front_L",
    )

    body_tube_front_r: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The front body tube(right)",
        alias="Body_Tube_Front_R",
    )

    center_tube_l: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The center tube(left)",
        alias="Center_Tube_L",
    )

    center_tube_r: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The center tube(right)",
        alias="Center_Tube_R",
    )

    front_tube_l: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The front tube(left)",
        alias="Front_Tube_L",
    )

    front_tube_c: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The front tube(Center)",
        alias="Front_Tube_C",
    )

    front_tube_r: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The front tube(right)",
        alias="Front_Tube_R",
    )

    rear_tube_l: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The rear tube(left)",
        alias="Rear_Tube_L",
    )

    rear_tube_c: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The rear tube(Center)",
        alias="Rear_Tube_C",
    )

    rear_tube_r: Tube = Field(
        Tubes["0394OD_para_tube"],
        description="The rear tube(right)",
        alias="Rear_Tube_R",
    )

    front_flange_l: Flange = Field(
        Flanges["0394_para_flange"],
        description="The Front left flange",
        alias="Front_Flange_L",
    )

    front_flange_c: Flange = Field(
        Flanges["0394_para_flange"],
        description="The Front center flange",
        alias="Front_Flange_C",
    )

    front_flange_r: Flange = Field(
        Flanges["0394_para_flange"],
        description="The Front right flange",
        alias="Front_Flange_R",
    )

    rear_flange_l: Flange = Field(
        Flanges["0394_para_flange"],
        description="The rear left flange",
        alias="Rear_Flange_L",
    )

    rear_flange_r: Flange = Field(
        Flanges["0394_para_flange"],
        description="The rear right flange",
        alias="Rear_Flange_R",
    )

    front_prop_c: Propeller = Field(
        Propellers.apc_propellers_4_75x4_75EC,
        description="The front-center propeller",
        alias="Front_Prop_C",
    )

    front_prop_l: Propeller = Field(
        Propellers.apc_propellers_4_75x4_75E,
        description="The front-left propeller",
        alias="Front_Prop_L",
    )

    front_prop_r: Propeller = Field(
        Propellers.apc_propellers_4_75x4_75EP,
        description="The front-right propeller",
        alias="Front_Prop_R",
    )

    rear_prop_l: Propeller = Field(
        Propellers.apc_propellers_4_75x4_75EP,
        description="The rear-left propeller",
        alias="Rear_Prop_L",
    )

    rear_prop_r: Propeller = Field(
        Propellers.apc_propellers_4_75x4_75E,
        description="The rear-right propeller",
        alias="Rear_Prop_R",
    )

    front_motor_l: Motor = Field(
        Motors.kde_direct_KDE2306XF2550,
        description="The Front left Motor",
        alias="Front_Motor_L",
    )

    front_motor_r: Motor = Field(
        Motors.kde_direct_KDE2306XF2550,
        description="The Front right Motor",
        alias="Front_Motor_R",
    )

    front_motor_c: Motor = Field(
        Motors.kde_direct_KDE2306XF2550,
        description="The Front center Motor",
        alias="Front_Motor_C",
    )

    rear_motor_l: Motor = Field(
        Motors.kde_direct_KDE2306XF2550,
        description="The rear left Motor",
        alias="Rear_Motor_L",
    )

    rear_motor_r: Motor = Field(
        Motors.kde_direct_KDE2306XF2550,
        description="The rear right Motor",
        alias="Rear_Motor_R",
    )

    front_esc_l: ESC = Field(
        ESCs.t_motor_AIR_40A,
        description="The front-left controller",
        alias="Front_ESC_L",
    )

    front_esc_r: ESC = Field(
        ESCs.t_motor_AIR_40A,
        description="The front-right controller",
        alias="Front_ESC_R",
    )

    front_esc_c: ESC = Field(
        ESCs.t_motor_AIR_40A,
        description="The front-center controller",
        alias="Front_ESC_C",
    )

    rear_esc_l: ESC = Field(
        ESCs.t_motor_AIR_40A, description="The rear-left controller", alias="Rear_ESC_L"
    )

    rear_esc_r: ESC = Field(
        ESCs.t_motor_AIR_40A,
        description="The rear-right controller",
        alias="Rear_ESC_R",
    )

    battery_0: Battery = Field(
        Batteries.TurnigyGraphene2200mAh3S75C,
        description="The battery",
        alias="Battery_0",
    )

    @validator(*__design_vars__, pre=True, always=True)
    def validate_design_vars_tuple(cls, value):
        if isinstance(value, Tuple):
            assert (
                value[0] <= value[1]
            ), "The first element should be less than the second one; while using ranges"
        return value


class HexRing(SeedDesign):
    pass
