import pytest
from pydantic import ValidationError

from symbench_athens_client.models.design_state_creo import (
    CreoDesignState,
    DesignInputParameter,
    DesignSweep,
    Interference,
    MassProperties,
)


class TestDesignStateCreo:
    def test_interference(self):
        with pytest.raises(ValidationError):
            interference = Interference(
                part_1_name="ABC",
                part_2_name="XYZ",
            )

    def test_design_sweep(self):
        param_0 = DesignInputParameter(name="Param_0", value=(2.0, 2000.0))

        param_1 = DesignInputParameter(name="Param_1", value=(2.0, 2000.0))

        param_2 = DesignInputParameter(name="Param_2", value=(20.0, 25.0))

        param_3 = DesignInputParameter(name="Param_3", value=20.0)

        param_4 = DesignInputParameter(name="Param_4", value=46.0)

        param_5 = DesignInputParameter(name="Param_5", value=(200.0, 20000.0))

        sweep = DesignSweep(
            parameters=[param_0, param_1, param_2, param_3, param_4, param_5]
        )

        param_state_with_fixed = list(
            sweep.lhs_states(num_states=10, include_fixed=True, seed=42)
        )

        param_state_with_fixed_repeat = list(
            sweep.lhs_states(num_states=10, include_fixed=True, seed=42)
        )

        assert param_state_with_fixed_repeat == param_state_with_fixed

        assert "Param_4" in param_state_with_fixed[0]
        assert "Param_3" in param_state_with_fixed_repeat[0]

        param_state_without_fixed = list(
            sweep.lhs_states(num_states=10, include_fixed=False, seed=32)
        )

        param_state_without_fixed_repeat = list(
            sweep.lhs_states(num_states=10, include_fixed=False, seed=32)
        )

        assert param_state_without_fixed == param_state_without_fixed_repeat
        assert "Param_4" not in param_state_without_fixed_repeat[0]
        assert "Param_3" not in param_state_without_fixed_repeat[0]
