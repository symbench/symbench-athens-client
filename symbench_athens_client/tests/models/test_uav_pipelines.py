import pytest

from symbench_athens_client.models.designs import QuadCopter
from symbench_athens_client.models.uav_pipelines import (
    CircularFlight,
    InitialConditionsFlight,
    RacingOvalFlight,
    RiseAndHoverFlight,
    StraightLineFlight,
    TrimSteadyFlight,
)


class TestFlightModes:
    @pytest.fixture(scope="session")
    def initial_conditions_flight(self):
        return InitialConditionsFlight(design=QuadCopter(design=QuadCopter()))

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

    def test_initial_conditions_flight_parameters(self, initial_conditions_flight):
        initial_conditions_flight.requested_velocity = 25.0
        assert (
            initial_conditions_flight.dict(by_alias=True)["Requested_Velocity"] == 25.0
        )
        assert (
            "Requested_Velocity=25.0 Analysis_Type=1"
            in initial_conditions_flight.to_jenkins_parameters()["DesignVars"]
        )

    def test_trim_flight_parameters(self, trim_flight):
        trim_flight.requested_velocity = 25.0
        assert trim_flight.dict(by_alias=True)["Requested_Velocity"] == 25.0
        assert (
            "Requested_Velocity=25.0 Analysis_Type=2"
            in trim_flight.to_jenkins_parameters()["DesignVars"]
        )

    def test_straight_line_flight_parameters(self, straight_line_flight):
        straight_line_flight.requested_velocity = 25
        straight_line_flight.requested_lateral_speed = 100
        straight_line_flight.r = 10
        assert straight_line_flight.dict(by_alias=True)["Requested_Velocity"] == 25.0
        assert straight_line_flight.dict(by_alias=True)["R"] == 10.0
        assert (
            straight_line_flight.dict(by_alias=True)["Requested_Lateral_Speed"] == 100.0
        )
        assert (
            "Requested_Velocity=25.0 Requested_Lateral_Speed=100.0 Q_Position=1.0 Q_Velocity=1.0 Q_Angular_velocity=1.0 Q_Angles=1.0 R=10.0 Analysis_Type=3 Flight_Path=1"
            in straight_line_flight.to_jenkins_parameters()["DesignVars"]
        )

    def test_circular_flight_parameters(self, circular_flight):
        circular_flight.q_angles = 90
        circular_flight.requested_lateral_speed = 10
        circular_flight.q_position = 100
        assert (
            "Requested_Velocity=10.0 Requested_Lateral_Speed=10.0 Q_Position=100.0 Q_Velocity=1.0 Q_Angular_velocity=1.0 Q_Angles=90.0 R=1.0 Analysis_Type=3 Flight_Path=3"
            in circular_flight.to_jenkins_parameters()["DesignVars"]
        )

    def test_rise_and_hover_flight_parameters(self, rise_and_hover_flight):
        assert (
            "Requested_Velocity=10.0 Requested_Lateral_Speed=0.0 Q_Position=1.0 Q_Velocity=1.0 Q_Angular_velocity=1.0 Q_Angles=1.0 R=1.0 Analysis_Type=3 Flight_Path=4"
            in rise_and_hover_flight.to_jenkins_parameters()["DesignVars"]
        )

    def test_racing_oval_flight_parameters(self, racing_oval_flight):
        assert racing_oval_flight.flight_path == 5
