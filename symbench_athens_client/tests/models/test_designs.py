import pytest
from pydantic import ValidationError

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
            == "Length_0=220.0,220.0 Length_1=95.0,95.0 Length_2=0.0,0.0 Length_3=0.0,0.0"
        )

    def test_quadcopter_jenkins_params(self, qd_spider_copter):
        params = qd_spider_copter.to_jenkins_parameters()
        assert (
            params["DesignVars"]
            == "Length_0=220.0,220.0 Length_1=155.0,155.0 Length_2=80.0,80.0 Length_3=80.0,80.0 Length_4=0.0,0.0 Length_5=0.0,0.0 Param_0=120.0,120.0"
        )

    def test_hplane_jenkins_params(self, h_plane):
        params = h_plane.to_jenkins_parameters()
        assert params["DesignVars"] == "Length_1=320.0,320.0"

    def test_hcopter_jenkins_params(self, h_copter):
        params = h_copter.to_jenkins_parameters()
        assert (
            params["DesignVars"]
            == "Length_0=500.0,500.0 Length_1=95.0,95.0 Length_2=0.0,0.0 Length_3=0.0,0.0"
        )
