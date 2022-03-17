import json
import os.path
import time
from csv import DictWriter

from symbench_athens_client.models.design_state_creo import DesignSweep
from symbench_athens_client.utils import create_directory, get_logger


class CREOExperiment:
    """Run an experiment in creo.

    Parameters
    ----------
    design_in_creo: symbench_athens_client import SymbenchDesignInCREO
        A design instance opened in creo for which the experiment is run

    outdir: str, pathlib.Path
        The directory to save the output file in
    """

    def __init__(self, design_in_creo, outdir):
        self.design_in_creo = design_in_creo
        self.logger = get_logger(self.__class__.__name__)
        self.logger.setLevel(design_in_creo.logger.level)
        self.outdir = create_directory(outdir)
        self.results_dir = None
        self.intf_dir = None
        self.output_file = None
        self.op_csv_writer = None
        self.failures_file = None

    def _create_new_run_directory(self):
        return create_directory(
            self.outdir
            / f"CREO_experiment_{time.strftime('%b_%d_%Y_%H_%M_%S', time.localtime())}"
        )

    def _set_design_params(self, params):
        self.logger.debug("Setting fixed parameters for the design")
        state = self.design_in_creo.apply_params(params)
        self.logger.info("Successfully set fixed parameters for the design")
        return state

    def _initialize_writers(self):
        self.output_file = open(self.results_dir / "output.csv", "w")
        self.failures_file = open(self.results_dir / "failures.txt", "w")
        op_csv_keys = self.design_in_creo.get_state().flat_dict().keys()
        self.op_csv_writer = DictWriter(self.output_file, fieldnames=op_csv_keys)
        self.op_csv_writer.writeheader()

    def _record_state(self, state, record_intf_data):
        self.op_csv_writer.writerow(state.flat_dict())
        if record_intf_data and len(state.interferences_dict()):
            with open(self.intf_dir / f"{state.GUID}.json", "w") as intf_json_file:
                json.dump(state.interferences_dict(), intf_json_file)

        self.logger.info(f"Recorded state with GUID {state.GUID}")

    def _record_failure(self, params, e):
        self.failures_file.write(f"{params} {e}\n")

    def _deinit_writers(self):
        self.output_file.close()
        self.failures_file.close()
        self.output_file = None
        self.op_csv_writer = None
        self.failures_file = None

    def _deinit_result_dirs(self):
        self.results_dir = None
        self.intf_dir = None

    def run_and_record(self, sweep_dict, samples=10000, record_intf_data=False):
        self.results_dir = self._create_new_run_directory()
        self.intf_dir = create_directory(self.results_dir / "interferences")
        self._initialize_writers()

        self.logger.info(f"Results for this run will be saved in {self.results_dir}")
        design_sweep = DesignSweep(**sweep_dict)
        self._set_design_params(dict(design_sweep.fixed_params()))

        start = time.time()
        for params in design_sweep.lhs_sweep(num_states=samples):
            try:
                state = self._set_design_params(params)
                self._record_state(state, record_intf_data)
            except Exception as e:
                self.logger.error(e)
                self._record_failure(params, e)
            time.sleep(0.001)
        end = time.time()
        self.logger.info(f"Time taken for {samples} samples: {end - start} seconds.")

        self._deinit_writers()
        self._deinit_result_dirs()


if __name__ == "__main__":
    from symbench_athens_client.design_in_creo import SymbenchDesignInCREO
    from symbench_athens_client.tests.utils import get_test_file_path

    parameters_map = get_test_file_path("rake_parameters_map.json")
    with open(parameters_map) as json_file:
        parameters_map = json.load(json_file)

    rake = SymbenchDesignInCREO(
        assembly_path="./TestBench_CADTB_V1/uav_1.asm", parameters_map=parameters_map
    )

    experiment = CREOExperiment(
        design_in_creo=rake, outdir="./results-experiment-in-creo"
    )

    params_dict = "./rake_sweep.json"
    with open(params_dict) as json_file:
        params_dict = json.load(json_file)

    experiment.run_and_record(params_dict, samples=100)
