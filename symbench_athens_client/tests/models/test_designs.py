import pytest
from pydantic import ValidationError

from symbench_athens_client.models.designs import QuadCopter, QuadSpiderCopter


class TestDesigns:
    @pytest.fixture(scope="session")
    def qd_copter(self):
        return QuadCopter()

    @pytest.fixture(scope="session")
    def qd_spider_copter(self):
        return QuadSpiderCopter()

    def test_quadcopter_jenkins_params(self, qd_copter):
        params = qd_copter.to_jenkins_parameters()
        assert "Length_0" in params
        assert "Length_1" in params
        assert "Length_2" in params
        assert "Length_3" in params

    def test_quadcopter_jenkins_params(self, qd_spider_copter):
        params = qd_spider_copter.to_jenkins_parameters()
        assert "Length_0" in params
        assert "Length_1" in params
        assert "Length_2" in params
        assert "Length_3" in params
        assert "Rot_a" in params
        assert "Rot_b" in params
        assert "Length_4" in params
        assert "Length_5" in params

    def test_qd_spider_sum_non_zero(self):
        with pytest.raises(ValidationError):
            QuadSpiderCopter(rot_a=90, rot_b=189)
