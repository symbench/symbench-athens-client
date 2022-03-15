import pytest
from pydantic import ValidationError

from symbench_athens_client.models.design_state_creo import (
    CreoDesignState,
    Interference,
    MassProperties,
    Parameter,
)


class TestDesignStateCreo:
    def test_interference(self):
        with pytest.raises(ValidationError):
            interference = Interference(
                part_1_name="ABC",
                part_2_name="XYZ",
            )
