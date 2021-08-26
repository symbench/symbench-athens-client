from symbench_athens_client.exceptions import MissingExperimentError
from symbench_athens_client.fdm_experiment import FlightDynamicsExperiment
from symbench_athens_client.models.fixed_bemp_designs import (
    TurnigyGraphene5000MAHQuadCopter,
    TurnigyGraphene6000MAHQuadCopter,
)

# Note this will not work, unless you have the correct paths.
# This is just provided for convenience


def get_experiments_by_name(name):
    experiments = {
        "ExperimentOnTurnigyGraphene5000MAHQuadCopter": dict(
            design=TurnigyGraphene5000MAHQuadCopter(),
            testbench_path="./testbenches/TurnigyGraphene5000MAHQuadCopter.zip",
            propellers_data="./propellers/",
            valid_parameters=TurnigyGraphene5000MAHQuadCopter.__design_vars__,
            valid_requirements={"requested_vertical_speed", "requested_lateral_speed"},
        ),
        "ExperimentOnTurnigyGraphene6000MAHQuadCopter": dict(
            design=TurnigyGraphene6000MAHQuadCopter(),
            testbench_path="./testbenches/TurnigyGraphene6000MAHQuadCopter.zip",
            propellers_data="./propellers/",
            valid_parameters=TurnigyGraphene6000MAHQuadCopter.__design_vars__,
            valid_requirements={"requested_vertical_speed", "requested_lateral_speed"},
        ),
    }

    if name not in experiments:
        raise MissingExperimentError("The experiment {name} doesn't exist.")

    return FlightDynamicsExperiment(**experiments[name])
