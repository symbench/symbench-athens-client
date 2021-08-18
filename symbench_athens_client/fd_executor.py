import subprocess
import tempfile
from pathlib import Path

from symbench_athens_client.exceptions import FDMFailedException
from symbench_athens_client.utils import lhs_sampling


class FDMExecutor:
    def __init__(self, fdm_path):
        """The executor for fdm process.

        Parameters
        ----------
        fdm_path: str
            The full path of the new_fdm.exe or new_fdm compiled on a linux system
        """
        self.fdm_path = fdm_path

    def execute(self, input_file, output_file):
        """Execute the FDM process.

        Parameters
        ----------
        input_file: str
            The input file path for the flight dynamics software
        output_file: str
            The output file path for the flight dynamics software
        """
        with subprocess.Popen(
            f"{self.fdm_path} < {input_file} > output_file", shell=True
        ) as fdm_process:
            try:
                fdm_process.wait(300)
                if fdm_process.returncode != 0:
                    raise FDMFailedException(
                        f"The FDM executable failed. The stderr is:\n{fdm_process.stderr}"
                    )
                return self.parse_fdm_output(output_file)
            except subprocess.TimeoutExpired:
                raise FDMFailedException("The FDM Process timed-out. Exiting.")

    @staticmethod
    def parse_fdm_output(output_file):
        with open(output_file) as fdm_output:
            metrics_start = False
            metrics = []
            for line in fdm_output:
                if line.strip().startswith("#Metrics"):
                    print("here")
                    metrics_start = True
                if line and metrics_start:
                    metrics.append(line.strip())
            return metrics


class FDMSampler:
    pass
