from typing import ClassVar

from pydantic import BaseModel, Field, validator

from symbench_athens_client.utils import dict_to_string


class FlightModeSettings(BaseModel):
    """The Base Flight Dyanamics Settings"""

    __attr_aliases__: ClassVar[dict] = {"analysis_type": "Analysis_Type"}

    requested_velocity: float = Field(
        10.0,
        alias="Requested_Velocity",
        description="The requested velocity for the FD-Simulation",
    )

    @property
    def analysis_type(self):
        raise NotImplemented

    def to_jenkins_parameters(self):
        params = self.parameters()
        return {"DesignVars": dict_to_string(params, repeat_values=False)}

    def parameters(self):
        params = self.dict(by_alias=True)

        for k, v in self.__attr_aliases__.items():
            if hasattr(self, k):
                params[v] = getattr(self, k)

        return params

    class Config:
        validate_assignment = True
        allow_population_by_field_name = True


class InitialConditionsFlight(FlightModeSettings):
    """The Initial Conditions Flight"""

    @property
    def analysis_type(self):
        return 1


class TrimSteadyFlight(FlightModeSettings):
    """The Trim Steady Flight"""

    @property
    def analysis_type(self):
        return 2


class FlightPathFlight(FlightModeSettings):
    """The Flight path flight"""

    __attr_aliases__: ClassVar[dict] = {
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

    q_angluar_velocity: float = Field(
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
