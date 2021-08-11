import pytest

from symbench_athens_client.models.components import (
    Batteries,
    ESCs,
    Flanges,
    Hubs,
    Propellers,
    Tubes,
)
from symbench_athens_client.models.designs import (
    HCopter,
    HPlane,
    QuadCopter,
    QuadSpiderCopter,
)


class TestDesigns:
    @pytest.fixture(scope="session")
    def qd_copter(self):
        return QuadCopter()

    @pytest.fixture(scope="session")
    def qd_spider_copter(self):
        return QuadSpiderCopter()

    @pytest.fixture(scope="session")
    def h_plane(self):
        return HPlane()

    @pytest.fixture(scope="session")
    def h_copter(self):
        return HCopter()

    def test_quadcopter_jenkins_params(self, qd_copter):
        params = qd_copter.to_jenkins_parameters()
        assert (
            params["DesignVars"]
            == "Length_0=220.0,220.0 Length_1=95.0,95.0 Length_8=0.0,0.0 Length_9=0.0,0.0"
        )

    def test_quadspider_copter_jenkins_params(self, qd_spider_copter):
        params = qd_spider_copter.to_jenkins_parameters()
        assert (
            params["DesignVars"]
            == "Length_0=220.0,220.0 Length_1=155.0,155.0 Length_2=80.0,80.0 Length_3=80.0,80.0 Length_8=0.0,0.0 Length_9=0.0,0.0 Param_0=120.0,120.0"
        )

    def test_hplane_jenkins_params(self, h_plane):
        params = h_plane.to_jenkins_parameters()
        assert (
            params["DesignVars"]
            == "Length_1=320.0,320.0 Length_8=0.0,0.0 Length_9=0.0,0.0"
        )

    def test_hcopter_jenkins_params(self, h_copter):
        params = h_copter.to_jenkins_parameters()
        assert (
            params["DesignVars"]
            == "Length_0=500.0,500.0 Length_1=95.0,95.0 Length_8=0.0,0.0 Length_9=0.0,0.0"
        )

    def test_design_params_after_change(self, h_copter):
        h_copter_copy = h_copter.copy(deep=True)
        h_copter_copy.support_length = 220
        params = h_copter_copy.to_jenkins_parameters()
        assert (
            params["DesignVars"]
            == "Length_0=500.0,500.0 Length_1=220.0,220.0 Length_8=0.0,0.0 Length_9=0.0,0.0"
        )

    def test_components_qd_copter(self, qd_copter):
        assert qd_copter.battery_0 == Batteries.TurnigyGraphene1000mAh2S75C
        assert qd_copter.esc_0 == ESCs.ESC_debugging
        assert qd_copter.hub_4_way == Hubs["0394od_para_hub_4"]
        assert qd_copter.support_0 == Tubes["0394OD_para_tube"]

    def test_components_qd_spider_copter(self, qd_spider_copter):
        assert qd_spider_copter.bend_0a == Hubs["0394od_para_hub_2"]
        assert qd_spider_copter.flange_0 == Flanges["0394_para_flange"]
        assert qd_spider_copter.propeller_0 == Propellers["apc_propellers_10x7E"]

    def test_components_h_copter(self, h_copter):
        assert h_copter.arm_left_center == Tubes["0394OD_para_tube"]
        assert h_copter.support_3 == Tubes["0394OD_para_tube"]

    def test_components_h_plane(self, h_plane):
        assert h_plane.rear_prop_l == Propellers["apc_propellers_4_75x4_75EP"]
        assert h_plane.rear_prop_r == Propellers["apc_propellers_4_75x4_75E"]
        assert h_plane.rear_tube_c == Tubes["0394OD_para_tube"]
