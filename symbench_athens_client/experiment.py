from pathlib import Path

from uav_analysis.testbench_data import TestbenchData

from symbench_athens_client.fdm_executor import execute_fd_all_paths
from symbench_athens_client.utils import get_logger


class FlightDynamicsExperiment:
    """The symbench athens client's experiment class.

    Experiment with the SWRI's flight dynamics software based on a fixed-bemp design.

    This class abstracts the enchilada of design constructs,
    exposing the domain scientist i.e. you to things you care about
    i.e. those design variables. Many instances of this classes will be
    available and this is what people are supposed to work on.

    This class also assumes that the flight dynamics software from SWRI is installed
    and available in your PATH.

    ..warning::
        Experimental API, subject to changes

    Parameters
    ----------
    design: symbench_athens_client.models.design.SeedDesign
        The design instance to run this experiment on
    testbench_path: str, pathlib.Path
        The location of the testbench data for estimating mass properties of a design
    propellers_data: str, pathlib.Path
        The location of the propellers data

    Notes
    -----
    Every run gets a guid (returned in the output dictionary). The results for each
    run (the flight dynamics input and output files) are saved in results/artifacts.
    The results/output.csv file is what you should look for if you ever want to revisit
    the metrics.
    """

    def __init__(
        self,
        design,
        testbench_path,
        propellers_data,
        valid_parameters,
        valid_requirements,
    ):
        self.design = design
        self.testbench_path = testbench_path
        self.propellers_data = propellers_data
        self.valid_parameters = valid_parameters
        self.valid_requirements = valid_requirements
        self.logger = get_logger(self.__class__.__name__)
        self._validate_files()

    def _validate_files(self):
        assert (
            Path(self.testbench_path).resolve().exists()
        ), "The testbench data path doesn't exist"
        assert (
            Path(self.propellers_data).resolve().exists()
        ), "The propellers data path doesn't exist"
        tb = TestbenchData()
        try:
            tb.load(self.testbench_path)
        except:
            raise TypeError("The testbench data provided is not valid")

    def run_for(self, parameters=None, requirements=None):
        """Run the flight dynamics for the given parameters and requirements"""
        parameters = self._validate_dict(parameters, "parameters")
        requirements = self._validate_dict(requirements, "requirements")

        for key, value in parameters.items():
            if key in self.valid_parameters:
                setattr(self.design, key, value)

        self.logger.info(
            f"About to execute FDM on {self.design.__class__.__name__}, "
            f"parameters: {self.design.parameters()}, "
            f"requirements: {requirements}"
        )

        return execute_fd_all_paths(
            design=self.design,
            tb_data_location=self.testbench_path,
            propellers_data_location=self.propellers_data,
            **requirements,
        )

    @staticmethod
    def _validate_dict(var, name):
        if var and not isinstance(var, dict):
            raise TypeError(
                f"Expecting {name} to be a dictionary, got {type(var)} instead"
            )

        return var or {}
