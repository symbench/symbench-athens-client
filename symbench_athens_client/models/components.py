import pandas as pd
from pydantic import BaseModel, Field, root_validator

from symbench_athens_client.utils import get_data_file_path, to_camel_case


class Component(BaseModel):
    """The Base Component Class"""

    category: str = Field(..., description="Category", alias="Category")

    style: str = Field(..., description="Style", alias="Style")

    name: str = Field(..., description="Name of the battery", alias="Name")

    manufacturer: str = Field(..., description="Manufacturer", alias="Manufacturer")

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}, Category: {self.category}, Name: {self.name}>"
        )

    def __str__(self):
        return repr(self)

    @root_validator(pre=True)
    def validate(cls, values):
        defaults = {float: 0.0, str: ""}
        field_annos = {}
        for field, field_info in cls.__fields__.items():
            field_annos[field_info.alias] = field_info.type_
        for field in values:
            if pd.isna(values[field]):
                values[field] = defaults[field_annos[field]]
        return values

    class Config:
        allow_mutation = False
        allow_population_by_field_name = True


class Battery(Component):
    """The Battery Component"""

    cost: float = Field(..., description="Cost in dollars", alias="Cost [$]")

    length: float = Field(..., description="Length in MM", alias="Length [mm]")

    width: float = Field(..., description="Width in MM", alias="Width [mm]")

    thickness: float = Field(..., description="Thickness in MM", alias="Thickness [mm]")

    weight: float = Field(..., description="Weight in grams", alias="Weight [g]")

    voltage: float = Field(..., description="Voltage in Volts", alias="Voltage [V]")

    num_cells: str = Field(..., description="Number of cells", alias="Number of Cells")

    chemistry_type: str = Field(
        ..., description="Chemistry Type", alias="Chemistry Type"
    )

    capacity: float = Field(..., description="Capacity in Mah", alias="Capacity [mAh]")

    peak_discharge_rate: float = Field(
        ..., description="Peak Discharge Rate [C]", alias="Peak Discharge Rate [C]"
    )

    cont_discharge_rate: float = Field(
        ..., description="Cont. Discharge Rate [C]", alias="Cont. Discharge Rate [C]"
    )

    pack_resistance: float = Field(
        ..., description="Pack Resistance [mΩ]", alias="Pack Resistance [mΩ]"
    )

    discharge_cable_size_awg: float = Field(
        0.0,
        description="Discharge Cable Size [AWG]",
        alias="Discharge Cable Size [AWG]",
    )

    discharge_plug: str = Field(
        ..., description="Discharge Plug", alias="Discharge Plug"
    )

    performance_file: str = Field(
        "", description="Performance File", alias="Performance File"
    )

    buy_link: str = Field(..., description="Buy Link", alias="Buy Link")

    cad_file: str = Field(..., description="CAD File", alias="CAD File")

    manf_cad: str = Field(..., description="Manufacturer CAD File", alias="Manf CAD")

    image_file: str = Field(..., description="Image File", alias="Image File")

    product_description: str = Field(
        ..., description="Product Description", alias="Product Description"
    )


class Propeller(Component):
    """The propeller component"""

    cost: float = Field(
        ...,
    )


class ComponentBuilder:
    """The components repository builder class"""

    def __init__(self, creator, spreadsheet):
        self.creator = creator
        self.components = self._initialize_components(creator, spreadsheet)

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
    def _initialize_components(creator, spreadsheet):
        batteries_excel_sheet = get_data_file_path(spreadsheet)
        df = pd.read_excel(batteries_excel_sheet)
        dicts = df.to_dict(orient="records")
        components = {}
        for battery_dict in dicts:
            comp = creator.parse_obj(battery_dict)
            components[to_camel_case(comp.name)] = comp
        return components


Batteries = ComponentBuilder(Battery, "Battery_Corpus.xlsx")
