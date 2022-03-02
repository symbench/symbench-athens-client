from typing import Tuple, Union

from pydantic import Field

from symbench_athens_client.models.base_design import SeedDesign


class UAMSeedDesign(SeedDesign):
    pass


class Rake(UAMSeedDesign):
    __design_vars__ = {
        "naca",
        "param_0",
        "param_1",
        "param_2" "param_3" "param_4" "param_5",
        "param_6",
        "param_7",
        "param_8",
        "param_9",
        "param_10",
        "param_11",
        "param_12",
        "param_13",
        "param_14",
        "param_15",
        "param_16",
        "param_17",
        "param_18",
        "param_19",
        "param_20",
        "param_21",
        "param_22",
        "param_23",
        "param_24",
        "param_25",
        "param_26",
        "rear_battery_percent",
        "front_battery_percent",
        "voltage_1",
        "voltage_2",
        "q_position",
        "q_velocity",
        "q_angular_velocity",
        "q_angles",
        "r",
    }

    naca: int = Field(default=4512, alias="NACA")

    param_0: Union[float, Tuple[float, float]] = Field(default=3000.0, alias="Param_0")

    param_1: Union[float, Tuple[float, float]] = Field(default=1000.0, alias="Param_1")

    param_2: Union[float, Tuple[float, float]] = Field(default=12.0, alias="Param_2")

    param_3: Union[float, Tuple[float, float]] = Field(default=1000.0, alias="Param_3")

    param_4: Union[float, Tuple[float, float]] = Field(default=100.0, alias="Param_4")

    param_5: Union[float, Tuple[float, float]] = Field(default=2000.0, alias="Param_5")

    param_6: Union[float, Tuple[float, float]] = Field(default=1520.0, alias="Param_6")

    param_7: Union[float, Tuple[float, float]] = Field(default=200.0, alias="Param_7")

    param_8: Union[float, Tuple[float, float]] = Field(default=275.0, alias="Param_8")

    param_9: Union[float, Tuple[float, float]] = Field(default=150.0, alias="Param_9")

    param_10: Union[float, Tuple[float, float]] = Field(
        default=2500.0, alias="Param_10"
    )

    param_11: Union[float, Tuple[float, float]] = Field(
        default=3000.0, alias="Param_11"
    )

    param_12: Union[float, Tuple[float, float]] = Field(default=12.0, alias="Param_12")

    param_13: Union[float, Tuple[float, float]] = Field(
        default=7000.0, alias="Param_13"
    )

    param_14: Union[float, Tuple[float, float]] = Field(
        default=8500.0, alias="Param_14"
    )

    param_15: Union[float, Tuple[float, float]] = Field(default=801.0, alias="Param_15")

    param_16: Union[float, Tuple[float, float]] = Field(default=150.0, alias="Param_16")

    param_17: Union[float, Tuple[float, float]] = Field(
        default=2200.0, alias="Param_17"
    )

    param_18: Union[float, Tuple[float, float]] = Field(default=2.0, alias="Param_18")

    param_19: Union[float, Tuple[float, float]] = Field(
        default=-350.0, alias="Param_19"
    )

    param_20: Union[float, Tuple[float, float]] = Field(default=210.0, alias="Param_20")

    param_21: Union[float, Tuple[float, float]] = Field(
        default=-210.0, alias="Param_21"
    )

    param_22: Union[float, Tuple[float, float]] = Field(
        default=1000.0, alias="Param_22"
    )

    param_23: Union[float, Tuple[float, float]] = Field(default=250.0, alias="Param_23")

    param_24: Union[float, Tuple[float, float]] = Field(
        default=-220.0, alias="Param_24"
    )

    param_25: Union[float, Tuple[float, float]] = Field(default=500.0, alias="Param_25")

    param_26: Union[float, Tuple[float, float]] = Field(default=790.0, alias="Param_26")

    rear_battery_percent: Union[float, Tuple[float, float]] = Field(
        default=12.0, alias="rear_battery_percent"
    )

    front_battery_percent: Union[float, Tuple[float, float]] = Field(
        default=10.0, alias="front_battery_percent"
    )

    voltage_1: Union[float, Tuple[float, float]] = Field(
        default=724.0, alias="Voltage1"
    )

    voltage_2: Union[float, Tuple[float, float]] = Field(default=51.8, alias="Voltage2")
