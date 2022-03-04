import csv
import json
from typing import ClassVar, Dict, Optional, Tuple, Union

from pydantic import BaseModel, Field, root_validator, validator

from symbench_athens_client.utils import (
    get_data_file_path,
    inject_none_for_missing_fields_and_nans,
)


class Component(BaseModel):
    """The Base Component Class"""

    __swap_aliases__: ClassVar[Dict[str, str]] = {}

    name: str = Field(
        ...,
        description="The name of the component as is in the graph database",
        alias="Name",
    )

    model: str = Field(..., description="Model name of the Component", alias="MODEL")

    classification: str = Field(
        "Battery",
        description="The component type for this battery. Redundant but useful info",
        alias="Classification",
    )

    corpus: str = Field(
        ..., description="The corpus for which this element belongs to", alias="Corpus"
    )

    @property
    def prt_file(self) -> Optional[str]:
        return None

    def __repr__(self):
        return f"<{self.__class__.__name__}, Category: {self.classification}, Name: {self.name}>"

    def __str__(self):
        return repr(self)

    @root_validator(pre=True)
    def inject_model(cls, values):
        if "Model" in values:
            values["MODEL"] = values.pop("Model")

        if not values.get("model", values.get("MODEL", values.get("Model"))):
            values["model"] = values.get("name", values.get("Name"))

        for original, replace in cls.__swap_aliases__.items():
            if original in values:
                values[replace] = values.pop(original)

        return values

    @validator("corpus")
    def check_corpus(cls, corpus):
        if corpus not in {"uav", "uam"}:
            raise ValueError("Corpus can only be either `uav` or `uam`")
        return corpus

    class Config:
        allow_mutation = False
        allow_population_by_field_name = True
        extra = "forbid"


class Battery(Component):
    __swap_aliases__ = {"BASE_VOLTAGE": "VOLTAGE"}

    """The Battery Component
    An example of a battery attributes in the Graph database is shown below:


    "PEAK_DISCHARGE_RATE": "150",
    "NUMBER_OF_CELLS": "4S1P",
    "THICKNESS": "34",
    "CONT_DISCHARGE_RATE": "75",
    "VOLTAGE": "14.8",
    "CAPACITY": "6000",
    "DISCHARGE_PLUG": "XT90",
    "WIDTH": "69",
    "CHEMISTRY_TYPE": "LiPo",
    "COST": "99.8",
    "PACK_RESISTANCE": "9.0",
    "MODEL": "TurnigyGraphene6000mAh4S75C",
    "WEIGHT": "0.8",
    "LENGTH": "168.0",
    "Classification": "Battery"
    """
    battery_type: Optional[str] = Field(
        default=None, alias="BATTERY_TYPE", description="The Battery Type"
    )

    peak_discharge_rate: float = Field(
        ...,
        description="Peak Discharge rate of the Battery",
        alias="PEAK_DISCHARGE_RATE",
    )

    number_of_cells: Optional[str] = Field(
        None, description="Number of cells", alias="NUMBER_OF_CELLS"
    )

    thickness: float = Field(..., description="Thickness", alias="THICKNESS")

    cont_discharge_rate: float = Field(
        ..., description="Continuous Discharge Rate", alias="CONT_DISCHARGE_RATE"
    )

    voltage: float = Field(..., description="Voltage", alias="VOLTAGE")

    capacity: float = Field(
        ..., description="Capacity of the Battery", alias="CAPACITY"
    )

    discharge_plug: Optional[str] = Field(
        None, description="Discharge Plug Details", alias="DISCHARGE_PLUG"
    )

    width: Optional[float] = Field(
        None, description="Width of the Battery", alias="WIDTH"
    )

    chemistry_type: Optional[str] = Field(
        None, description="Chemistry Type of the Battery", alias="CHEMISTRY_TYPE"
    )

    cost: Optional[float] = Field(None, description="Cost of the Battery", alias="COST")

    pack_resistance: Optional[float] = Field(
        None, description="Pack Resistance of the Battery", alias="PACK_RESISTANCE"
    )

    weight: Optional[float] = Field(
        None,
        description="Weight of the Battery",
        alias="WEIGHT",
    )

    length: Optional[float] = Field(
        None, description="Length of the Battery", alias="LENGTH"
    )

    chord_1: Optional[float] = Field(None, description="Chord 1", alias="CHORD_1")

    chord_2: Optional[float] = Field(None, description="Chord 2", alias="CHORD_2")

    module_mass: Optional[float] = Field(
        None, description="Module Mass", alias="MODULE_MASS"
    )

    module_volume: Optional[float] = Field(
        None, description="Module Volume", alias="MODULE_VOLUME"
    )

    mount_side: Optional[float] = Field(
        None, description="Mount Side", alias="MOUNT_SIDE"
    )

    span: Optional[float] = Field(None, description="Span", alias="SPAN")

    taper_offset: Optional[float] = Field(
        None, description="TAPER_OFFSET", alias="TAPER_OFFSET"
    )

    voltage_request: Optional[float] = Field(
        None, description="Voltage Request", alias="VOLTAGE_REQUEST"
    )

    volume_percent: Optional[float] = Field(
        None, description="VOLUME_PERCENT", alias="VOLUME_PERCENT"
    )

    @property
    def prt_file(self) -> Optional[str]:
        return "para_battery.prt"

    def to_fd_inp(self):
        return {
            "num_cells": int(self.number_of_cells[0]),
            "voltage": self.voltage,
            "capacity": self.capacity,
            "C_Continuous": self.cont_discharge_rate,
            "C_Peak": self.peak_discharge_rate,
        }

    @root_validator(pre=True)
    def validate_fields(cls, values):
        if "Chemistry Type" in values:
            values["CHEMISTRY_TYPE"] = values.pop("Chemistry Type")
        if "Discharge Plug" in values:
            values["DISCHARGE_PLUG"] = values.pop("Discharge Plug")
        if "Number of Cells" in values:
            values["NUMBER_OF_CELLS"] = values.pop("Number of Cells")
        return values


class BatteryController(Component):
    input_voltage: float = Field(
        ..., description="Input Voltage", alias="Input_Voltage"
    )

    output_voltage: float = Field(
        ..., description="Output Voltage", alias="Output_Voltage"
    )


class Propeller(Component):
    """The propeller component

    An example of a propeller attributes can be seen below:
    "PITCH": "226.06",
    "SHAFT_DIAMETER": "6.35",
    "HUB_THICKNESS": "15.24",
    "Performance_File": "PER3_88x89.dat",
    "DIAMETER": "223.52",
    "Direction": "1",
    "Weight": "0.02608",
    "MODEL": "apc_propellers_8_8x8_9",
    "Classification": "Propeller"
    """

    hub_thickness: float = Field(
        ..., description="HUB_THICKNESS", alias="HUB_THICKNESS"
    )

    diameter: float = Field(..., description="Diameter", alias="DIAMETER")

    direction: int = Field(..., description="Direction", alias="Direction")

    performance_file: str = Field(
        ..., description="Performance file location/name", alias="Performance_File"
    )

    shaft_diameter: float = Field(
        ..., description="The shaft diameter of the propeller", alias="SHAFT_DIAMETER"
    )

    pitch: float = Field(..., description="The pitch of the propeller", alias="PITCH")

    weight: float = Field(..., description="Weight of the propeller", alias="WEIGHT")

    prop_type: Optional[int] = Field(
        default=None, description="The propeller type", alias="Prop_type"
    )

    @property
    def prt_file(self) -> Optional[str]:
        return "para_prop.prt"

    def to_fd_inp(self, data_path):
        return {
            "cname": f"'{self.name}'",
            "ctype": "'MR'",
            "prop_fname": f"'{str(data_path)}{self.performance_file}'"
            if data_path
            else f"'{self.performance_file}'",
            "Ir": (self.weight * self.diameter**2 / 12.0),
            "x": None,
            "y": None,
            "z": None,
            "nx": None,
            "ny": None,
            "nz": None,
            "radius": self.diameter / 2,
            "spin": int(self.direction),
        }

    @root_validator(pre=True)
    def validate_propeller_attributes(cls, values):
        if "Weight" in values:
            values["WEIGHT"] = values.pop("Weight")
        return values


class Motor(Component):
    """The Motor Component in the graph database

    An example of motor attributes is shown below:

    "MAX_POWER": "44.0",
    "TOTAL_LENGTH": "26.0",
    "CAN_DIAMETER": "17.7",
    "IO_IDLE_CURRENT@10V": "0.2",
    "SHAFT_DIAMETER": "4.0",
    "KT": "0.0030804182533915227",
    "Max # of Cells": "2.0",
    "LENGTH": "12.0",
    "PROP_PITCH_REC.": "2,3",
    "PROP_SIZE_REC.": "6,7",
    "MODEL": "MT13063100KV",
    "ESC/BEC Class": "3.0",
    "CAN_LENGTH": "6.0",
    "KM": "0.012371257411140733",
    "INTERNAL_RESISTANCE": "62.0",
    "Min # of Cells": "1.0",
    "MAX_CURRENT": "6.0",
    "COST": "41.9",
    "CONTROL_CHANNEL": "none",
    "WEIGHT": "0.0112",
    "KV": "3100.0",
    "Poles": "9N12P",
    "Classification": "Motor"
    """

    __swap_aliases__ = {
        "ESC/BEC Class": "ESC_BEC_Class",
        "Max # of Cells": "Max_Cells",
        "Min # of Cells": "Min_Cells",
        "IO_IDLE_CURRENT@10V": "IO_IDLE_CURRENT_10V",
        "PROP_SIZE_REC.": "PROP_SIZE_REC",
        "PROP_PITCH_REC.": "PROP_PITCH_REC",
    }

    max_power: float = Field(
        ..., description="Max power of the motor", alias="MAX_POWER"
    )

    io_idle_current_at_10V: float = Field(
        ..., description="Maximum idle current at 10V", alias="IO_IDLE_CURRENT_10V"
    )

    length: float = Field(..., description="Length of the Motor", alias="LENGTH")

    kt: float = Field(..., description="The KT rating of the Motor", alias="KT")

    esc_bec_class: Optional[float] = Field(
        ..., description="The ESC/BEC Class", alias="ESC_BEC_Class"
    )

    can_length: float = Field(..., description="The can length", alias="CAN_LENGTH")

    total_length: float = Field(..., description="Total length", alias="TOTAL_LENGTH")

    km: float = Field(..., description="KM rating of the motor", alias="KM")

    shaft_diameter: float = Field(
        ..., description="The shaft diameter of the motor", alias="SHAFT_DIAMETER"
    )

    weight: float = Field(..., description="Weight of the motor", alias="WEIGHT")

    poles: Optional[str] = Field(
        ..., description="The poles of the motor", alias="Poles"
    )

    internal_resistance: float = Field(
        ..., description="Internal Resistance of the motor", alias="INTERNAL_RESISTANCE"
    )

    control_channel: int = Field(
        ..., description="The control channel", alias="CONTROL_CHANNEL"
    )

    adapter_length: Optional[Union[float, Tuple[float, float]]] = Field(
        ..., description="The adapter length", alias="ADAPTER_LENGTH"
    )

    max_current: float = Field(
        ..., description="Max current rating of the motor", alias="MAX_CURRENT"
    )

    max_no_cells: int = Field(
        ..., description="Max number of cells in the motor", alias="Max_Cells"
    )

    kv: float = Field(..., description="The KV rating of the motor", alias="KV")

    cost: float = Field(..., description="Cost of the motor", alias="COST")

    can_diameter: float = Field(
        ..., description="The can diameter of the motor", alias="CAN_DIAMETER"
    )

    min_no_cells: int = Field(
        ...,
        description="The minimum number of cells of the motor",
        alias="Min_Cells",
    )

    prop_size_rec: Optional[Union[float, Tuple[float, float]]] = Field(
        ...,
        description="The propsize rec",
        alias="PROP_SIZE_REC",
    )

    prop_pitch_rec: Optional[Union[float, Tuple[float, float]]] = Field(
        ..., description="The prop pitch rec", alias="PROP_PITCH_REC"
    )

    esc_pwm_rate_min: Optional[float] = Field(
        ..., description="ESC_PWM_RATE_MIN", alias="ESC_PWM_RATE_MIN"
    )

    adapter_diameter: Optional[Union[float, Tuple[float, float]]] = Field(
        ..., description="Adapter diameter", alias="ADAPTER_DIAMETER"
    )

    esc_pwm_rate_max: Optional[float] = Field(
        ..., description="ESC PWM RATE MAX", alias="ESC_PWM_RATE_MAX"
    )

    cost_adapter: Optional[float] = Field(
        ...,
        description="Adapter Cost",
        alias="COST_ADAPTER",
    )

    esc_rate: Optional[float] = Field(..., description="ESC_RATE", alias="ESC_RATE")

    @property
    def prt_file(self):
        return "para_motor.prt"

    def to_fd_inp(self):
        return {
            "motor_fname": f"'../../Motors/{self.name}'",
            "KV": self.kv,
            "KT": self.kt,
            "I_max": self.max_current,
            "I_idle": self.io_idle_current_at_10V,
            "maxpower": self.max_power,
            "Rw": self.internal_resistance / 1000.0,
            "icontrol": None,
            "ibattery": None,
        }

    @validator("prop_size_rec", pre=True, always=True)
    def validate_prop_pitch(cls, value):
        if isinstance(value, str) and "," in value:
            value = tuple(float(v) for v in value.split(","))
        return value

    @validator("prop_pitch_rec", pre=True, always=True)
    def validate_prop_length(cls, value):
        if isinstance(value, str) and "," in value:
            value = tuple(float(v) for v in value.split(","))
        return value

    @validator("adapter_diameter", pre=True, always=True)
    def validate_adapter_diameter(cls, value):
        if isinstance(value, str) and "," in value:
            value = tuple(float(v) for v in value.split(","))
        return value

    @validator("adapter_length", pre=True, always=True)
    def validate_adapter_length(cls, value):
        if isinstance(value, str) and "," in value:
            value = tuple(float(v) for v in value.split(","))
        return value

    @validator("max_no_cells", "min_no_cells", pre=True, always=True)
    def validate_int(cls, cell):
        return int(float(cell))

    @root_validator(pre=True)
    def validate_fields(cls, values):
        if "CONTROL_CHANNEL" in values and values["CONTROL_CHANNEL"] == "none":
            values["CONTROL_CHANNEL"] = None

        return inject_none_for_missing_fields_and_nans(cls, values)


class ESC(Component):
    length: float = Field(..., description="Length of the ESC", alias="LENGTH")

    cont_amps: Optional[float] = Field(
        ..., description="Continuous ampere ratings", alias="CONT_AMPS"
    )

    max_voltage: float = Field(..., description="Maximum voltage", alias="MAX_VOLTAGE")

    bec: Optional[Union[float, Tuple]] = Field(
        ..., description="BEC_RATING", alias="BEC"
    )

    bec_output_cont_amps: Optional[Union[float, Tuple]] = Field(
        ...,
        description="Bec Output in continuous amps",
        alias="BEC_OUTPUT_CONT_AMPS",
    )

    bec_output_peak_amps: Optional[float] = Field(
        ..., description="Bec output peak amps", alias="BEC_OUTPUT_PEAK_AMPS"
    )

    cost: float = Field(..., description="Cost of the ESC Component", alias="COST")

    bec_output_voltage: Optional[Union[float, Tuple]] = Field(
        ..., description="Bec output voltage", alias="BEC_OUTPUT_VOLTAGE"
    )

    control_channel: int = Field(
        ..., description="Control Channel", alias="CONTROL_CHANNEL"
    )

    esc_bec_class: Optional[float] = Field(
        ..., description="The ESC/BEC Class", alias="ESC/BEC Class"
    )

    thickness: float = Field(..., description="THICKNESS", alias="THICKNESS")

    offset: float = Field(..., description="Offset", alias="Offset")

    mount_angle: float = Field(..., description="The mount angle", alias="Mount_Angle")

    tube_od: float = Field(..., description="The tube OD", alias="TUBE_OD")

    width: float = Field(..., description="The width of ESC", alias="WIDTH")

    weight: float = Field(..., description="The weight of ESC", alias="WEIGHT")

    peak_amps: Optional[float] = Field(
        ...,
        description="The Peak ampere ratings for the ESC controller",
        alias="PEAK_AMPS",
    )

    @property
    def prt_file(self):
        return "para_esc.prt"

    @validator("bec", pre=True, always=True)
    def validate_bec(cls, value):
        if isinstance(value, str) and "," in value:
            value = tuple(float(v) for v in value.split(","))
        return value

    @validator("bec_output_voltage", pre=True, always=True)
    def validate_bec_output_voltage(cls, value):
        if isinstance(value, str) and "," in value:
            value = tuple(float(v) for v in value.split(","))
        return value

    @validator("bec_output_cont_amps", pre=True, always=True)
    def validate_bec_output_cont_amps(cls, value):
        if isinstance(value, str) and "," in value:
            value = tuple(float(v) for v in value.split(","))
        return value

    @root_validator(pre=True)
    def validate_fields(cls, values):
        if "Control_Channel" in values:
            values["CONTROL_CHANNEL"] = values.pop("Control_Channel")
        for field in ["Offset", "Mount_Angle", "CONTROL_CHANNEL", "TUBE_OD"]:
            if field in values and values[field] == "none":
                values[field] = None
        return inject_none_for_missing_fields_and_nans(cls, values)


class Instrument_Battery(Battery):
    """The Instrument Battery Component"""

    @property
    def prt_file(self) -> Optional[str]:
        return None


class Wing(Component):
    """The Wing Component"""

    span: float = Field(..., description="SPAN property", alias="SPAN")

    aileron_bias: Optional[float] = Field(..., description="BIAS", alias="AILERON_BIAS")

    aoa_cl_max: Optional[float] = Field(
        None, description="AoA_CL_Max", alias="AoA_CL_Max"
    )

    offset: Optional[float] = Field(None, description="OFFSET", alias="OFFSET")

    control_channel_flaps: Optional[int] = Field(
        None, description="CONTROL_CHANNEL_FLAPS", alias="CONTROL_CHANNEL_FLAPS"
    )

    cl_max: Optional[float] = Field(None, description="CL_Max", alias="CL_Max")

    cl_max_cd0_min: Optional[float] = Field(
        None, description="CL_Max_CD0_Min", alias="CL_Max_CD0_Min"
    )

    last_two: Optional[float] = Field(None, description="LAST_TWO", alias="LASTTWO")

    chord: Optional[float] = Field(None, description="CHORD", alias="CHORD")

    tube_offset: Optional[float] = Field(
        None, description="Tube Offset", alias="TUBE_OFFSET"
    )

    cl_ld_max: Optional[float] = Field(None, description="CL_LD_Max", alias="CL_LD_Max")

    servo_width: Optional[float] = Field(
        None, description="Servo Width", alias="SERVO_WIDTH"
    )

    aoa_l0: Optional[float] = Field(None, description="AOA_L0", alias="AoA_L0")

    dcl_daoa_slope: Optional[float] = Field(
        None, description="dCl_dAoA_Slope", alias="dCl_dAoA_Slope"
    )

    control_channel_ailerons: Optional[int] = Field(
        None, description="CONTROL_CHANNEL_AILERONS", alias="CONTROL_CHANNEL_AILERONS"
    )

    diameter: Optional[float] = Field(None, description="DIAMETER", alias="DIAMETER")

    ld_max: Optional[float] = Field(None, description="LD_Max", alias="LD_Max")

    servo_length: Optional[float] = Field(
        None, description="SERVO_LENGTH", alias="SERVO_LENGTH"
    )

    cd0_min: Optional[float] = Field(None, description="CD0_MIn", alias="CD0_Min")

    cd_min: Optional[float] = Field(None, description="CD_MIN", alias="CD_Min")

    cm0: Optional[float] = Field(None, description="CM0", alias="CM0")

    flap_bias: float = Field(..., description="Flap Bias", alias="FLAP_BIAS")

    chord_1: Optional[float] = Field(None, description="Chord 1", alias="CHORD_1")

    chord_2: Optional[float] = Field(None, description="Chord 1", alias="CHORD_2")

    load: Optional[float] = Field(None, description="Load", alias="LOAD")

    naca_profile: Optional[str] = Field(
        None, description="NACA Profile", alias="NACA_Profile"
    )

    taper_offset: Optional[float] = Field(
        None, description="Taper Offset", alias="TAPER_OFFSET"
    )

    thickness: Optional[float] = Field(None, description="Thickness", alias="THICKNESS")

    @property
    def prt_file(self):
        return (
            "para_wing_left.prt"
            if self.name.startswith("left")
            else "para_wing_right.prt"
        )

    @root_validator(pre=True)
    def validate_fields(cls, values):
        for field in [
            "SPAN",
            "AILERON_BIAS",
            "OFFSET",
            "SERVO_WIDTH",
            "SERVO_LENGTH",
            "CONTROL_CHANNEL_FLAPS",
            "DIAMETER",
            "FLAP_BIAS",
            "TUBE_OFFSET",
            "CONTROL_CHANNEL_AILERONS",
        ]:
            if field in values and values[field] == "none":
                values[field] = None

        return values


class GPS(Component):
    """The GPS Component"""

    min_voltage: Optional[float] = Field(
        ..., description="Minimum Voltage", alias="MIN_VOLTAGE"
    )

    output_rate: float = Field(..., description="Output Rate", alias="OUTPUT_RATE")

    max_voltage: Optional[float] = Field(
        ..., description="Maximum Voltage", alias="MAX_VOLTAGE"
    )

    power_consumption: float = Field(
        ..., description="Power Consumption", alias="POWER_CONSUMPTION"
    )

    max_current_range: Optional[float] = Field(
        ..., description="Max Current Range", alias="MAX_CURRENT_RANGE"
    )

    cost: float = Field(..., description="COST", alias="Cost")

    gps_loc: str = Field(..., description="GPS_Location", alias="GPS_Location")

    weight: float = Field(..., description="Weight of the GPS", alias="WEIGHT")

    number_of_gnss: float = Field(
        ..., description="NUMBER_of_GNSS", alias="Number_of_GNSS"
    )

    gps_accuracy: float = Field(..., description="GPS_ACCURACY", alias="GPS_ACCURACY")

    diameter: float = Field(..., description="Diameter", alias="DIAMETER")

    height: float = Field(..., description="Height", alias="HEIGHT")

    @property
    def prt_file(self):
        return "para_gps.prt"

    @root_validator(pre=True)
    def validate_gps_fields(cls, values):
        return inject_none_for_missing_fields_and_nans(cls, values)


class Servo(Component):
    travel: float = Field(..., description="Travel", alias="Travel")

    LENF: float = Field(..., description="LenF", alias="LENF")

    min_stall_torque: float = Field(
        ..., description="Min_Stall_Torque", alias="Min_Stall_Torque"
    )

    output_shaft_spline: str = Field(
        ..., description="Output_Shaft_Spline", alias="Output_Shaft_Spline"
    )

    wire_gauge: float = Field(..., description="Wire_Gauge", alias="Wire_Gauge")

    current_no_load: float = Field(
        ..., description="Current at no load", alias="Current_No_Load"
    )

    deadband_width: float = Field(
        ..., description="Dead Band Width", alias="Deadband_Width"
    )

    weight: float = Field(..., description="WEIGHT", alias="WEIGHT")

    lend: float = Field(..., description="Lend", alias="LEND")

    min_no_load_speed: float = Field(
        ..., description="No load speed minimum", alias="Min_No_Load_Speed"
    )

    idle_current: float = Field(..., description="Current_Idle", alias="Current_Idle")

    max_voltage: float = Field(..., description="Max_Voltage", alias="Max_Voltage")

    len_e: float = Field(..., description="Lene", alias="LENE")

    max_stall_torque: float = Field(
        ..., description="Max stall torque", alias="Max_Stall_Torque"
    )

    max_rotation: float = Field(..., description="Max Rotation", alias="Max_Rotation")

    len_a: float = Field(..., description="Len A", alias="LENA")

    min_voltage: float = Field(..., description="Minimum Voltage", alias="Min_Voltage")

    len_c: float = Field(..., description="Len C", alias="LENC")

    max_no_load_speed: float = Field(
        ..., description="Max_No_Load_Speed", alias="Max_No_Load_Speed"
    )

    max_pwm_range: str = Field(..., description="Max PWM range", alias="Max_PWM_Range")

    len_b: float = Field(..., description="Len B", alias="LENB")

    stall_current: float = Field(
        ..., description="Stall Current", alias="Stall_Current"
    )

    servo_class: str = Field(..., description="Servo Class", alias="Servo_Class")

    @property
    def prt_file(self):
        return "para_servo.prt"


class Receiver(Component):
    max_voltage: float = Field(..., description="Maximum Voltage", alias="MAX_VOLTAGE")

    width: float = Field(..., description="Width", alias="WIDTH")

    height: float = Field(..., description="Height", alias="HEIGHT")

    weight: float = Field(..., description="Weight", alias="WEIGHT")

    min_voltage: float = Field(..., description="Minimum Voltage", alias="MIN_VOLTAGE")

    power_consumption: float = Field(
        ..., description="POWER_CONSUMPTION", alias="POWER_CONSUMPTION"
    )

    length: float = Field(..., description="Length", alias="LENGTH")

    cost: float = Field(..., description="Cost", alias="Cost ($)")

    max_no_channels: float = Field(
        ..., description="Maximum Number of Channels", alias="Max_Number_of_Channels"
    )

    @property
    def prt_file(self):
        return "para_receiver.prt"


class Sensor(Component):
    max_voltage: Optional[float] = Field(
        ..., description="Max Voltage", alias="MAX_VOLTAGE"
    )

    weight: float = Field(..., description="Weight", alias="WEIGHT")

    cost: float = Field(..., description="COST", alias="Cost")

    length: float = Field(..., description="LENGTH", alias="LENGTH")

    power_consumption: float = Field(
        ..., description="POWER_CONSUMPTION", alias="POWER_CONSUMPTION"
    )

    height: float = Field(..., description="Height", alias="HEIGHT")

    min_voltage: Optional[float] = Field(
        ..., description="MIN_VOLTAGE", alias="MIN_VOLTAGE"
    )

    voltage_precision: Optional[float] = Field(
        ..., description="VOLTAGE_PRECISION", alias="VOLTAGE_PRECISION"
    )

    width: float = Field(..., description="WIDTH", alias="WIDTH")

    max_altitude: Optional[float] = Field(
        ..., description="Max altitude", alias="MAX_ALTITUDE"
    )

    min_altitude: Optional[float] = Field(
        ..., description="Min altitude", alias="MIN_ALTITUDE"
    )

    altitude_precision: Optional[float] = Field(
        ..., description="Altitude Precision", alias="ALTITUDE_PRECISION"
    )

    max_rpm: Optional[float] = Field(..., description="Max rpm", alias="MAX_RPM")

    min_rpm: Optional[float] = Field(..., description="Min rpm", alias="MIN_RPM")

    max_temp: Optional[float] = Field(
        ..., description="Max Temperature", alias="MAX_TEMP"
    )

    min_temp: Optional[float] = Field(
        ..., description="Min Temperature", alias="MIN_TEMP"
    )

    @property
    def prt_file(self):
        return "para_sensor.prt"

    @root_validator(pre=True)
    def validate_fields(cls, values):
        return inject_none_for_missing_fields_and_nans(cls, values)


class Autopilot(Component):
    max_servo_rail_voltage: float = Field(
        ..., description="Max servo rail voltage", alias="MAX_SERVO_RAIL_VOLTAGE"
    )

    can: float = Field(..., description="can", alias="CAN")

    acc_gyro_1: str = Field(..., description="ACCGyro_1", alias="AccGyro_1")

    i2c: float = Field(..., description="I2C", alias="I2C")

    no_of_telem_inputs: float = Field(
        ..., description="No. of telem inputs", alias="Number_of_Telem_Inputs"
    )

    uart: Optional[float] = Field(..., description="UART", alias="UART")

    fmu_cached_memory: float = Field(
        ..., description="FMU_CACHED_MEMORY", alias="FMU_CACHED_MEMORY"
    )

    width: float = Field(..., description="WIDTH", alias="WIDTH")

    magnetometer: str = Field(..., description="Magnetometer", alias="Magnetometer")

    acc_gyro_3: Optional[str] = Field(..., description="AccGyro_3", alias="AccGyro_3")

    cost: float = Field(..., description="Cost", alias="COST")

    height: float = Field(..., description="height", alias="HEIGHT")

    main_fmu_processor: str = Field(
        ..., description="MAIN_FMU_PROCESSOR", alias="Main_FMU_Processor"
    )

    no_of_input_batteries: str = Field(
        ..., description="No. of input batteries", alias="Number_of_Input_Batteries"
    )

    weight: float = Field(..., description="Weight", alias="WEIGHT")

    fmu_bits: float = Field(..., description="FMU_Bits", alias="FMU_Bits")

    input_voltage: Optional[Union[float, Tuple[float, float]]] = Field(
        ..., description="INPUT_VOLTAGE", alias="INPUT_VOLTAGE"
    )

    barometer_1: str = Field(..., description="Barometer_1", alias="Barometer_1")

    spi: float = Field(..., description="SPI", alias="SPI")

    fmu_speed: float = Field(..., description="FMU_SPEED", alias="FMU_SPEED")

    acc_gyro_2: str = Field(..., description="ACC_GYRO2", alias="AccGyro_2")

    pwm_outputs: float = Field(..., description="PWM_Outputs", alias="PWM_Outputs")

    pwm_inputs: Optional[float] = Field(
        ..., description="PWM_Inputs", alias="PWM_Inputs"
    )

    barometer_2: Optional[str] = Field(
        ..., description="Second barometer", alias="Barometer_2"
    )

    fmu_ram: float = Field(..., description="FMU_RAM", alias="FMU_RAM")

    adc: float = Field(..., description="ADC", alias="ADC")

    length: float = Field(..., description="LENGTH", alias="LENGTH")

    io_bits: Optional[float] = Field(..., description="IO_Bits", alias="IO_Bits")

    io_processor: Optional[str] = Field(
        ..., description="IO_Processor", alias="IO_Processor"
    )

    io_ram: Optional[float] = Field(..., description="IO_RAM", alias="IO_RAM")

    io_speed: Optional[float] = Field(..., description="IO_SPEED", alias="IO_SPEED")

    @property
    def prt_file(self):
        return None  # ToDo: is the the same as FlightController

    @validator("input_voltage", pre=True, always=True)
    def validate_input_voltage(cls, value):
        if isinstance(value, str) and "," in value:
            value = tuple(float(v) for v in value.split(","))
        return value

    @root_validator(pre=True)
    def validate_fields(cls, values):
        if "Number_of_Tele_ Inputs" in values:
            values["Number_of_Telem_Inputs"] = values.pop("Number_of_Tele_ Inputs")
        return inject_none_for_missing_fields_and_nans(cls, values)


class Flange(Component):
    od: float = Field(..., description="Outer Diameter", alias="OD")

    box: float = Field(..., description="Box", alias="BOX")

    clock_angle: Optional[float] = Field(
        None, description="The Clock Angle", alias="CLOCK_ANGLE"
    )

    sidemount_offset: Optional[float] = Field(
        None, description="The Side Mount Offset", alias="SIDEMOUNT_OFFSET"
    )

    offset: Optional[float] = Field(None, description="Offset", alias="OFFSET")

    num_horizontal_conn: Optional[int] = Field(
        None, description="The number of horizontal connections", alias="NUMHORZCONN"
    )

    angle_horizontal_connection: Optional[float] = Field(
        None, description="The angle of horizontal connections", alias="ANGHORZCONN"
    )


class Tube(Component):
    length: float = Field(..., description="Length of the tube", alias="Length")

    od: float = Field(..., description="The outer diameter", alias="OD")

    id: float = Field(..., description="The inner diameter", alias="ID")

    rot_2: Optional[float] = Field(
        default=None, description="The ROT2 parameter", alias="ROT2"
    )


class Hub(Component):
    num_of_horizontal_connections: int = Field(
        ..., description="The number of horizontal connections", alias="NUMHORZCONN"
    )

    angle_of_horizontal_connections: float = Field(
        ..., description="The angle of horizontal connection", alias="ANGHORZCONN:"
    )


class Orient(Component):
    z_angle: float = Field(..., description="The Z-Angle", alias="Z_ANGLE")


class CarbonFiberPlate(Component):
    width: float = Field(..., description="The width of the CFP", alias="WIDTH")

    thickness: float = Field(
        ..., description="The Thickness of the plate", alias="THICKNESS"
    )

    density: float = Field(..., description="The density of the plate", alias="DENSITY")

    length: float = Field(..., description="The Length of the plate", alias="LENGTH")

    x8_offset: float = Field(..., description="X8_OFFSET", alias="X8_OFFSET")

    z6_offset: float = Field(..., description="Z6_OFFSET", alias="Z6_OFFSET")

    z8_offset: float = Field(..., description="Z8_OFFSET", alias="Z8_OFFSET")

    x6_offset: float = Field(..., description="X6_OFFSET", alias="X6_OFFSET")

    z7_offset: float = Field(..., description="The Z7_OFFSET", alias="Z7_OFFSET")

    z3_offset: float = Field(..., description="The Z3_OFFSET", alias="Z3_OFFSET")

    x5_offset: float = Field(..., description="X5_OFFSET", alias="X5_OFFSET")

    x2_offset: float = Field(..., description="X2_OFFSET", alias="X2_OFFSET")

    x4_offset: float = Field(..., description="X4_OFFSET", alias="X4_OFFSET")

    z1_offset: float = Field(..., description="Z1_OFFSET", alias="Z1_OFFSET")

    x1_offset: float = Field(..., description="X1_OFFSET", alias="X1_OFFSET")

    x3_offset: float = Field(..., description="X3_OFFSET", alias="X3_OFFSET")

    z4_offset: float = Field(..., description="Z4_OFFSET", alias="Z4_OFFSET")

    x7_offset: float = Field(..., description="X7_OFFSET", alias="X7_OFFSET")

    z2_offset: float = Field(..., description="Z2_OFFSET", alias="Z2_OFFSET")

    z5_offset: float = Field(..., description="Z5_OFFSET", alias="Z5_OFFSET")


class Beam_Cap(Component):
    thickness: float = Field(..., description="Thickness", alias="THICKNESS")

    chord: float = Field(..., alias="CHORD")


class NACA_Port_Connector(Component):
    bottom_connection_disp: float = Field(
        default=0, description="BOTTOM_CONNECTION_DISP", alias="BOTTOM_CONNECTION_DISP"
    )

    port_thickness: float = Field(
        default=100, description="CHORD", alias="PORT_THICKNESS"
    )

    chord: float = Field(default=500, description="CHORD", alias="CHORD")

    thickness: float = Field(default=12, description="THICKNESS", alias="THICKNESS")


class ComponentsRepository:
    """The components repository builder class"""

    def __init__(self, creator, components, corpus):
        self.creator = creator
        self.corpus = corpus
        self.components = self._initialize_components(components)

    @property
    def all(self):
        return list(self.components.keys())

    def __getattr__(self, item):
        if item in self.components:
            return self.components[item]
        else:
            raise AttributeError(
                f"{self.creator.__name__} {item} is missing from the repository"
            )

    def __getitem__(self, item):
        if isinstance(item, int):
            components = list(self.components.values())
            return components[item]
        else:
            component_names = {
                component.name: component for component in self.components.values()
            }

            if item in component_names:
                return component_names[item]
            else:
                raise KeyError(
                    f"{self.creator.__name__} {item} is missing from the repository"
                )

    def __iter__(self):
        for component in self.components.values():
            yield component

    def __len__(self):
        return len(self.components)

    def to_csv(self, filename):
        """Write these components to a csv_file"""
        keys = [field.alias for _, field in self.creator.__fields__.items()]
        with open(filename, "w", newline="") as op_csv:
            dict_writer = csv.DictWriter(op_csv, keys)
            dict_writer.writeheader()
            for component in self.components.values():
                dict_writer.writerow(component.dict(by_alias=True))

    def _initialize_components(self, components):
        component_instances = {}

        for component_dict in components:
            object_dict = self._fix_parametric_properties(component_dict)
            object_dict["corpus"] = self.corpus
            component_instance = self.creator.parse_obj(object_dict)
            component_instances[component_instance.name] = component_instance

        return component_instances

    def _fix_parametric_properties(self, component_dict):
        parametric_properties = {}
        all_properties = {}
        for key, value in component_dict.items():
            if key.startswith("para"):
                splitted = key.split("_")
                parameter_name = "_".join(splitted[1:-1])
                if parameter_name not in parametric_properties:
                    parametric_properties[parameter_name] = {}
                if splitted[-1] == "[]AssignedValue":
                    parametric_properties[parameter_name]["value"] = value
                if splitted[-1] == "[]Minimum":
                    parametric_properties[parameter_name]["min"] = value
                if splitted[-1] == "[]Maximum":
                    parametric_properties[parameter_name]["max"] = value
            else:
                all_properties[key] = value

        assigned_values = dict(
            map(lambda v: (v[0], v[1]["value"]), parametric_properties.items())
        )

        all_properties.update(assigned_values)

        return all_properties

    def __repr__(self):
        return f"<{self.creator.__name__} Library, Count: {self.__len__()}, Corpus: {self.corpus}>"


class Cylinder(Component):
    wall_thickness: float = Field(default=3.0, alias="WALL_THICKNESS")

    left_conn_display: float = Field(default=0.0, alias="LEFT_CONN_DISP")

    top_conn_display: float = Field(default=0.0, alias="TOP_CONN_DISP")

    right_conn_display: float = Field(default=0.0, alias="RIGHT_CONN_DISP")

    bottom_conn_display: float = Field(default=0.0, alias="BOTTOM_CONN_DISP")

    diameter: float = Field(default=0.0, alias="DIAMETER")

    port_thickness: float = Field(default=100.0, alias="PORT_THICKNESS")

    length: float = Field(default=100.0, alias="LENGTH")

    front_angle: float = Field(default=1000.0, alias="FRONT_ANGLE")


class Fuselage(Component):
    wall_thickness: float = Field(
        ..., description="WALL THICKNESS", alias="WALL_THICKNESS"
    )

    seat_1_lr: float = Field(default=100, description="SEAT 1 LR", alias="SEAT_1_LR")

    floor_height: float = Field(
        default=100, description="FLOOR HEIGHT", alias="FLOOR_HEIGHT"
    )

    port_thickness: float = Field(
        default=100, description="PORT THICKNESS", alias="PORT_THICKNESS"
    )

    middle_length: float = Field(
        default=100, description="MIDDLE LENGTH", alias="MIDDLE_LENGTH"
    )

    bottom_port_disp: float = Field(
        default=100, description="BOTTOM PORT DISP", alias="BOTTOM_PORT_DISP"
    )

    length: float = Field(default=100, description="LENGTH", alias="LENGTH")

    seat_2_fb: float = Field(default=100, description="SEAT 2 FB", alias="SEAT_2_FB")

    seat_1_fb: float = Field(default=100, description="SEAT 1 FB", alias="SEAT_1_FB")

    seat_2_lr: float = Field(default=100, description="SEAT 2 LR", alias="SEAT_2_LR")

    tail_diameter: float = Field(
        default=100, description="TAIL DIAMETER", alias="TAIL_DIAMETER"
    )

    sphere_diameter: float = Field(
        default=100, description="SPHERE DIAMETER", alias="SPHERE_DIAMETER"
    )

    right_port_disp: float = Field(
        default=100, description="RIGHT PORT DISP", alias="RIGHT_PORT_DISP"
    )

    top_port_disp: float = Field(
        default=100, description="TOP PORT DISP", alias="TOP_PORT_DISP"
    )

    left_port_disp: float = Field(
        default=100, description="LEFT PORT DISP", alias="LEFT_PORT_DISP"
    )


class Passenger(Component):

    weight: float = Field(..., description="WEIGHT", alias="WEIGHT")


class Beam(Component):
    top_conn_disp: float = Field(
        default=0.0, description="TOP CONN DISP", alias="TOP_CONN_DISP"
    )

    chord: float = Field(default=500.0, description="CHORD", alias="CHORD")

    thickness: float = Field(default=40.0, description="THICKNESS", alias="THICKNESS")

    span: float = Field(default=1000.0, description="SPAN", alias="SPAN")

    bottom_conn_disp: float = Field(
        default=0.0, description="BOTTOM CONN DISP", alias="BOTTOM_CONN_DISP"
    )


class Cylinder_Flip(Component):
    wall_thickness: float = Field(
        ..., description="WALL THICKNESS", alias="WALL_THICKNESS"
    )

    length: float = Field(..., description="LENGTH", alias="LENGTH")

    diameter: float = Field(default=0, description="DIAMETER", alias="DIAMETER")


all_uav_components = get_data_file_path("all_uav_components.json")
with open(all_uav_components) as json_file:
    all_uav_components = json.load(json_file)

all_uam_components = get_data_file_path("all_uam_components.json")
with open(all_uam_components) as json_file:
    all_uam_components = json.load(json_file)


def get_corpus_components(corpus):
    if corpus == "uav":
        all_components = all_uav_components
    elif corpus == "uam":
        all_components = all_uam_components
    else:
        raise ValueError("corpus can only be either `uav` or `uam`")
    return all_components


def get_all_components_of_class(cls, corpus):
    all_components = get_corpus_components(corpus)
    for key, value in all_components.items():
        if value["Classification"] == cls.__name__:
            value["Name"] = key
            yield value


def build_components(cls, corpus):
    return ComponentsRepository(
        creator=cls, components=get_all_components_of_class(cls, corpus), corpus=corpus
    )


def build_components_of_class(cls, names, corpus):
    return ComponentsRepository(
        creator=cls,
        components=(
            {
                "Name": comp_name,
                **get_corpus_components(corpus)[comp_name],
                "Classification": cls.__name__,
            }
            for comp_name in names
        ),
        corpus=corpus,
    )


def build_tubes(names, corpus):
    for tube_name in names:
        corpus_components = get_corpus_components(corpus)
        if "para_Length_[]AssignedValue" not in corpus_components[tube_name]:
            corpus_components[tube_name][
                "para_Length_[]AssignedValue"
            ] = corpus_components[tube_name].pop("LENGTH", 200.0)

    return build_components_of_class(Tube, names, corpus=corpus)
