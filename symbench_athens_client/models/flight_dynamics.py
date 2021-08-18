from uuid import uuid4

from pydantic import BaseModel, Field


class FlightDynamicsOutput(BaseModel):
    guid: str = Field(
        default_factory=lambda: str(uuid4()),
        description="The GUID of this flight dynamics output",
        alias="GUID",
    )

    analysis_error: bool = Field(
        ..., description="The analysis error", alias="AnalysisError"
    )

    total_path_score: float = Field(
        ..., description="The total path score of this analysis", alias="TotalPathScore"
    )

    interferences: int = Field(..., description="Interferences", alias="Interferences")

    ixx: float = Field(..., description="xx of moment of inertia tensor I", alias="Ixx")

    iyy: float = Field(..., description="yy of moment of inertia tensor I", alias="iyy")

    izz: float = Field(..., description="zz of moment of inertia tensor I", alias="Izz")

    mass_estimate: float = Field(
        ..., description="The mass estimate", alias="MassEstimate"
    )

    avg_speed_path1: float = Field(
        ..., description="The average speed", alias="Avg_speed_path_Path1"
    )

    battery_amps_ratio_mfd: float = Field(
        ..., description="Batt_amps_ratio_MFD", alias="Batt_amps_ratio_MFD"
    )

    battery_amps_mx_speed: float = Field(
        ..., description="Batt_amps_ratio_MxSpd", alias="Batt_amps_ratio_MxSpd"
    )

    distance_max_speed: float = Field(
        ..., description="Distance_MxSpd", alias="Distance_MxSpd"
    )

    flight_distance_path_1: float = Field(
        ..., description="Flight_dist_Path1", alias="Flight_dist_Path1"
    )

    max_distance: float = Field(..., description="Max_Distance", alias="Max_Distance")

    hover_time: float = Field(..., description="Hover_Time", alias="Hover_Time")

    max_speed: float = Field(..., description="Max_Speed", alias="Max_Speed")

    max_uc_at_mfd: float = Field(
        ..., description="Max_Speed_At_MFD", alias="Max_uc_at_MFD"
    )

    mx_error_flight_path_1: float = Field(
        ..., description="Mx_error_flight_Path1", alias="Mx_error_flight_Path1"
    )

    mot_amps_ratio_mfd: float = Field(
        ..., description="Mot_amps_ratio_MFD", alias="Mot_amps_ratio_MFD"
    )

    mot_amps_ratio_mxspeed: float = Field(
        ..., description="Mot_amps_ratio_MxSpd", alias="Mot_amps_ratio_MxSpd"
    )

    mot_power_ratio_mfd: float = Field(
        ..., description="Mot_power_ratio_MFD", alias="Mot_power_ratio_MFD"
    )

    mot_power_ratio_mxspd: float = Field(
        ..., description="Mot_power_ratio_MxSpd", alias="Mot_power_ratio_MxSpd"
    )

    path_score_1: float = Field(
        ..., description="Path_score_Path1", alias="Path_score_Path1"
    )

    power_at_mfd: float = Field(..., description="Power_at_MFD", alias="Power_at_MFD")

    power_mx_speed: float = Field(..., description="Power_MxSpd", alias="Power_MxSpd")

    avg_error_flight_path_1: float = Field(
        ..., description="Avg_error_fight_Path1", alias="Avg_error_fight_Path1"
    )

    time_path_path_1: float = Field(..., description="Speed_at_MFD")

    Time_path_Path1
    Avg_speed_path_Path3
    Flight_dist_Path3
    Mx_error_flight_Path3
    Path_score_Path3
    Avg_error_fight_Path3
    Time_path_Path3
    Avg_speed_path_Path4
    Flight_dist_Path4
    Mx_error_flight_Path4
    Path_score_Path4
    Avg_error_fight_Path4
    Time_path_Path4
    Avg_speed_path_Path5
    Flight_dist_Path5
    Mx_error_flight_Path5
    Path_score_Path5
    Avg_error_fight_Path5
    Time_path_Path5
    Length_0
    Length_1
    Length_2
    Length_3
    Length_4
    Length_5
    Length_6
    Length_7
    Length_8
    Length_9
    Param_0
    Param_1
    Param_2
    Param_3
    Param_4
    Param_5
    Param_6
    Param_7
    Param_8
    Param_9
    Q_Angles
    Q_Angular_Velocity
    Q_Position
    Q_Velocity
    R
    Requested_Lateral_Speed
    Requested_Vertical_Speed

    class Config:
        allow_mutation = False
