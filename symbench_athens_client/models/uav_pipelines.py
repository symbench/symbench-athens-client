from typing import ClassVar

from pydantic import Field, validator

from symbench_athens_client.models.designs import SeedDesign
from symbench_athens_client.models.pipelines import JenkinsPipeline
from symbench_athens_client.utils import dict_to_string


class UAVWorkflows(JenkinsPipeline):
    __attr_aliases__: ClassVar[dict] = {"pet_name": "PETName"}

    @property
    def pipeline_name(self):
        return "UAV_Workflows"

    @property
    def pet_name(self):
        raise NotImplemented

    design: SeedDesign = Field(
        ...,
        description="The Name in JanusGraph of the top level/Root node in your design graph (not currently used)",
    )

    num_samples: int = Field(
        1,
        description="Number of samples to execute for Monte Carlo DOE, uniformly sampled",
        alias="NumSamples",
    )

    def to_jenkins_parameters(self):
        return self.parameters()

    def parameters(self):
        params = self.dict(by_alias=True, exclude={"design"})

        for k, v in self.__attr_aliases__.items():
            if hasattr(self, k):
                params[v] = getattr(self, k)
        params["GraphGUID"] = self.design.name

        params.update(self.design.to_jenkins_parameters())
        params["DesignVars"] = '"' + params["DesignVars"] + '"'
        return params

    def design_vars(self):
        design_vars = self.parameters()["DesignVars"][1:-1]
        return dict(var.split("=") for var in design_vars.split(" "))


class HoverCalc(UAVWorkflows):
    @property
    def pet_name(self):
        return "/D_Testing/PET/HoverCalc_V1"


class GeometryV1(UAVWorkflows):
    @property
    def pet_name(self):
        return "/D_Testing/PET/Geom_V1"


class FlightDynamicsV1(UAVWorkflows):
    """The Base Flight Dyanamics Workflow"""

    __design_vars__: ClassVar[dict] = {"requested_velocity"}

    __fixed_design_vars__: ClassVar[dict] = {"analysis_type": "Analysis_Type"}

    requested_velocity: float = Field(
        10.0,
        alias="Requested_Velocity",
        description="The requested velocity for the FD-Simulation",
    )

    @property
    def analysis_type(self):
        raise NotImplemented

    @property
    def pet_name(self):
        return "/D_Testing/PET/FlightDyn_V1"

    def to_jenkins_parameters(self):
        return self.parameters()

    def parameters(self):
        params = self.dict(
            by_alias=True, exclude={"design"}.union(self.__design_vars__)
        )
        for k, v in self.__attr_aliases__.items():
            if hasattr(self, k):
                params[v] = getattr(self, k)
        params["GraphGUID"] = self.design.name
        design_params = self.design.to_jenkins_parameters()
        design_vars_parametric = dict_to_string(
            self.dict(by_alias=True, include=self.__design_vars__), repeat_values=False
        )
        design_vars_fixed = dict_to_string(
            {v: getattr(self, k) for k, v in self.__fixed_design_vars__.items()},
            repeat_values=False,
        )
        params["DesignVars"] = " ".join(
            [design_params["DesignVars"], design_vars_parametric, design_vars_fixed]
        )
        params["DesignVars"] = '"' + params["DesignVars"] + '"'
        return params


class InitialConditionsFlight(FlightDynamicsV1):
    """The Initial Conditions Flight"""

    @property
    def analysis_type(self):
        return 1


class TrimSteadyFlight(FlightDynamicsV1):
    """The Trim Steady Flight"""

    @property
    def analysis_type(self):
        return 2


class FlightPathFlight(FlightDynamicsV1):
    """The Flight path flight"""

    __design_vars__: ClassVar[dict] = {
        "requested_velocity",
        "requested_lateral_speed",
        "q_position",
        "q_velocity",
        "q_angular_velocity",
        "q_angles",
        "r",
    }
    __fixed_design_vars__: ClassVar[dict] = {
        "analysis_type": "Analysis_Type",
        "flight_path": "Flight_Path",
    }

    @property
    def analysis_type(self):
        return 3

    @property
    def flight_path(self):
        raise NotImplemented

    requested_lateral_speed: float = Field(
        default=10.0,
        alias="Requested_Lateral_Speed",
        description="The requested lateral speed",
    )

    q_position: float = Field(
        default=1.0, alias="Q_Position", description="The Q-Position"
    )

    q_velocity: float = Field(
        default=1.0, description="The Q-Velocity", alias="Q_Velocity"
    )

    q_angular_velocity: float = Field(
        default=1.0, description="The Q-Angular Velocity", alias="Q_Angular_velocity"
    )

    q_angles: float = Field(1.0, description="The Q-Angles", alias="Q_Angles")

    r: float = Field(1.0, description="The R-Parameter", alias="R")


class StraightLineFlight(FlightPathFlight):
    """The Straight line flight"""

    @property
    def flight_path(self):
        return 1


class CircularFlight(FlightPathFlight):
    """The Circular flight"""

    @property
    def flight_path(self):
        return 3


class RiseAndHoverFlight(FlightPathFlight):
    """The rise and hover flight"""

    @property
    def flight_path(self):
        return 4

    @validator("requested_lateral_speed", pre=True, always=True)
    def validate_lateral_speed(cls, value):
        if value != 0.0:
            value = 0.0
        return value


class RacingOvalFlight(FlightPathFlight):
    """The racing oval flight"""

    @property
    def flight_path(self):
        return 5
