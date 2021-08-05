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
        return self.dict(by_alias=True, exclude={"name", "swap_list"})

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
        200.00,
        description="Length of Arm_0, Arm_1, Arm_2, Arm_3 in mm",
        alias="Length_0",
    )

    support_length: float = Field(
        200.00, description="Length of support in mm", alias="Length_1"
    )

    batt_mount_x_offset: float = Field(
        200.00,
        description="X-Offset of the battery mounting position from center of the plate in mm",
        alias="Length_3",
    )

    batt_mount_z_offset: float = Field(
        200.00,
        description="Z-Offset of the battery mounting position from center of the plate in mm",
        alias="Length_4",
    )


class QuadSpiderCopter(SeedDesign):
    """The QuadSpiderCopter seed design."""

    arm_length: float = Field(
        200.00,
        description="Length of Arm_0, Arm_1, Arm_2, Arm_3 in mm",
        alias="Length_0",
    )

    support_length: float = Field(
        200.00, description="Length of support in mm", alias="Length_1"
    )

    arm_a_length: float = Field(
        200.00, description="Length of segment Arm_a in mm", alias="Length_2"
    )

    arm_b_length: float = Field(
        200.00, description="Length of segment Arm_*b in mm", alias="Length_3"
    )

    bend: float = (
        Field(90, description="Bend Angle of Bend_ in degrees", alias="Bend"),
    )

    rot_a: float = Field(90.0, description="Rotational angle of arm", alias="Rot_a")

    rot_b: float = Field(-90.0, description="Rotational angle of arm", alias="Rot_b")

    batt_mount_x_offset: float = Field(
        200.00,
        description="X-Offset of the battery mounting position from center of the plate in mm",
        alias="Length_4",
    )

    batt_mount_z_offset: float = Field(
        200.00,
        description="Z-Offset of the battery mounting position from center of the plate in mm",
        alias="Length_5",
    )

    @root_validator(pre=True)
    def validate_angle_rot_b(cls, values):
        rot_a = values.get("rot_a", 90.00)
        rot_b = values.get("rot_b", -90.00)
        assert rot_a + rot_b == 0.0, "Sum of Rot_a and Rot_b should be zero"
        return values
