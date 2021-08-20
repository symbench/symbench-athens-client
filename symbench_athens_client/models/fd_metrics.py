from pydantic import BaseModel, Field


class FDMFlightMetric(BaseModel):
    max_hover_time: float = Field(
        ..., description="The maximum hover time", alias="Hover_Time"
    )

    max_lateral_speed: float = Field(
        ..., description="The maximum lateral speed", alias="Max_Speed"
    )

    max_flight_distance: float = Field(
        ..., description="The maximum flight distance", alias="Max_Distance"
    )

    speed_at_mfd: float = Field(..., description="Speed at MFD", alias="Speed_at_MFD")

    max_uc_at_mfd: float = Field(
        ..., description="Maximum uc at MFD", alias="Max_uc_at_MFD"
    )

    power_at_mfd: float = Field(..., description="Power at MFD", alias="Power_at_MFD")

    motor_amps_ratio_mfd: float = Field(
        ..., description="Motor amps ratio at MFD", alias="Mot_amps_ratio_MFD"
    )

    mot_power_ratio_mfd: float = Field(
        ..., description="Motor power ration at MFD", alias="Mot_power_ratio_MFD"
    )

    batt_amps_ratio_mfd: float = Field(
        ..., description="Battery amps at MFD", alias="Batt_amps_ratio_MFD"
    )

    distance_max_speed: float = Field(
        ..., description="Distance at maximum speed", alias="Distance_MxSpd"
    )

    power_max_speed: float = Field(
        ..., description="Power at maximum speed", alias="Power_MxSpd"
    )

    motor_power_ratio_max_speed: float = Field(
        ...,
        description="The motor power ration at max speed",
        alias="Mot_power_ratio_MxSpd",
    )

    motor_amps_ratio_max_speed: float = Field(
        ...,
        description="The motor amps ratio at max speed",
        alias="Mot_amps_ratio_MxSpd",
    )

    batt_amps_ratio_max_speed: float = Field(
        ...,
        description="The motor amps ratio at max speed",
        alias="Batt_amps_ratio_MxSpd",
    )

    def to_csv_dict(self):
        return self.dict(by_alias=True)

    @classmethod
    def from_fd_metrics(cls, metrics_file):
        fields = {
            "Battery_amps_to_max_amps_ratio_at_Max_Flight_Distance": "batt_amps_ratio_mfd",
            "Battery_amps_to_max_amps_ratio_at_Max_Speed": "batt_amps_ratio_max_speed",
            "Distance_at_Max_Speed_(m)": "distance_max_speed",
            "Max_Flight_Distance_(m)": "max_flight_distance",
            "Max_Hover_Time_(s)": "max_hover_time",
            "Max_Lateral_Speed_(m/s)": "max_lateral_speed",
            "Max_uc_at_Max_Flight_Distance": "max_uc_at_mfd",
            "Motor_amps_to_max_amps_ratio_at_Max_Flight_Distance": "motor_amps_ratio_mfd",
            "Motor_amps_to_max_amps_ratio_at_Max_Speed": "motor_amps_ratio_max_speed",
            "Motor_power_to_max_power_ratio_at_Max_Flight_Distance": "mot_power_ratio_mfd",
            "Power_at_Max_Flight_Distance_(W)": "power_at_mfd",
            "Power_at_Max_Speed_(W)": "power_max_speed",
            "Speed_at_Max_Flight_Distance_(m/s)": "speed_at_mfd",
            "Motor_power_to_max_power_ratio_at_Max_Speed": "motor_power_ratio_max_speed",
        }
        flight_metrics_dict = {}
        with open(metrics_file) as metrics_fp:
            lines = metrics_fp.readlines()
            for line in lines:
                line_splited = line.strip().split()
                if line_splited and line_splited[0] in fields:
                    flight_metrics_dict[
                        fields[line_splited[0]]
                    ] = cls.get_float_from_line(line)

        return cls(**flight_metrics_dict)

    @staticmethod
    def get_float_from_line(line):
        return float(line.strip().split()[-1])

    class Config:
        allow_mutation = False
        allow_population_by_field_name = True


class FDMFlightPathMetric(BaseModel):
    flight_path: int = Field(0.0, description="The flight path", alias="FLIGHT_PATH")

    average_speed: float = Field(
        ..., description="The average speed", alias="Avg_speed_path"
    )

    flight_distance: float = Field(
        ..., description="The flight distance", alias="Flight_dist"
    )

    maximum_error_distance_during_flight: float = Field(
        ..., description="Mx_error_flight", alias="Mx_error_flight"
    )

    path_score: float = Field(..., description="Path_score", alias="Path_score")

    average_error: float = Field(
        ..., description="Avg_error_fight", alias="Avg_error_fight"
    )

    time_to_traverse_path: float = Field(
        ..., description="Time_path", alias="Time_path"
    )

    def to_csv_dict(self):
        """Convert metrics to a CSV dictionary"""
        self_dict = self.dict(by_alias=True, exclude={"flight_path"})
        csv_dict = {}
        for key, value in self_dict.items():
            csv_dict[f"{key}_Path{self.flight_path}"] = value
        return csv_dict

    @classmethod
    def from_fd_metrics(cls, metrics_file):
        """Return an instance of path metrics from this metrics file"""
        with open(metrics_file) as metrics_fp:
            lines = metrics_fp.readlines()
            for line in lines:
                if line.strip().startswith("Path performance"):
                    flight_path = int(line.strip().split()[-1])
                if line.strip().startswith("Flight_distance"):
                    flight_distance = cls.get_float_from_line(line)
                if line.strip().startswith("Time_to_traverse_path"):
                    time = cls.get_float_from_line(line)
                if line.strip().startswith("Average_speed_to_traverse_path"):
                    average_speed = cls.get_float_from_line(line)
                if line.strip().startswith("Maximimum_error_distance_during_flight"):
                    maximum_error_distance_during_flight = cls.get_float_from_line(line)
                if line.strip().startswith("Spatial_average_distance_error"):
                    average_error = cls.get_float_from_line(line)
                if line.strip().startswith("Path_traverse_score_based_on_requirements"):
                    path_score = cls.get_float_from_line(line)

        return cls(
            flight_path=flight_path,
            flight_distance=flight_distance,
            time_to_traverse_path=time,
            maximum_error_distance_during_flight=maximum_error_distance_during_flight,
            average_error=average_error,
            path_score=path_score,
            average_speed=average_speed,
        )

    @staticmethod
    def get_float_from_line(line):
        return float(line.strip().split()[-1])

    class Config:
        allow_mutation = False
        allow_population_by_field_name = True
