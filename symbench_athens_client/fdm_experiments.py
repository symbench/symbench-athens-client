import glob
import random

from symbench_athens_client.exceptions import MissingExperimentError
from symbench_athens_client.fdm_experiment import (
    FlightDynamicsExperiment,
    QuadCopterVariableBatteryPropExperiment,
)
from symbench_athens_client.models.fixed_bemp_designs import (
    QuadCopter_5,
    QuadCopter_5Light,
    TurnigyGraphene5000MAHQuadCopter,
    TurnigyGraphene6000MAHQuadCopter,
)


def get_testbench_zips(root):
    zips = glob.glob(root + "/*.zip")
    return zips


# Note this will not work, unless you have the correct paths.
# This is just provided for convenience
def get_experiments_by_name(name):
    experiments = {
        "ExperimentOnTurnigyGraphene5000MAHQuadCopter": dict(
            design=TurnigyGraphene5000MAHQuadCopter(),
            testbenches="./testbenches/TurnigyGraphene5000MAHQuadCopter.zip",
            propellers_data="./propellers/",
            valid_parameters=TurnigyGraphene5000MAHQuadCopter.__design_vars__,
            valid_requirements={"requested_vertical_speed", "requested_lateral_speed"},
        ),
        "ExperimentOnTurnigyGraphene6000MAHQuadCopter": dict(
            design=TurnigyGraphene6000MAHQuadCopter(),
            testbenches="./testbenches/TurnigyGraphene6000MAHQuadCopter.zip",
            propellers_data="./propellers/",
            valid_parameters=TurnigyGraphene6000MAHQuadCopter.__design_vars__,
            valid_requirements={"requested_vertical_speed", "requested_lateral_speed"},
        ),
        "ExperimentOnQuadCopter_5": dict(
            design=QuadCopter_5(),
            testbenches="./testbenches/QuadCopter_5.zip",
            propellers_data="./propellers/",
            valid_parameters=QuadCopter_5.__design_vars__,
            valid_requirements={"requested_vertical_speed", "requested_lateral_speed"},
        ),
        "ExperimentOnQuadCopter_5Light": dict(
            design=QuadCopter_5Light(),
            testbenches="./testbenches/QuadCopter_5Light.zip",
            propellers_data="./propellers/",
            valid_parameters=QuadCopter_5Light.__design_vars__,
            valid_requirements={"requested_vertical_speed", "requested_lateral_speed"},
        ),
        "QuadCopterVariableBatteryPropExperiment": dict(
            testbenches=get_testbench_zips(
                "./testbenches/QuadCopterVariablePropellerBattery/"
            ),
            propellers_data="./propellers",
        ),
    }

    if name not in experiments:
        raise MissingExperimentError("The experiment {name} doesn't exist.")

    if name == "QuadCopterVariableBatteryPropExperiment":
        return QuadCopterVariableBatteryPropExperiment(**experiments[name])
    else:
        return FlightDynamicsExperiment(**experiments[name])
