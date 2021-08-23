import math
import os
import subprocess
import zipfile
from csv import DictWriter
from glob import glob
from pathlib import Path
from shutil import move
from uuid import uuid4

from symbench_athens_client.exceptions import FDMFailedException
from symbench_athens_client.models.designs import QuadCopter
from symbench_athens_client.models.fd_metrics import (
    FDMFlightMetric,
    FDMFlightPathMetric,
    FDMInputMetric,
)
from symbench_athens_client.utils import get_logger


class FDMExecutor:
    def __init__(self, fdm_path=None):
        """The executor for fdm process.

        Parameters
        ----------
        fdm_path: str, default=None
            The full path of the new_fdm.exe or new_fdm compiled on a linux system (can be none if its already in your path)
        """
        self.fdm_path = fdm_path or "new_fdm"
        self.logger = get_logger(self.__class__.__name__)

    def execute(self, input_file, output_file):
        """Execute the FDM process.

        Parameters
        ----------
        input_file: str
            The input file path for the flight dynamics software
        output_file: str
            The output file path for the flight dynamics software
        """
        fdm_cmd = f"{self.fdm_path} < {input_file} > {output_file}"
        self.logger.info(f"Opening the FDM execution process as {fdm_cmd}")
        with subprocess.Popen(fdm_cmd, shell=True) as fdm_process:
            try:
                fdm_process.wait(300)
                if fdm_process.returncode != 0:
                    raise FDMFailedException(
                        f"The FDM executable failed. The stderr is:\n{fdm_process.stderr}"
                    )

                return (
                    FDMInputMetric.from_fd_input(input_file),
                    FDMFlightMetric.from_fd_metrics("metrics.out"),
                    FDMFlightPathMetric.from_fd_metrics("metrics.out"),
                )

            except subprocess.TimeoutExpired:
                raise FDMFailedException("The FDM Process timed-out. Exiting.")


def _update_total_score(metrics):
    scores = [
        metrics["Path_score_Path1"],
        metrics["Path_score_Path3"],
        metrics["Path_score_Path4"],
        metrics["Path_score_Path5"],
    ]
    metrics["TotalPathScore"] = sum(scores) if not math.isclose(scores[2], 0.0) else 0.0


def _write_output_csv(output_dir, metrics):
    # Note that this should be a pathlib.Path instance,
    # but since this is an internal use function which might be
    # refactored anyways. Its always fine to do it this way
    output_csv = output_dir / "output.csv"
    should_write_header = True

    if output_csv.exists():
        should_write_header = False

    with open(output_csv, "a") as csv_file:
        csv_writer = DictWriter(
            csv_file, fieldnames=list(metrics.keys()), lineterminator="\n"
        )
        if should_write_header:
            csv_writer.writeheader()
        csv_writer.writerow(metrics)


def _cleanup_score_files():
    out_files = glob("*.out")
    for file in out_files:
        os.unlink(file)


def _copy_testbench_files(testbench_path, output_dir):
    files_of_interest = {
        "componentMap.json",
        "connectionMap.json",
    }
    if not isinstance(testbench_path, Path):
        testbench_path = Path(testbench_path).resolve()
    assert testbench_path.exists(), "The provided path doesn't exist"
    assert testbench_path.suffix == ".zip", "The testbench is not a zip file"

    with testbench_path.open("rb") as testbench_zip:
        with zipfile.ZipFile(testbench_zip) as zip_file:
            for file in zip_file.namelist():
                if file in files_of_interest:
                    zip_file.extract(file, output_dir)


def execute_fd_all_paths(
    design,
    tb_data_location,
    requested_vertical_speed=10.0,
    requested_lateral_speed=1,
    propellers_data_location=f"../data/propellers",
    fdm_path=None,
    output_dir="results",
):
    """Execute flight dynamics on all paths for a design(only works for quadcopter).

    Parameters
    ----------
    design: QuadCopter
        The quadCopter seed design instance
    tb_data_location: str, pathlib.Path
        The testbench data location to compute mass properties for this design
    requested_vertical_speed: float, default = 10.0
        The requested vertical speed for this run
    requested_lateral_speed: float, default = 1.0
        The requested lateral speed for this run
    propellers_data_location: str, pathlib.Path, default="../data/propellers"
        The location for the propellers data
    fdm_path: str, pathlib.Path, default=None
        The fdm executable path (If None, it is assumed that fdm is in your path)
    output_dir: str, patlib.Path, default="results"
        Where to save the output to

    Returns
    -------
    The contents of output.csv (Metrics) as a dictionary
    """

    assert isinstance(
        design, QuadCopter
    ), "The function only works for quadcopter design"

    output_dir = Path(output_dir).resolve()
    if not output_dir.exists():
        os.makedirs(output_dir)
    run_guid = str(uuid4())
    artifacts_dir = output_dir / "artifacts"
    if not artifacts_dir.exists():
        os.makedirs(artifacts_dir)

    fd_files_base_path = artifacts_dir / run_guid
    os.makedirs(fd_files_base_path, exist_ok=True)

    # Copy relavent testbench files
    _copy_testbench_files(tb_data_location, output_dir)

    # Keep a .generated mark
    (output_dir / ".generated").touch()

    executor = FDMExecutor(fdm_path=fdm_path)

    metrics = {"GUID": run_guid, "AnalysisError": None}
    try:
        for i in [1, 3, 4, 5]:
            fd_input_path = f"FlightDyn_Path{i}.inp"
            fd_output_path = f"FlightDynReport_Path{i}.out"

            design.to_fd_input(
                test_bench_path=str(tb_data_location),
                requested_vertical_speed=0 if i != 4 else requested_vertical_speed,
                requested_lateral_speed=0 if i == 0 else int(requested_lateral_speed),
                flight_path=i,
                propellers_data_path=str(propellers_data_location),
                filename=fd_input_path,
            )

            input_metrics, flight_metrics, path_metrics = executor.execute(
                str(fd_input_path), str(fd_output_path)
            )

            # Input Metrics
            metrics.update(input_metrics.to_csv_dict())

            # Get the FlightPath metrics
            metrics.update(flight_metrics.to_csv_dict())
            metrics.update(path_metrics.to_csv_dict())

            # Move input and output files to necessary locations
            move(fd_input_path, fd_files_base_path)
            move(fd_output_path, fd_files_base_path)

            # Remove metrics.out, score.out namemap.out
            _cleanup_score_files()

        # Update the total score
        _update_total_score(metrics)
        metrics["AnalysisError"] = False

    except Exception as e:
        metrics["AnalysisError"] = True
        raise e

    _write_output_csv(output_dir=output_dir, metrics=metrics)

    return metrics
