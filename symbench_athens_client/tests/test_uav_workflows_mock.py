from symbench_athens_client.models.designs import QuadCopter
from symbench_athens_client.uav_workflows_mock import (
    fly_circle,
    fly_rise_and_hover,
    fly_straight_line,
    fly_trim_steady,
    fly_with_initial_conditions,
    racing_oval_flight,
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
