import json
from typing import Any, Dict, Optional, Tuple, Union

from pydantic import BaseModel, Field, root_validator, validator

from symbench_athens_client.utils import (
    get_data_file_path,
    inject_none_for_missing_fields,
)


class Component(BaseModel):
    """The Base Component Class"""

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

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}, Category: {self.category}, Name: {self.name}>"
        )

    def __str__(self):
        return repr(self)

    @root_validator(pre=True)
    def inject_model(cls, values):
        if "Model" in values:
            values["MODEL"] = values.pop("Model")

        if not values.get("model", values.get("MODEL", values.get("Model"))):
            values["model"] = values.get("name", values.get("Name"))
        return values

    class Config:
        allow_mutation = False
        allow_population_by_field_name = True
        extra = "forbid"


class Battery(Component):
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

    peak_discharge_rate: float = Field(
        ...,
        description="Peak Discharge rate of the Battery",
        alias="PEAK_DISCHARGE_RATE",
    )

    number_of_cells: str = Field(
        ..., description="Number of cells", alias="NUMBER_OF_CELLS"
    )

    thickness: str = Field(..., description="Thickness", alias="THICKNESS")

    cont_discharge_rate: float = Field(
        ..., description="Continuous Discharge Rate", alias="CONT_DISCHARGE_RATE"
    )

    voltage: float = Field(..., description="Voltage", alias="VOLTAGE")

    capacity: float = Field(
        ..., description="Capacity of the Battery", alias="CAPACITY"
    )

    discharge_plug: str = Field(
        ..., description="Discharge Plug Details", alias="DISCHARGE_PLUG"
    )

    width: float = Field(..., description="Width of the Battery", alias="WIDTH")

    chemistry_type: str = Field(
        ..., description="Chemistry Type of the Battery", alias="CHEMISTRY_TYPE"
    )

    cost: float = Field(..., description="Cost of the Battery", alias="COST")

    pack_resistance: float = Field(
        0.0, description="Pack Resistance of the Battery", alias="PACK_RESISTANCE"
    )

    weight: float = Field(
        ...,
        description="Weight of the Battery",
        alias="WEIGHT",
    )

    length: float = Field(..., description="Length of the Battery", alias="LENGTH")

    @root_validator(pre=True)
    def validate_fields(cls, values):
        if "Chemistry Type" in values:
            values["CHEMISTRY_TYPE"] = values.pop("Chemistry Type")
        if "Discharge Plug" in values:
            values["DISCHARGE_PLUG"] = values.pop("Discharge Plug")
        if "Number of Cells" in values:
            values["NUMBER_OF_CELLS"] = values.pop("Number of Cells")
        return values


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

    direction: float = Field(..., description="Direction", alias="Direction")

    performance_file: str = Field(
        ..., description="Performance file location/name", alias="Performance_File"
    )

    shaft_diameter: float = Field(
        ..., description="The shaft diameter of the propeller", alias="SHAFT_DIAMETER"
    )

    pitch: float = Field(..., description="The pitch of the propeller", alias="PITCH")

    weight: float = Field(..., description="Weight of the propeller", alias="WEIGHT")

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

    max_power: float = Field(
        ..., description="Max power of the motor", alias="MAX_POWER"
    )

    io_idle_current_at_10V: float = Field(
        ..., description="Maximum idle current at 10V", alias="IO_IDLE_CURRENT@10V"
    )

    length: float = Field(..., description="Length of the Motor", alias="LENGTH")

    kt: float = Field(..., description="The KT rating of the Motor", alias="KT")

    esc_bec_class: float = Field(
        ..., description="The ESC/BEC Class", alias="ESC/BEC Class"
    )

    can_length: float = Field(..., description="The can length", alias="CAN_LENGTH")

    total_length: float = Field(..., description="Total length", alias="TOTAL_LENGTH")

    km: float = Field(..., description="KM rating of the motor", alias="KM")

    shaft_diameter: float = Field(
        ..., description="The shaft diameter of the motor", alias="SHAFT_DIAMETER"
    )

    weight: float = Field(..., description="Weight of the motor", alias="WEIGHT")

    poles: str = Field(..., description="The poles of the motor", alias="Poles")

    internal_resistance: float = Field(
        ..., description="Internal Resistance of the motor", alias="INTERNAL_RESISTANCE"
    )

    control_channel: Optional[str] = Field(
        ..., description="The control channel", alias="CONTROL_CHANNEL"
    )

    adapter_length: Optional[Union[float, Tuple[float, float]]] = Field(
        ..., description="The adapter length", alias="ADAPTER_LENGTH"
    )

    max_current: float = Field(
        ..., description="Max current rating of the motor", alias="MAX_CURRENT"
    )

    max_no_cells: float = Field(
        ..., description="Max number of cells in the motor", alias="Max # of Cells"
    )

    kv: float = Field(..., description="The KV rating of the motor", alias="KV")

    cost: float = Field(..., description="Cost of the motor", alias="COST")

    can_diameter: float = Field(
        ..., description="The can diameter of the motor", alias="CAN_DIAMETER"
    )

    min_no_cells: float = Field(
        ...,
        description="The minimum number of cells of the motor",
        alias="Min # of Cells",
    )

    prop_size_rec: Union[float, Tuple[float, float]] = Field(
        ...,
        description="The propsize rec",
        alias="PROP_SIZE_REC.",
    )

    prop_pitch_rec: Union[float, Tuple[float, float]] = Field(
        ..., description="The prop pitch rec", alias="PROP_PITCH_REC."
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

    @root_validator(pre=True)
    def validate_fields(cls, values):
        if "CONTROL_CHANNEL" in values and values["CONTROL_CHANNEL"] == "none":
            values["CONTROL_CHANNEL"] = None
        return inject_none_for_missing_fields(cls, values)


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

    control_channel: Optional[str] = Field(
        ..., description="Control Channel", alias="CONTROL_CHANNEL"
    )

    esc_bec_class: Optional[float] = Field(
        ..., description="The ESC/BEC Class", alias="ESC/BEC Class"
    )

    thickness: float = Field(..., description="THICKNESS", alias="THICKNESS")

    offset: Optional[float] = Field(..., description="Offset", alias="Offset")

    mount_angle: Optional[float] = Field(
        ..., description="The mount angle", alias="Mount_Angle"
    )

    tube_od: Optional[float] = Field(..., description="The tube OD", alias="TUBE_OD")

    width: float = Field(..., description="The width of ESC", alias="WIDTH")

    weight: float = Field(..., description="The weight of ESC", alias="WEIGHT")

    peak_amps: Optional[float] = Field(
        ...,
        description="The Peak ampere ratings for the ESC controller",
        alias="PEAK_AMPS",
    )

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
        return inject_none_for_missing_fields(cls, values)


class Instrument_Battery(Battery):
    """The Instrument Battery Component"""


class Wing(Component):
    """The Wing Component"""

    span: Optional[float] = Field(..., description="SPAN property", alias="SPAN")

    aileron_bias: Optional[float] = Field(..., description="BIAS", alias="AILERON_BIAS")

    aoa_cl_max: float = Field(..., description="AoA_CL_Max", alias="AoA_CL_Max")

    offset: Optional[float] = Field(..., description="OFFSET", alias="OFFSET")

    control_channel_flaps: Optional[float] = Field(
        ..., description="CONTROL_CHANNEL_FLAPS", alias="CONTROL_CHANNEL_FLAPS"
    )

    cl_max: float = Field(..., description="CL_Max", alias="CL_Max")

    cl_max_cd0_min: float = Field(
        ..., description="CL_Max_CD0_Min", alias="CL_Max_CD0_Min"
    )

    last_two: float = Field(..., description="LAST_TWO", alias="LASTTWO")

    chord: Optional[str] = Field(..., description="CHORD", alias="CHORD")

    tube_offset: Optional[str] = Field(
        ..., description="Tube Offset", alias="TUBE_OFFSET"
    )

    cl_ld_max: float = Field(..., description="CL_LD_Max", alias="CL_LD_Max")

    servo_width: Optional[float] = Field(
        ..., description="Servo Width", alias="SERVO_WIDTH"
    )

    aoa_l0: Optional[float] = Field(..., description="AOA_L0", alias="AoA_L0")

    dcl_daoa_slope: float = Field(
        ..., description="dCl_dAoA_Slope", alias="dCl_dAoA_Slope"
    )

    control_channel_ailerons: Optional[str] = Field(
        ..., description="CONTROL_CHANNEL_AILERONS", alias="CONTROL_CHANNEL_AILERONS"
    )

    diameter: Optional[float] = Field(..., description="DIAMETER", alias="DIAMETER")

    ld_max: float = Field(..., description="LD_Max", alias="LD_Max")

    servo_length: Optional[float] = Field(
        ..., description="SERVO_LENGTH", alias="SERVO_LENGTH"
    )

    cd0_min: float = Field(..., description="CD0_MIn", alias="CD0_Min")

    cd_min: float = Field(..., description="CD_MIN", alias="CD_Min")

    cm0: float = Field(..., description="CM0", alias="CM0")

    flap_bias: Optional[float] = Field(..., description="Flap Bias", alias="FLAP_BIAS")

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

    @root_validator(pre=True)
    def validate_gps_fields(cls, values):
        return inject_none_for_missing_fields(cls, values)


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

    @root_validator(pre=True)
    def validate_fields(cls, values):
        return inject_none_for_missing_fields(cls, values)


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

    @validator("input_voltage", pre=True, always=True)
    def validate_input_voltage(cls, value):
        if isinstance(value, str) and "," in value:
            value = tuple(float(v) for v in value.split(","))
        return value

    @root_validator(pre=True)
    def validate_fields(cls, values):
        if "Number_of_Tele_ Inputs" in values:
            values["Number_of_Telem_Inputs"] = values.pop("Number_of_Tele_ Inputs")
        return inject_none_for_missing_fields(cls, values)


class ParametricComponent(Component):
    """A parametric component from the graph database"""

    parameters: Dict[str, Any] = Field(
        ..., description="The Parameters of these components"
    )


class Flange(ParametricComponent):
    pass


class Tube(ParametricComponent):
    pass


class Hub(ParametricComponent):
    pass


class Orient(ParametricComponent):
    pass


class CarbonFiberPlate(ParametricComponent):
    pass


class ComponentsBuilder:
    """The components repository builder class"""

    def __init__(self, creator, components):
        self.creator = creator
        self.components = self._initialize_components(creator, components)

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

    @staticmethod
    def _initialize_components(creator, components):
        component_instances = {}

        for component_dict in components:
            component_instance = creator.parse_obj(component_dict)
            component_instances[component_instance.name] = component_instance

        return component_instances


all_comps = get_data_file_path("all_components.json")
with open(all_comps) as json_file:
    all_comps = json.load(json_file)


def get_all_components_of_class(cls):
    for key, value in all_comps.items():
        if value["Classification"] == cls.__name__:
            value["Name"] = key
            yield value


def _build_components(cls):
    return ComponentsBuilder(creator=cls, components=get_all_components_of_class(cls))


def _build_parametric_components(cls, names):
    return ComponentsBuilder(
        creator=cls,
        components=(
            {"Name": comp_name, "parameters": all_comps[comp_name]}
            for comp_name in names
        ),
    )


ALL_FLANGES = ["0394_para_flange", "0281_para_flange"]
ALL_TUBES = ["0281OD_para_tube", "0394OD_para_tube"]
ALL_HUBS = [
    "0394od_para_hub_5",
    "0394od_para_hub_6",
    "0394od_para_hub_3",
    "0394od_para_hub_4",
    "0394od_para_hub_2",
]
ALL_ORIENTS = ["Orient"]
ALL_CFPS = ["para_cf_fplate"]

Batteries = _build_components(Battery)
Propellers = _build_components(Propeller)
Motors = _build_components(Motor)
ESCs = _build_components(ESC)
Instrument_Batteries = _build_components(Instrument_Battery)
Wings = _build_components(Wing)
GPSes = _build_components(GPS)
Servos = _build_components(Servo)
Receivers = _build_components(Receiver)
Sensors = _build_components(Sensor)
AutoPilots = _build_components(Autopilot)
# Begin Parametric Components
Orients = _build_parametric_components(Orient, ALL_ORIENTS)
Flanges = _build_parametric_components(Flange, ALL_FLANGES)
Tubes = _build_parametric_components(Tube, ALL_TUBES)
Hubs = _build_parametric_components(Hub, ALL_HUBS)
CFPs = _build_parametric_components(CarbonFiberPlate, ALL_CFPS)
