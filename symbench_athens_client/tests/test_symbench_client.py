import os

import pytest

from symbench_athens_client.__main__ import SymbenchAthensClient


@pytest.mark.skip
class TestSymbenchClient:
    @pytest.fixture(scope="session")
    def symbench_client(self):
        return SymbenchAthensClient(
            jenkins_url=os.environ.get("JENKINS_URL"),
            username=os.environ.get("JENKINS_USERNAME"),
            password=os.environ.get("JENKINS_PASSWORD"),
        )

    def test_client_exists(self, symbench_client):
        assert symbench_client

    def test_available_jobs(self, symbench_client):
        jobs = symbench_client.get_available_jobs()
        assert len(jobs) == 6
        job_names = symbench_client.get_available_jobs(names_only=True)
        assert "UAV_Workflows" in job_names
        assert "AddConnection" in job_names
        assert "ClearDesign" in job_names
        assert "CloneDesign" in job_names
        assert "CopyComponent" in job_names
        assert "AddConnection" in job_names
