from typing import ClassVar, Tuple, Union

from pydantic import Field, validator

from symbench_athens_client.models.designs import SeedDesign
from symbench_athens_client.models.pipelines import JenkinsPipeline
from symbench_athens_client.utils import dict_to_design_vars


class UAVWorkflows(JenkinsPipeline):
    """UAV_Workflows pipeline."""

    __attr_aliases__: ClassVar[dict] = {"pet_name": "PETName"}

    @property
    def pipeline_name(self):
        return "UAV_Workflows"

    @property
    def pet_name(self):
        raise NotImplementedError

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
        params["graphGUID"] = self.design.name

        params.update(self.design.to_jenkins_parameters())
        params["DesignVars"] = '"' + params["DesignVars"] + '"'
        return params

    def design_vars(self):
        design_vars = self.parameters()["DesignVars"][1:-1]
        return dict(var.split("=") for var in design_vars.split(" "))


class HoverCalc(UAVWorkflows):
    """The `HoverCalc_V1` TestBench for UAV_Workflows."""

    @property
    def pet_name(self):
        return "/D_Testing/PET/HoverCalc_V1"


class GeometryV1(UAVWorkflows):
    """The `Geometry_V1` TestBench for UAV_Workflows."""

    @property
    def pet_name(self):
        return "/D_Testing/PET/Geom_V1"


class FlightDynamicsV1(UAVWorkflows):
    """The Base `FlightDyn_V1` TestBench for UAV_Workflows."""

    __design_vars__: ClassVar = {}

    __fixed_design_vars__: ClassVar[dict] = {"analysis_type": "Analysis_Type"}

    @property
    def analysis_type(self):
        raise NotImplementedError

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
        params["graphGUID"] = self.design.name
        design_params = self.design.to_jenkins_parameters()
        design_vars_parametric = dict_to_design_vars(
            self.dict(by_alias=True, include=self.__design_vars__),
            repeat_values=True,
        )
        design_vars_fixed = dict_to_design_vars(
            {v: getattr(self, k) for k, v in self.__fixed_design_vars__.items()},
            repeat_values=True,
        )
        params["DesignVars"] = " ".join(
            [design_params["DesignVars"], design_vars_parametric, design_vars_fixed]
        ).strip()
        params["DesignVars"] = '"' + params["DesignVars"] + '"'
        return params


class InitialConditionsFlight(FlightDynamicsV1):
    """The InitialConditions Flight, using `analysis_type=1` in `FlightDynamics`."""

    @property
    def analysis_type(self):
        return 1


class TrimSteadyFlight(FlightDynamicsV1):
    """The Trim Steady Flight, using `analysis_type=2` in `FlightDyanmics`."""

    @property
    def analysis_type(self):
        return 2


class FlightPathFlight(FlightDynamicsV1):
    """The Flight path flight, using `analysis_type=3`(has many subclasses)."""

    __design_vars__: ClassVar[set] = {
        "requested_lateral_speed",
        "requested_vertical_speed",
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
        raise NotImplementedError

    requested_lateral_speed: Union[float, Tuple[float, float]] = Field(
        default=10.0,
        alias="Requested_Lateral_Speed",
        description="The requested lateral speed",
    )

    requested_vertical_speed: Union[float, Tuple[float, float]] = Field(
        default=1.0,
        alias="Requested_Vertical_Speed",
        description="The requested vertical speed",
    )

    q_position: Union[float, Tuple[float, float]] = Field(
        default=1.0, alias="Q_Position", description="The Q-Position"
    )

    q_velocity: Union[float, Tuple[float, float]] = Field(
        default=1.0, description="The Q-Velocity", alias="Q_Velocity"
    )

    q_angular_velocity: Union[float, Tuple[float, float]] = Field(
        default=1.0, description="The Q-Angular Velocity", alias="Q_Angular_velocity"
    )

    q_angles: Union[float, Tuple[float, float]] = Field(
        1.0, description="The Q-Angles", alias="Q_Angles"
    )

    r: Union[float, Tuple[float, float]] = Field(
        1.0, description="The R-Parameter", alias="R"
    )

    @validator(*__design_vars__, pre=True, always=True)
    def validate_design_vars_tuple(cls, value):
        if isinstance(value, Tuple):
            assert (
                value[0] <= value[1]
            ), "The first element should be less than the second one; while using ranges"
        return value


class FlightPathsAll(FlightPathFlight):
    """Run all the FlightPathFlights' Analysis (1, 3, 4 and 5)"""

    __fixed_design_vars__ = {}

    @property
    def pet_name(self):
        return "/D_Testing/PET/FlightDyn_V1_AllPaths"


class StraightLineFlight(FlightPathFlight):
    """The Straight line flight, subclasses `FlightPathFlight`, `analysis_type=3`, `flight_path=1`."""

    @property
    def flight_path(self):
        return 1


class CircularFlight(FlightPathFlight):
    """The Circular flight, subclasses `FlightPathFlight`, `analysis_type=3`, `flight_path=3`."""

    @property
    def flight_path(self):
        return 3


class RiseAndHoverFlight(FlightPathFlight):
    """The rise and hover flight, subclasses `FlightPathFlight`, `analysis_type=3`, `flight_path=4`."""

    @property
    def flight_path(self):
        return 4

    @validator("requested_lateral_speed", pre=True, always=True)
    def validate_lateral_speed(cls, value):
        if value != 0.0:
            value = 0.0
        return value


class RacingOvalFlight(FlightPathFlight):
    """The racing oval flight, subclasses FlightPathFlight, `analysis_type=3`, `flight_path=5`."""

    @property
    def flight_path(self):
        return 5
