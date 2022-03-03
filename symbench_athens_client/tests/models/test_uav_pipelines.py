import pytest

from symbench_athens_client.models.uam_designs import Rake
from symbench_athens_client.models.uav_designs import QuadCopter
from symbench_athens_client.models.uav_pipelines import (
    CircularFlight,
    FlightPathsAll,
    InitialConditionsFlight,
    RacingOvalFlight,
    RiseAndHoverFlight,
    StraightLineFlight,
    TrimSteadyFlight,
)


class TestFlightModes:
    @pytest.fixture(scope="session")
    def initial_conditions_flight(self):
        return InitialConditionsFlight(design=QuadCopter())

    @pytest.fixture(scope="session")
    def trim_flight(self):
        return TrimSteadyFlight(design=QuadCopter())

    @pytest.fixture(scope="session")
    def straight_line_flight(self):
        return StraightLineFlight(design=QuadCopter())

    @pytest.fixture(scope="session")
    def circular_flight(self):
        return CircularFlight(design=QuadCopter())

    @pytest.fixture(scope="session")
    def rise_and_hover_flight(self):
        return RiseAndHoverFlight(design=QuadCopter())

    @pytest.fixture(scope="session")
    def racing_oval_flight(self):
        return RacingOvalFlight(design=QuadCopter())

    @pytest.fixture(scope="session")
    def all_flights_path(self):
        return FlightPathsAll(design=QuadCopter())

    def test_initial_conditions_flight_parameters(self, initial_conditions_flight):
        assert (
            "Analysis_Type=1"
            in initial_conditions_flight.to_jenkins_parameters()["DesignVars"]
        )

    def test_trim_flight_parameters(self, trim_flight):
        assert "Analysis_Type=2" in trim_flight.to_jenkins_parameters()["DesignVars"]

    def test_straight_line_flight_parameters(self, straight_line_flight):
        straight_line_flight.requested_lateral_speed = 100
        straight_line_flight.design.r = 10
        straight_line_flight.requested_vertical_speed = 200
        assert straight_line_flight.design.dict(by_alias=True)["R"] == 10.0
        assert (
            straight_line_flight.dict(by_alias=True)["Requested_Lateral_Speed"] == 100.0
        )

        assert (
            "Analysis_Type=3,3 Flight_Path=1,1"
            in straight_line_flight.to_jenkins_parameters()["DesignVars"]
        )

    def test_circular_flight_parameters(self, circular_flight):
        circular_flight.design.q_angles = 90
        circular_flight.requested_lateral_speed = 10
        circular_flight.design.q_position = 100

        assert (
            "Q_Position=100.0,100.0 Q_Velocity=1.0,1.0 Q_Angular_Velocity=1.0,1.0 Q_Angles=90.0,90.0 R=1.0,1.0 Length_0=220.0,220.0"
            in circular_flight.to_jenkins_parameters()["DesignVars"]
        )

    def test_rise_and_hover_flight_parameters(self, rise_and_hover_flight):

        assert (
            "Q_Angular_Velocity=1.0,1.0 Q_Angles=1.0,1.0 R=1.0,1.0"
            in rise_and_hover_flight.to_jenkins_parameters()["DesignVars"]
        )

    def test_racing_oval_flight_parameters(self, racing_oval_flight):
        assert racing_oval_flight.flight_path == 5

    def test_fly_circle_sweep(self, circular_flight):
        circular_flight.design.q_angles = 25, 90
        circular_flight.requested_vertical_speed = 100.0, 200.5
        assert (
            "Q_Angles=25.0,90.0"
            in circular_flight.to_jenkins_parameters()["DesignVars"]
        )
        assert (
            "Requested_Vertical_Speed=100.0,200.5"
            in circular_flight.to_jenkins_parameters()["DesignVars"]
        )

    def test_flight_paths_all(self, all_flights_path):
        assert (
            "Analysis_Type"
            not in all_flights_path.to_jenkins_parameters()["DesignVars"]
        )
        assert (
            "Flight_Path" not in all_flights_path.to_jenkins_parameters()["DesignVars"]
        )
        assert (
            all_flights_path.to_jenkins_parameters()["PETName"]
            == "/D_Testing/PET/FlightDyn_V1_AllPaths"
        )

    def test_fd_all_paths_pet_name(self):
        quadcopter_pipeline = FlightPathsAll(design=QuadCopter())

        assert quadcopter_pipeline.pet_name == "/D_Testing/PET/FlightDyn_V1_AllPaths"

        rake_pipeline = FlightPathsAll(design=Rake())

        assert rake_pipeline.pet_name == "/D_Testing/PET/FlightDyn_V2"
