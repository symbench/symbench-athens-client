import json
from typing import Tuple, Union

from pydantic import BaseModel, Field, root_validator, validator

from symbench_athens_client.utils import get_data_file_path


class Component(BaseModel):
    """The Base Component Class"""

    name: str = Field(
        ...,
        description="The name of the component as is in the graph database",
        alias="Name",
    )

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

    model: str = Field(..., description="Model name of the Battery", alias="MODEL")

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
    """The propeller component"""

    cost: float = Field(
        ..., description="Cost of the propeller in dollars", alias="Cost ($)"
    )

    hub_diameter_in: float = Field(
        ..., description="Hub diameter in inches", alias="Hub Diameter [in]"
    )

    hub_diameter_mm: float = Field(
        ..., description="Hub Diameter in mm", alias="Hub Diameter [mm]"
    )

    hub_thickness_in: float = Field(
        ..., description="Hub Thickness in inches", alias="Hub Thickness [in]"
    )

    hub_thickness_mm: float = Field(
        ..., description="Hub Thickness in mm", alias="Hub Thickness [mm]"
    )

    shaft_diameter_in: float = Field(
        ..., description="Shaft Diameter in inches", alias="Shaft Diameter [in]"
    )

    shaft_diameter_mm: float = Field(
        ..., description="Shaft Diameter in mm", alias="Shaft Diameter [mm]"
    )

    diameter_in: float = Field(
        ..., description="Diameter in inches", alias="Diameter [in]"
    )

    diameter_mm: float = Field(..., description="Diameter in mm", alias="Diameter [mm]")

    pitch_in: float = Field(..., description="Pitch in in", alias="Pitch [in]")

    pitch_mm: float = Field(..., description="Pitch in mm", alias="Pitch [mm]")

    weight_lbm: float = Field(..., description="Weight in lbm", alias="Weight [lbm]")


class Motor(Component):
    cost_adapter: float = Field(
        ..., description="Adapter Cost", alias="Cost Adapter [$]"
    )

    shaft_diameter_mm: float = Field(
        ..., description="Shaft Diameter in mm", alias="Shaft Diameter [mm]"
    )

    length_mm: float = Field(..., description="Length in mm", alias="Length [mm]")

    can_diameter: float = Field(
        ..., description="Can diameter in mm", alias="Can Diameter [mm]"
    )

    can_length: float = Field(
        ..., description="Can length in mm", alias="Can Length [mm]"
    )

    total_length: float = Field(
        ..., description="Total Length in mm", alias="Total Length [mm]"
    )

    adapter_length: Union[float, Tuple[float, float]] = Field(
        ..., description="Adapter Length in mm", alias="Adapter Length [mm]"
    )

    adapter_diameter: Union[float, Tuple[float, float]] = Field(
        ..., description="Adapter diameter in mm", alias="Adapter Diameter [mm]"
    )

    weight_g: float = Field(..., description="Weight in grams", alias="Weight [g]")

    kv: float = Field(..., description="RPM/V", alias="KV [RPM/V]")

    kt: float = Field(..., description="Nm/A", alias="KT [Nm/A]")

    km: float = Field(..., description="KM [Nm/sqrt(W)]", alias="KM [Nm/sqrt(W)]")

    max_current: float = Field(..., description="Max Current", alias="Max Current [A]")

    max_power: float = Field(..., description="Max Power", alias="Max Power [W]")

    internal_resistance: float = Field(
        ...,
        description="Internal Resistance [mOhm]",
        alias="Internal Resistance [mOhm]",
    )

    io_idle_current: float = Field(
        ..., description="Io Idle Current @10V[A]", alias="Io Idle Current@10V [A]"
    )

    poles: str = Field(..., description="Poles", alias="Poles")

    esc_pwm_rate_min: float = Field(
        ..., description="ESC PWM Rate Min [kHz]", alias="ESC PWM Rate Min [kHz]"
    )

    esc_pwm_rate_max: float = Field(
        ..., description="ESC PWM Rate Max [kHz]", alias="ESC PWM Rate Max [kHz]"
    )

    esc_rate: float = Field(..., description="ESC Rate", alias="ESC Rate [Hz]")

    motor_timing_min: float = Field(
        ..., description="Motor Timing Min [deg.]", alias="Motor Timing Min [deg.]"
    )

    motor_timing_max: float = Field(
        ..., description="Motor Timing Max [deg.]", alias="Motor Timing Max [deg.]"
    )

    min_no_cells: float = Field(
        ..., description="Min # of Cells", alias="Min # of Cells"
    )

    max_no_cells: float = Field(
        ..., description="Max # of Cells", alias="Max # of Cells"
    )

    prop_size_rec: Tuple[float, float] = Field(
        ..., description="Prop Size Rec. [in]", alias="Prop Size Rec. [in]"
    )

    prop_pitch_rec: Tuple[float, float] = Field(
        ..., description="Prop Pitch Rec. [in]", alias="Prop Pitch Rec. [in]"
    )

    esc_bec_class: float = Field(
        ..., description="ESC/BEC Class", alias="ESC/BEC Class"
    )

    manf_cad: str = Field(..., description="Manufacturer CAD File", alias="Manf CAD")

    @validator("prop_pitch_rec", pre=True, always=True)
    def validate_prop_pitch(cls, value):
        if isinstance(value, str):
            value = tuple(float(v) for v in value.split(","))
        return value

    @validator("prop_size_rec", pre=True, always=True)
    def validate_prop_length(cls, value):
        if isinstance(value, str):
            value = tuple(float(v) for v in value.split(","))
        return value

    @validator("adapter_diameter", pre=True, always=True)
    def validate_adapter_diameter(cls, value):
        if isinstance(value, str):
            value = tuple(float(v) for v in value.split(","))
        return value

    @validator("adapter_length", pre=True, always=True)
    def validate_adapter_length(cls, value):
        if isinstance(value, str):
            value = tuple(float(v) for v in value.split(","))
        return value


class ESC(Component):
    pass


class ComponentBuilder:
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


def get_all_components_of_class(cls_):
    for key, value in all_comps.items():
        if value["Classification"] == cls_.__name__:
            value["Name"] = key
            yield value


Batteries = ComponentBuilder(
    creator=Battery, components=get_all_components_of_class(Battery)
)
print(Batteries.__len__())
