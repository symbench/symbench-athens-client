import json
from typing import List, Tuple, Union

from pydantic import BaseModel, Field
from scipy.stats.qmc import LatinHypercube, scale


class Parameter(BaseModel):
    pass


class DesignInputParameter(Parameter):
    name: str = Field(..., description="Name of the input parameter")
    value: Union[float, Tuple[float, float]] = Field(
        ..., description="Value of the input parameter"
    )


class DesignOutputParameter(Parameter):
    class Config:
        allow_mutation = False


class Interference(DesignOutputParameter):
    part_2_name: str = Field(..., description="The interfering part 1")

    part_1_name: str = Field(..., description="The interfering part 2")

    interference_volume: float = Field(..., description="The interference volume")

    @staticmethod
    def from_dicts(interferences) -> List["Interference"]:
        return [Interference(**interference) for interference in interferences]


class MassProperties(DesignOutputParameter):
    surface_area: float = Field(
        ...,
        description="The surface area",
    )

    density: float = Field(
        ...,
        description="The density",
    )

    mass: float = Field(
        ...,
        description="The mass",
    )

    coordIxx: float = Field(
        ...,
        description="The coordinate system inertia Ixx",
    )

    coordIxy: float = Field(
        ...,
        description="The coordinate system inertia Ixy",
    )

    coordIxz: float = Field(
        ...,
        description="The coordinate system inertia Ixz",
    )

    coordIyx: float = Field(
        ...,
        description="The coordinate system inertia Iyx",
    )

    coordIyy: float = Field(..., description="The coordinate system inertia Iyy")

    coordIyz: float = Field(..., description="The coordinate system inertia Iyz")

    coordIzx: float = Field(
        ...,
        description="The coordinate system inertia Izx",
    )

    coordIzy: float = Field(..., description="The coordinate system inertia Izy")

    coordIzz: float = Field(..., description="The coordinate system inertia Izz")

    cgIxx: float = Field(
        ...,
        description="The center-of-gravity inertia Ixx",
    )

    cgIxy: float = Field(
        ...,
        description="The center-of-gravity inertia Ixy",
    )

    cgIxz: float = Field(
        ...,
        description="The center-of-gravity inertia Ixz",
    )

    cgIyx: float = Field(
        ...,
        description="The center-of-gravity inertia Iyx",
    )

    cgIyy: float = Field(..., description="The center-of-gravity inertia Iyy")

    cgIyz: float = Field(..., description="The center-of-gravity inertia Iyz")

    cgIzx: float = Field(
        ...,
        description="The center-of-gravity inertia Izx",
    )

    cgIzy: float = Field(..., description="The center-of-gravity inertia Izy")

    cgIzz: float = Field(..., description="The center-of-gravity inertia Izz")

    @classmethod
    def from_creoson_dict(cls, mass_props):
        return cls(
            **{
                "surface_area": mass_props["surface_area"],
                "density": mass_props["density"],
                "mass": mass_props["mass"],
                # Coordinate System
                "coordIxx": mass_props["coord_sys_inertia_tensor"]["x_axis"]["x"],
                "coordIxy": mass_props["coord_sys_inertia_tensor"]["x_axis"]["y"],
                "coordIxz": mass_props["coord_sys_inertia_tensor"]["x_axis"]["z"],
                "coordIyx": mass_props["coord_sys_inertia_tensor"]["y_axis"]["x"],
                "coordIyy": mass_props["coord_sys_inertia_tensor"]["y_axis"]["y"],
                "coordIyz": mass_props["coord_sys_inertia_tensor"]["y_axis"]["z"],
                "coordIzx": mass_props["coord_sys_inertia_tensor"]["z_axis"]["x"],
                "coordIzy": mass_props["coord_sys_inertia_tensor"]["z_axis"]["y"],
                "coordIzz": mass_props["coord_sys_inertia_tensor"]["z_axis"]["z"],
                # Center of Gravity
                "cgIxx": mass_props["ctr_grav_inertia_tensor"]["x_axis"]["x"],
                "cgIxy": mass_props["ctr_grav_inertia_tensor"]["x_axis"]["y"],
                "cgIxz": mass_props["ctr_grav_inertia_tensor"]["x_axis"]["z"],
                "cgIyx": mass_props["ctr_grav_inertia_tensor"]["y_axis"]["x"],
                "cgIyy": mass_props["ctr_grav_inertia_tensor"]["y_axis"]["y"],
                "cgIyz": mass_props["ctr_grav_inertia_tensor"]["y_axis"]["z"],
                "cgIzx": mass_props["ctr_grav_inertia_tensor"]["z_axis"]["x"],
                "cgIzy": mass_props["ctr_grav_inertia_tensor"]["z_axis"]["y"],
                "cgIzz": mass_props["ctr_grav_inertia_tensor"]["z_axis"]["z"],
            }
        )


class CreoDesignState(BaseModel):
    parameters: List[DesignInputParameter] = Field(
        ..., description="The input parameters for the design"
    )

    interferences: List[Interference] = Field(
        ..., description="The interferences in the design"
    )
    mass_properties: MassProperties = Field(
        ..., description="The mass properties of the design"
    )

    def flat_dict(self):
        """Return a flat dictionary of parameters/massproperties/interferences."""
        flat_dict = {}
        for parameter in self.parameters:
            flat_dict[parameter.name] = parameter.value

        flat_dict["interferences"] = True if self.interferences else False
        flat_dict["number_of_interferences"] = len(self.interferences)

        flat_dict.update(self.mass_properties.dict())
        return flat_dict


class DesignSweep(BaseModel):
    parameters: List[DesignInputParameter] = Field(
        ..., description="The parameters to sweep the design from"
    )

    def fixed_params(self):
        for parameter in self.parameters:
            if isinstance(parameter.value, float):
                yield parameter.name, parameter.value

    def lhs_states(self, num_states, include_fixed=False, seed=42):
        """Yield the latin hypercube sample states for design parameters.

        Parameters
        ----------
        num_states: int
            The number of states to yield

        include_fixed: bool, default=False
            If True, include fixed values in the parameter

        seed: int, default=42
            The random seed for LHS Samples
        """
        parameter_keys = []
        u_bounds = []
        l_bounds = []
        for parameter in self.parameters:
            if isinstance(parameter.value, tuple):
                parameter_keys.append(parameter.name)
                u_bounds.append(parameter.value[-1])
                l_bounds.append(parameter.value[0])

        assert len(u_bounds) == len(l_bounds)

        sampler = LatinHypercube(d=len(u_bounds), centered=True, seed=seed)

        lhs_samples = sampler.random(n=num_states)

        parameter_samples = scale(
            sample=lhs_samples, l_bounds=l_bounds, u_bounds=u_bounds
        )

        fixed_params = {name: value for name, value in self.fixed_params()}

        for sample in parameter_samples:
            state = {key: sample[i] for i, key in enumerate(parameter_keys)}

            if include_fixed:
                state.update(fixed_params)

            yield state
