from symbench_athens_client.models.designs import QuadCopter, QuadSpiderCopter
from symbench_athens_client.uav_workflows_mock import (
    fly_circle,
    fly_racing_oval,
    fly_rise_and_hover,
    fly_straight_line,
    fly_trim_steady,
    fly_with_initial_conditions,
)


class TestUAVWorkflowsMock:
    def test_fly_with_initial_conditions(self):
        design = QuadCopter()
        design.arm_length = 330.0
        params = fly_with_initial_conditions(
            design, num_samples=29, requested_velocity=20.0
        )
        assert params["NumSamples"] == 29
        assert params["PETName"] == "/D_Testing/PET/FlightDyn_V1"
        assert "Requested_Velocity=20.0" in params["DesignVars"]
        assert "Length_0=330.0,330.0" in params["DesignVars"]

    def test_fly_trim_steady(self):
        design = QuadSpiderCopter()
        params = fly_trim_steady(design=design, requested_velocity=45.25)
        assert "Requested_Velocity=45.25" in params["DesignVars"]

    def test_fly_circle(self):
        design = QuadCopter()
        params = fly_circle(design, num_samples=2, requested_lateral_speed=25.600)
        assert params["NumSamples"] == 2
        assert "Requested_Lateral_Speed=25.6" in params["DesignVars"]

    def test_rise_and_hover(self):
        design = QuadSpiderCopter()
        params = fly_rise_and_hover(design, num_samples=30, r=300)
        assert params["NumSamples"] == 30
        assert "Flight_Path=4" in params["DesignVars"]

    def test_fly_straight_line(self):
        design = QuadCopter()
        params = fly_straight_line(design, num_samples=35, Q_Angles=24)
        assert "Q_Angles=24.0" in params["DesignVars"]
        assert "Flight_Path=1" in params["DesignVars"]
        assert "Analysis_Type=3" in params["DesignVars"]

    def test_fly_racing_oval(self):
        design = QuadSpiderCopter(arm_length=330)
        params = fly_racing_oval(design, requested_velocity=0)
        assert "Requested_Velocity=0.0" in params["DesignVars"]
