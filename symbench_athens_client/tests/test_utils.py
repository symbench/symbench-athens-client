import pytest

from symbench_athens_client.exceptions import PropellerAssignmentError
from symbench_athens_client.models.components import Propellers
from symbench_athens_client.models.designs import QuadCopter
from symbench_athens_client.utils import assign_propellers_quadcopter


class TestUtils:
    def test_design_assign_propellers_valid(self):
        design = QuadCopter()
        prop_neg = Propellers.apc_propellers_6x4EP
        prop_pos = Propellers.apc_propellers_6x4E
        assign_propellers_quadcopter(design, prop_neg)
        assert design.propeller_0 == design.propeller_2 == prop_neg
        assert design.propeller_1 == design.propeller_3 == prop_pos

        assign_propellers_quadcopter(design, prop_pos)
        assert design.propeller_0 == design.propeller_2 == prop_neg
        assert design.propeller_1 == design.propeller_3 == prop_pos

    def test_design_assign_propellers_invalid(self):
        design = QuadCopter()
        with pytest.raises(PropellerAssignmentError):
            assign_propellers_quadcopter(
                design, propeller=Propellers.apc_propellers_17x10N
            )

    def test_assign_propellers_type_error(self):
        design = QuadCopter()
        with pytest.raises(TypeError):
            assign_propellers_quadcopter(design, 1)

    def test_assign_propellers_string_name(self):
        design = QuadCopter()
        assign_propellers_quadcopter(design, "apc_propellers_6x4E")
        assert (
            design.propeller_0.name == design.propeller_2.name == "apc_propellers_6x4EP"
        )
        assert (
            design.propeller_1.name == design.propeller_3.name == "apc_propellers_6x4E"
        )
