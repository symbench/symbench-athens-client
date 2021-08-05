import logging
import time

import api4jenkins
from api4jenkins import user
from api4jenkins.exceptions import ItemNotFoundError
from api4jenkins.item import Item

from symbench_athens_client.utils import get_logger

__all__ = ["SymbenchAthensClient"]


class SymbenchAthensClient:
    """The client to the symbench athens server.

    Parameters
    ----------
    jenkins_url: str
        The url for the jenkins server
    username: str
        The username to login with
    password: str
        The password to login with

    Attributes
    ----------
    server: api4jenkins.Jenkins
        The python interface for the jenkins server
    """

    def __init__(self, jenkins_url, username, password, log_level=logging.DEBUG):
        self.server = api4jenkins.Jenkins(jenkins_url, auth=(username, password))
        self.logger = get_logger(self.__class__.__name__, log_level)
        self.logger.info(f"User with username {username} successfully logged in")

    def get_user_info(self):
        """Return information for the currently logged in user."""
        user = self.server.user
        return {
            "fullName": user.full_name,
            "id": user.id,
            "description": user.description,
        }

    def get_available_jobs(self, names_only=False):
        """Returns available jobs from the server.

        Parameters
        ----------
        names_only: bool, default=False
            If true, return the job names only

        Returns
        -------
        list of dict or list of str
            The jobs available in the server
        """
        jobs = []
        for job in self.server.iter_jobs():
            jobs.append(job.full_name if names_only else job.api_json())
        return jobs

    def get_job_info(self, job_name):
        """Get information about the job and its builds"""
        job = self.server.get_job(job_name)
        assert job, f"Provided job {job_name} doesn't exist"
        return job.api_json()

    def can_execute(self):
        """Return True if any worker nodes are connected"""
        executor_nodes = list(
            filter(lambda node: node.name != "(master)", self.server.nodes)
        )

        return not all(node.offline for node in executor_nodes)

    def build_and_wait(self, job_name, parameters):
        """Build a job and wait

        Parameters
        ----------
        job: str
            Name of the job
        parameters: dict
            Parameters for this build
        """
        job = self.server.get_job(job_name)
        if job is None:
            raise ItemNotFoundError(f"Job with name {job_name} doesn't exist")
        item = job.build(**parameters)
        self.logger.info(f"Job {job_name} is waiting to be built")

        while not item.get_build():
            time.sleep(1)

        self.logger.info(f"Job {job_name} is built")

        build = item.get_build()
        self.logger.info(f"Job {job_name} is running")
        while not build.result:
            time.sleep(1)
        self.logger.info(f"Job {job_name} is finished. The result is {build.result}")
        return build
