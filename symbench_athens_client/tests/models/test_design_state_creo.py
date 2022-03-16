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
    @pytest.fixture
    def param_list(self):
        param_0 = DesignInputParameter(name="Param_0", value=(2.0, 2000.0))

        param_1 = DesignInputParameter(name="Param_1", value=(2.0, 2000.0))

        param_2 = DesignInputParameter(name="Param_2", value=(20.0, 25.0))

        param_3 = DesignInputParameter(name="Param_3", value=20.0)

        param_4 = DesignInputParameter(name="Param_4", value=46.0)

        param_5 = DesignInputParameter(name="Param_5", value=(200.0, 20000.0))

        return [param_0, param_1, param_2, param_3, param_4, param_5]

    def test_interference(self):
        with pytest.raises(ValidationError):
            interference = Interference(
                part_1_name="ABC",
                part_2_name="XYZ",
            )

        interference = Interference(
            part_1_name="ABC", part_2_name="XYZ", interference_volume=220.0
        )
        assert interference.interference_volume == 220.0

    def test_design_state(self, param_list):
        mass_props = MassProperties(
            mass=2.0,
            surface_area=3000.0,
            density=3.0,
            cgIxx=2500,
            cgIxy=3203,
            cgIxz=2930,
            cgIyx=30000.0,
            cgIyy=2432.5,
            cgIyz=2343.6,
            cgIzx=24.9,
            cgIzy=243.5,
            cgIzz=2232.5,
            coordIxx=2500,
            coordIxy=3203,
            coordIxz=2930,
            coordIyx=30000.0,
            coordIyy=2432.5,
            coordIyz=2343.6,
            coordIzx=24.9,
            coordIzy=243.5,
            coordIzz=2232.5,
        )

        interference = Interference(
            part_1_name="ABC", part_2_name="XYZ", interference_volume=220.0
        )

        with pytest.raises(TypeError):
            mass_props.mass = 3.0

        with pytest.raises(TypeError):
            interference.interference_volume = 300.0

        design_state = CreoDesignState(
            mass_properties=mass_props,
            interferences=[interference],
            parameters=param_list,
        )

        flat_dict = design_state.flat_dict()

        assert flat_dict["interferences"] is True
        assert flat_dict["number_of_interferences"] == 1
        assert flat_dict["mass"] == 2.0
        assert flat_dict["coordIyx"] == 30000.0

    def test_design_sweep(self, param_list):

        sweep = DesignSweep(parameters=param_list)

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
