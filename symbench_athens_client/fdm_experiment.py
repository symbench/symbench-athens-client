import os
from datetime import datetime
from pathlib import Path
from shutil import move, rmtree
from tempfile import mkdtemp
from uuid import uuid4

from uav_analysis.mass_properties import quad_copter_batt_prop, quad_copter_fixed_bemp2
from uav_analysis.testbench_data import TestbenchData

from symbench_athens_client.fdm_executor import (
    FDMExecutor,
    cleanup_score_files,
    update_total_score,
    write_output_csv,
)
from symbench_athens_client.models.components import (
    Batteries,
    Battery,
    Propeller,
    Propellers,
)
from symbench_athens_client.models.designs import QuadCopter
from symbench_athens_client.utils import (
    estimate_mass_formulae,
    extract_from_zip,
    get_logger,
    relative_path,
)


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
    testbenches: str, pathlib.Path or list/set/tuple thereof
        The location of the testbench data for estimating mass properties of a design
    propellers_data: str, pathlib.Path
        The location of the propellers data
    fdm_path: str, pathlib.Path
        The location of the fdm executable, if None, its assumed to be in PATH
    estimator: function, optional, default=None
        The estimator function from uav_analyisis library to use, If None, quadcopter_fixed_bemp2 is used.

    Attributes
    ----------
    session_id: str
        ISO Formatted time stamp
    results_dir: str, pathlib.Path
        The results directory

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
        testbenches,
        propellers_data,
        valid_parameters,
        valid_requirements,
        fdm_path=None,
        estimator=None,
    ):
        self.testbenches, self.propellers_data = self._validate_files(
            testbenches, propellers_data
        )  # ToDo: More robust Validation here
        self.design = design
        self.valid_parameters = valid_parameters
        self.valid_requirements = valid_requirements
        self.logger = get_logger(self.__class__.__name__)
        self.session_id = f"e-{datetime.now().isoformat()}".replace(":", "-")
        self.executor = FDMExecutor(fdm_path=fdm_path)
        self.results_dir = Path(
            f"results/{self.design.__class__.__name__}/{self.session_id}"
        ).resolve()
        self.formulae = estimate_mass_formulae(
            frozenset(self.testbenches),
            estimator=estimator or quad_copter_fixed_bemp2,
        )

    def _create_results_dir(self):
        if not self.results_dir.exists():
            os.makedirs(self.results_dir, exist_ok=True)

        if len(self.testbenches) == 1:
            extract_from_zip(
                self.testbenches[0],
                self.results_dir,
                {
                    "componentMap.json",
                    "connectionMap.json",
                },
            )
        (self.results_dir / ".generated").touch()

        artifacts_dir = self.results_dir / "artifacts"
        if not artifacts_dir.exists():
            os.makedirs(artifacts_dir)

    def start(self):
        self._create_results_dir()

    def run_for(
        self,
        parameters=None,
        requirements=None,
        change_dir=False,
        write_to_output_csv=False,
    ):
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

        run_guid = str(uuid4())

        fd_files_base_path = self.results_dir / "artifacts" / run_guid
        os.makedirs(fd_files_base_path, exist_ok=True)

        metrics = {"GUID": run_guid, "AnalysisError": None}
        try:
            current_dir = os.getcwd()
            if change_dir:
                os.chdir(fd_files_base_path)

            for i in [1, 3, 4, 5]:
                fd_input_path = f"FlightDyn_Path{i}.inp"
                fd_output_path = f"FlightDynReport_Path{i}.out"

                self.design.to_fd_input(
                    testbench_path_or_formulae=self.formulae,
                    requested_vertical_speed=0
                    if i != 4
                    else requirements.get("requested_vertical_speed", -2),
                    requested_lateral_speed=0
                    if i == 4
                    else int(requirements.get("requested_lateral_speed", 10)),
                    flight_path=i,
                    propellers_data_path=relative_path(
                        os.getcwd(), self.propellers_data
                    )
                    + os.sep,
                    filename=fd_input_path,
                )

                input_metrics, flight_metrics, path_metrics = self.executor.execute(
                    str(fd_input_path), str(fd_output_path)
                )

                # Input Metrics
                metrics.update(input_metrics.to_csv_dict())
                other_metrics = self.design.parameters()
                for key in other_metrics:
                    if key.startswith("Length"):
                        metrics[key] = other_metrics[key]

                # Get the FlightPath metrics
                metrics.update(flight_metrics.to_csv_dict())
                metrics.update(path_metrics.to_csv_dict())

                # Move input and output files to necessary locations
                if not change_dir:
                    move(fd_input_path, fd_files_base_path)
                    move(fd_output_path, fd_files_base_path)

                move("./metrics.out", fd_files_base_path / f"metrics_Path{i}.out")

                # Remove metrics.out, score.out namemap.out
                cleanup_score_files()

            # Update the total score
            update_total_score(metrics)
            metrics["AnalysisError"] = False

            if change_dir:
                os.chdir(current_dir)

        except Exception as e:
            metrics["AnalysisError"] = True
            raise e

        if write_to_output_csv:
            write_output_csv(output_dir=self.results_dir, metrics=metrics)

        return metrics

    def start_new_session(self):
        self.session_id = f"e-{datetime.now().isoformat()}".replace(":", "-")
        self.results_dir = Path(
            f"results/{self.design.__class__.__name__}/{self.session_id}"
        ).resolve()
        self.start()

    @staticmethod
    def _validate_dict(var, name):
        if var and not isinstance(var, dict):
            raise TypeError(
                f"Expecting {name} to be a dictionary, got {type(var)} instead"
            )

        return var or {}

    @staticmethod
    def _validate_files(testbenches, propellers_data):
        if isinstance(testbenches, (list, set, tuple)):
            assert all(
                Path(testbench).resolve().exists() for testbench in testbenches
            ), "Testbench data paths are not valid"
        else:
            testbenches = Path(testbenches).resolve()
            assert testbenches.exists(), "The testbench data path doesn't exist"
            testbenches = [testbenches]

        propellers_data = Path(propellers_data).resolve()
        assert (
            propellers_data.resolve().exists()
        ), "The propellers data path doesn't exist"
        tb = TestbenchData()
        try:
            for d in testbenches:
                tb.load(str(d))
        except:
            raise TypeError("The testbench data provided is not valid")
        return testbenches, propellers_data


class QuadCopterVariableBatteryPropExperiment(FlightDynamicsExperiment):
    def __init__(
        self,
        testbenches,
        propellers_data,
        fdm_path=None,
    ):
        design = QuadCopter()
        valid_parameters = design.__design_vars__
        valid_requirements = {"requested_vertical_speed", "requested_lateral_speed"}
        super().__init__(
            design,
            testbenches,
            propellers_data,
            valid_parameters,
            valid_requirements,
            fdm_path=fdm_path,
            estimator=quad_copter_batt_prop,
        )

    def run_for(
        self,
        battery=None,
        propeller=None,
        parameters=None,
        requirements=None,
        change_dir=False,
        write_to_output_csv=False,
    ):
        if isinstance(battery, str):
            assert battery in self.available_batteries, "Battery name is not valid"
            battery = Batteries[battery]

        if isinstance(propeller, str):
            assert propeller in self.available_propellers, "Propeller name is not valid"
            propeller = Propellers[propeller]

        assert isinstance(
            battery, Battery
        ), f"Provided {battery} is not a Battery component"
        assert isinstance(
            propeller, Propeller
        ), f"Provided {propeller} is not a Propeller component"

        self._assign_battery(self.design, battery)
        self._assign_propellers(self.design, propeller)

        return super().run_for(
            parameters=parameters,
            requirements=requirements,
            change_dir=change_dir,
            write_to_output_csv=write_to_output_csv,
        )

    @property
    def available_batteries(self):
        return Batteries.all

    @property
    def available_propellers(self):
        return Propellers.all

    @staticmethod
    def _assign_battery(design, battery):
        design.battery_0 = battery

    @staticmethod
    def _assign_propellers(design, propeller):
        design.propeller_0 = propeller
        design.propeller_1 = propeller
        design.propeller_2 = propeller
        design.propeller_3 = propeller
