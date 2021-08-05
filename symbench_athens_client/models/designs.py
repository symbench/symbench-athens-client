from typing import List, Tuple

from pydantic import BaseModel, Field, root_validator, validator


class SeedDesign(BaseModel):
    name: str = Field(
        "", alias="name", description="Name of the seed design in the graph database"
    )

    swap_list: List[Tuple[str, str]] = Field(
        [],
        alias="swapList",
        description="List of components to swap from the base seed design",
    )

    def add_swap_components(self, src, dst):
        self.swap_list.append((src, dst))

    def needs_components_swap(self):
        return len(self.swap_list) > 0

    def to_jenkins_parameters(self):
        design_vars = self.dict(by_alias=True, exclude={"name", "swap_list"})
        return {
            "DesignVars": "".join(
                f"{k}={v},{v} " for k, v in design_vars.items()
            ).rstrip()
        }

    def parameters(self, **kwargs):
        kwargs["exclude"] = {"name", "swap_list"}
        return self.dict(**kwargs)

    @validator("name", pre=True, always=True)
    def validate_name(cls, name):
        if name is None or name == "":
            name = cls.__name__
        return name

    class Config:
        validate_assignment = True


class QuadCopter(SeedDesign):
    """The quadcopter seed design"""

    arm_length: float = Field(
        220.0,
        description="Length of Arm_0, Arm_1, Arm_2, Arm_3 in mm",
        alias="Length_0",
    )

    support_length: float = Field(
        95.0,
        description="Length of support_0, Support_1, Support_2, Support_3 in mm",
        alias="Length_1",
    )

    batt_mount_x_offset: float = Field(
        0.0,
        description="X-Offset of the battery mounting position from center of the plate in mm",
        alias="Length_2",
    )

    batt_mount_z_offset: float = Field(
        0.0,
        description="Z-Offset of the battery mounting position from center of the plate in mm",
        alias="Length_3",
    )


class QuadSpiderCopter(SeedDesign):
    """The QuadSpiderCopter seed design."""

    arm_length: float = Field(
        220.0,
        description="Length of Arm_0, Arm_1, Arm_2, Arm_3 in mm",
        alias="Length_0",
    )

    support_length: float = Field(
        155.0,
        description="Length for Support_0, Support_1, Support_2, Support_3 in mm",
        alias="Length_1",
    )

    arm_a_length: float = Field(
        80.0,
        description="Length for Arm_0a, Arm_1a, Arm_2a, Arm_3a in mm",
        alias="Length_2",
    )

    arm_b_length: float = Field(
        80.0, description="Length of segment Arm_*b in mm", alias="Length_3"
    )

    batt_mount_x_offset: float = Field(
        0.0,
        description="X-Offset of the battery mounting position from center of the plate in mm",
        alias="Length_4",
    )

    batt_mount_z_offset: float = Field(
        0.0,
        description="Z-Offset of the battery mounting position from center of the plate in mm",
        alias="Length_5",
    )

    bend_angle: float = Field(
        120.0,
        description="ANGHORZCONN for Bend_0a, Bend_0b, Bend_1a, Bend_1b, Bend_2a, Bend_2b, Bend_3a, Bend_3b",
        alias="Param_0",
    )


class HCopter(SeedDesign):
    arm_length: float = Field(
        500.0,
        description="Length of Arm_0, Arm_1, Arm_2, Arm_3 in mm (default 500)",
        alias="Length_0",
    )

    support_length: float = Field(
        95.0,
        description="Length of Support_0, Support_1, Support_2, Support_3 in mm (default 95)",
        alias="Length_1",
    )

    batt_mount_x_offset: float = Field(
        0.0,
        description="X Offset of battery mounting position from center of plate in mm (default 0)",
        alias="Length_2",
    )

    batt_mount_z_offset: float = Field(
        0.0,
        description="Z Offset of battery mounting position from center of plate in mm (default 0)",
        alias="Length_3",
    )


class HPlane(SeedDesign):
    tube_length: float = Field(
        320.0,
        description="Length for Body_Tube_Front_L, Body_Tube_Front_R, "
        "Body_Tube_Rear_L, Body_Tube_Rear_R in mm (default 320) "
        "Length in x. Do not put props under wings",
        alias="Length_1",
    )


class HexRing(SeedDesign):
    pass


default_params = {}
default_params["QuadCopter"] = QuadCopter().to_jenkins_parameters()
default_params["QuadSpiderCopter"] = QuadSpiderCopter().to_jenkins_parameters()
default_params["Hplane"] = HPlane().to_jenkins_parameters()
default_params["HCopter"] = HCopter().to_jenkins_parameters()

with open("default_params.json", "w") as json_file:
    import json

    json.dump(default_params, json_file, indent=2)
