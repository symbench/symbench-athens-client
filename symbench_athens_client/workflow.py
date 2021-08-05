from typing import List
from uuid import uuid4

from symbench_athens_client.exceptions import JobFailedError, ParametersMismatchError
from symbench_athens_client.models.jobs import JOB_STATUS, CloneDesign, Job

__all__ = ["WorkFlow"]


class WorkFlow:
    """The symbench Athens Workflow

    Parameters
    ----------
    client: symbench_athens_client.SymbenchAthensClient
        The jenkins client instance for Symbench Jenkins Server
    """

    def __init__(self, client) -> None:
        self.client = client

    def set_job_metadata(self, job, build_info):
        job.status = (
            JOB_STATUS.SUCCESS if build_info.result == "SUCCESS" else JOB_STATUS.FAILED
        )
        job.build_number = build_info.id

    def run(self, design, pipelines, build_params={}, clone=False, clone_name=None):
        jobs = []
        if not isinstance(pipelines, List):
            pipelines = [pipelines]

        if CloneDesign in pipelines:
            raise ValueError("Please use CloneDesign as a separate workflow")

        workflow_design = design
        if clone:
            clone_name = clone_name or design.name + f"clone-{str(uuid4())}"

            clone_job = Job(
                pipeline=CloneDesign,
                design=design,
                parameters={"FromDesignName": "abc", "ToDesignName": clone_name},
            )

            build_info = self.client.build_and_wait(
                clone_job.name, parameters=clone_job.to_jenkins_parameters()
            )

            self.set_job_metadata(clone_job, build_info)
            if clone_job.status != JOB_STATUS.SUCCESS:
                raise JobFailedError(f"Job {clone_job.name} Failed")
            workflow_design = design.copy(deep=True)
            workflow_design.name = clone_name
            jobs.append(clone_job)

        for pipeline in pipelines:
            if len(pipeline.parameters) != len(build_params.get(pipeline.name), []):
                raise ParametersMismatchError(
                    f"Insufficient build paramaters for pipeline {pipeline.name}. "
                    f"required parameters are {pipeline.parameters}"
                )
            parameters_for_job = build_params.get(pipeline.name)
            if clone:
                self.replace_from_dict(
                    parameters_for_job, design.name, workflow_design.name
                )

            job = Job(
                pipeline=pipeline, design=workflow_design, parameters=parameters_for_job
            )

            build_info = self.client.build_and_wait(
                job.name, parameters=clone_job.to_jenkins_parameters()
            )

            self.set_job_metadata(clone_job, build_info)
            if job.status != JOB_STATUS.SUCCESS:
                raise JobFailedError(f"Job {clone_job.name} Failed")

    @staticmethod
    def replace_from_dict(inp_dict, prev_value, new_value):
        for key in inp_dict:
            if inp_dict[key] == prev_value:
                inp_dict[key] = new_value


if __name__ == "__main__":
    from symbench_athens_client.athens_client import SymbenchAthensClient
    from symbench_athens_client.models.designs import QuadSpiderCopter
    from symbench_athens_client.models.jobs import clearComponents

    client = SymbenchAthensClient(
        jenkins_url="http://localhost:8080", username="symcps", password="symcps2021"
    )

    wf = WorkFlow(client)
    design = QuadSpiderCopter()
    wf.run(
        design,
        [clearComponents],
        build_params={"clearComponents": {"DesignName": design.name}},
        clone=True,
    )
