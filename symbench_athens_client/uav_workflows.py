import csv
import io
import logging
import time
import zipfile
from tempfile import TemporaryDirectory
from uuid import uuid4

import requests

from symbench_athens_client.athens_client import SymbenchAthensClient
from symbench_athens_client.models.pipelines import (
    ClearDesign,
    CloneDesign,
    SwapComponent,
)
from symbench_athens_client.models.uav_pipelines import (
    CircularFlight,
    GeometryV1,
    HoverCalc,
    InitialConditionsFlight,
    RacingOvalFlight,
    RiseAndHoverFlight,
    StraightLineFlight,
    TrimSteadyFlight,
)


class UAVWorkflowRunner(SymbenchAthensClient):
    """UAVWorkflow Runner class

    Notes
    -----
    This class subclasses the SymbenchAthensClient (architecture is hairy),
    can switch to composition in the future.

    See Also
    --------
    symbench_athens_client.athens_client.SymbenchAthensClient
        The Jenkins server interface which uses api4Jenkins to
        communicate with the jenkins server
    """

    def __init__(self, jenkins_url, username, password, log_level=logging.DEBUG):
        super().__init__(jenkins_url, username, password, log_level)

    def _clone_design(self, design, new_name=None):
        """Clone a design from the graph database

        Parameters
        ----------
        design: symbench_athens_client.models.designs.SeedDesign
            The design to clone
        """

        clone_name = new_name or f"{design.name}_{str(uuid4())}"
        self.logger.info(f"About to clone design {design.name} to {clone_name}")

        clone_job = CloneDesign(from_design_name=design.name, to_design_name=clone_name)

        self.build_and_wait(clone_job.pipeline_name, clone_job.to_jenkins_parameters())

        design.name = clone_name
        self.logger.info(f"Successfully cloned the design as {design.name}")

    def _clear_design(self, design):
        """Clear a design from the graph database

        Parameters
        ----------
        design: symbench_athens_client.models.designs.SeedDesign
            The design to delete/clear
        """
        clear_job = ClearDesign(design_name=design.name)

        self.logger.info(f"About to clear design {design}")

        self.build_and_wait(clear_job.pipeline_name, clear_job.to_jenkins_parameters())

        design.reset_name()
        self.logger.info(f"Cleared Design, name has been reset to {design.name}")

    def _swap_components(self, design):
        """Given a design, iterate through its swap list and begin swapping components

        Parameters
        ----------
        design: symbench_athens_client.models.designs.SeedDesign
            The design to delete/clear
        """
        for component_instance_name, swap_list in design.swap_list.items():
            swap_job = SwapComponent(
                design=design.name,
                ci_name=component_instance_name,
                from_comp_name=swap_list[0],
                to_comp_name=swap_list[-1],
            )

            self.logger.info(
                f"{component_instance_name} of {design.name} will be changed from {swap_job.from_comp_name} to {swap_job.to_comp_name}"
            )
            self.build_and_wait(
                swap_job.pipeline_name, swap_job.to_jenkins_parameters()
            )

        design.clear_swap()

    def _results_from_build(self, build):
        """Return results from a particular build as a list of dictionaries"""
        build_artifacts = build.api_json()["artifacts"]
        if len(build_artifacts):
            artifact_url = f'{build.url}artifact/{build_artifacts[0]["relativePath"]}'
            with TemporaryDirectory() as tmpdir:
                response = requests.get(
                    artifact_url, auth=(self.username, self.password)
                )
                if response.status_code != 200:
                    raise FileNotFoundError
                else:
                    artifacts_content = response.content
                    filename = f"{tmpdir}/data.zip"
                    with open(filename, "wb") as zip_artifact:
                        zip_artifact.write(artifacts_content)

                    with zipfile.ZipFile(filename) as zip_file:
                        with zip_file.open("output.csv") as csv_file:
                            csv_str = csv_file.read().decode("utf-8")
                            rows = csv.DictReader(io.StringIO(csv_str))
                            ops = []
                            for row in rows:
                                for k, v in row.items():
                                    try:
                                        row[k] = eval(v)
                                    except SyntaxError:
                                        pass
                                ops.append(row)

                            return ops

    def _run_uav_workflow(self, pipeline):
        """Run a UAV Workflow instance

        Parameters
        ----------
        pipeline: symbench_athens_client.models.uav_pipelines.UAVWorkflow
            A particular UAV Workflow instance

        Returns
        -------
        list of dict
            The results (logged in output.csv as a list of dictionaries)
        """
        build = self.build_and_wait(
            pipeline.pipeline_name, parameters=pipeline.to_jenkins_parameters()
        )
        while not build.api_json()["artifacts"]:
            time.sleep(2)
        return self._results_from_build(build)

    def run_hover_calc(self, design, num_samples=1, clone=True, clear=True):
        """Run HoverCalc test bench on the design

        Parameters
        ----------
        design: symebench_athens_client.models.designs.SeedDesign
            The Seed design to run this testbench on

        num_samples: int, default=1
            Number of samples to execute for Monte Carlo DOE, uniformly sampled

        clone: bool, default=True
            If True, clone the design before starting HoverCalc

        clear: bool, default=True
            If True, clear the design after completing HoverCalc

        Notes
        -----
        If some components in the design need swapping, those components will be swapped in the database
        """
        self.logger.info(
            f"Starting HoverCalc on {design.name} with number_samples={num_samples}, clone={clone}, clear={clear}"
        )
        if clone:
            self._clone_design(design)

        if design.needs_swap():
            self._swap_components(design)

        hover_calc = HoverCalc(design=design, num_samples=num_samples)

        results = self._run_uav_workflow(hover_calc)

        if clear:
            self._clear_design(design)

        self.logger.info(
            f"Finished HoverCalc on {design.name} with number_samples={num_samples}, clone={clone}, clear={clear}"
        )

        return results

    def run_geometry_v1(self, design, num_samples=1, clone=True, clear=True):
        """Run GeometryV1 test bench on the design

        Parameters
        ----------
        design: symebench_athens_client.models.designs.SeedDesign
            The Seed design to run this testbench on

        num_samples: int, default=1
            Number of samples to execute for Monte Carlo DOE, uniformly sampled\

        clone: bool, default=True
            If True, clone the design before starting HoverCalc

        clear: bool, default=True
            If True, clear the design after completing HoverCalc

        Notes
        -----
        If some components in the design need swapping, those components will be swapped in the database
        """
        self.logger.info(
            f"Starting GeometryV1 on {design.name} with number_samples={num_samples}, clone={clone}, clear={clear}"
        )
        if clone:
            self._clone_design(design)

        if design.needs_swap():
            self._swap_components(design)

        geometry_v1 = GeometryV1(design=design, num_samples=num_samples)

        results = self._run_uav_workflow(geometry_v1)

        if clear:
            self._clear_design(design)

        self.logger.info(
            f"Finished GeometryV1 on {design.name} with number_samples={num_samples}, clone={clone}, clear={clear}"
        )

        return results
