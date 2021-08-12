import pytest

from symbench_athens_client.models.flight_modes import (
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
        return InitialConditionsFlight()

    @pytest.fixture(scope="session")
    def trim_flight(self):
        return TrimSteadyFlight()

    @pytest.fixture(scope="session")
    def straight_line_flight(self):
        return StraightLineFlight()

    @pytest.fixture(scope="session")
    def circular_flight(self):
        return CircularFlight()

    @pytest.fixture(scope="session")
    def rise_and_hover_flight(self):
        return RiseAndHoverFlight()

    @pytest.fixture(scope="session")
    def racing_oval_flight(self):
        return RacingOvalFlight()

    def test_initial_conditions_flight_parameters(self, initial_conditions_flight):
        initial_conditions_flight.requested_velocity = 25.0
        assert initial_conditions_flight.parameters()["Requested_Velocity"] == 25.0
        assert initial_conditions_flight.parameters()["Analysis_Type"] == 1
        assert (
            initial_conditions_flight.to_jenkins_parameters()["DesignVars"]
            == "Requested_Velocity=25.0 Analysis_Type=1"
        )

    def test_trim_flight_parameters(self, trim_flight):
        trim_flight.requested_velocity = 25.0
        assert trim_flight.parameters()["Requested_Velocity"] == 25.0
        assert trim_flight.parameters()["Analysis_Type"] == 2
        assert (
            trim_flight.to_jenkins_parameters()["DesignVars"]
            == "Requested_Velocity=25.0 Analysis_Type=2"
        )

    def test_straight_line_flight_parameters(self, straight_line_flight):
        straight_line_flight.requested_velocity = 25
        straight_line_flight.requested_lateral_speed = 100
        straight_line_flight.r = 10
        assert straight_line_flight.parameters()["Requested_Velocity"] == 25.0
        assert straight_line_flight.parameters()["R"] == 10.0
        assert straight_line_flight.parameters()["Requested_Lateral_Speed"] == 100.0
        assert straight_line_flight.parameters()["Flight_Path"] == 1
        assert (
            straight_line_flight.to_jenkins_parameters()["DesignVars"]
            == "Requested_Velocity=25.0 Requested_Lateral_Speed=100.0 Q_Position=1.0 Q_Velocity=1.0 Q_Angular_velocity=1.0 Q_Angles=1.0 R=10.0 Analysis_Type=3 Flight_Path=1"
        )

    def test_circular_flight_parameters(self, circular_flight):
        circular_flight.q_angles = 90
        circular_flight.requested_lateral_speed = 10
        circular_flight.q_position = 100
        assert circular_flight.parameters()["Requested_Velocity"] == 10.0
        assert circular_flight.parameters()["R"] == 1.0
        assert circular_flight.parameters()["Requested_Lateral_Speed"] == 10.0
        assert circular_flight.parameters()["Flight_Path"] == 3
        assert (
            circular_flight.to_jenkins_parameters()["DesignVars"]
            == "Requested_Velocity=10.0 Requested_Lateral_Speed=10.0 Q_Position=100.0 Q_Velocity=1.0 Q_Angular_velocity=1.0 Q_Angles=90.0 R=1.0 Analysis_Type=3 Flight_Path=3"
        )

    def test_rise_and_hover_flight_parameters(self, rise_and_hover_flight):
        assert (
            rise_and_hover_flight.to_jenkins_parameters()["DesignVars"]
            == "Requested_Velocity=10.0 Requested_Lateral_Speed=0.0 Q_Position=1.0 Q_Velocity=1.0 Q_Angular_velocity=1.0 Q_Angles=1.0 R=1.0 Analysis_Type=3 Flight_Path=4"
        )

    def test_racing_oval_flight_parameters(self, racing_oval_flight):
        assert racing_oval_flight.parameters()["Flight_Path"] == 5
