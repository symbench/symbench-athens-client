import pandas as pd
import pkg_resources
from pydantic import BaseModel, Field

from symbench_athens_client.utils import to_camel_case


class Component(BaseModel):
    """The Base Component Class"""

    category: str = Field(..., description="Category", alias="Category")

    style: str = Field(..., description="Style", alias="Style")

    name: str = Field(..., description="Name of the battery", alias="Name")

    manufacturer: str = Field(..., description="Manufacturer", alias="Manufacturer")

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

    @staticmethod
    def _initialize_components(creator, spreadsheet):
        from pkg_resources import resource_filename

        batteries_excel_sheet = resource_filename(
            "symbench_athens_client", f"data/{spreadsheet}"
        )
        df = pd.read_excel(batteries_excel_sheet)
        dicts = df.to_dict(orient="records")
        components = {}
        for battery_dict in dicts:
            comp = creator.parse_obj(battery_dict)
            components[to_camel_case(comp.name)] = comp
        return components


Batteries = ComponentBuilder(Battery, "Battery_Corpus.xlsx")
